import time
from rich.console import Console
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings

# --------------------------------------------------
# Configuration
# --------------------------------------------------

DB_DIR = "chroma_db"
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "phi3:latest"

TOP_K = 5
MAX_DISTANCE = 0.7
DEBUG = True

console = Console()

# --------------------------------------------------
# Initialize
# --------------------------------------------------

embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

db = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embeddings,
)

llm = ChatOllama(
    model=LLM_MODEL,
    temperature=0,
    num_predict=300,
    repeat_penalty=1.2,
    top_k=20,
)

# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def retrieve(question: str):
    raw_results = db.similarity_search_with_score(question, k=TOP_K)
    filtered_results = [(doc, score) for doc, score in raw_results if score <= MAX_DISTANCE]
    return raw_results, filtered_results

def build_prompt(context: str, question: str) -> str:
    return f"""
You are Bilal AI Tutor, a helpful technical tutor.

Answer the user's question using the retrieved Context.

- Never invent facts.
- Use bullet points when helpful.
- Mention the document source if useful.

Context:
{context}

Question:
{question}

Answer:
"""

def print_sources(results):
    console.print("\n[bold]Sources[/bold]")
    seen = set()
    for doc, _ in results:
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "?")
        key = (source, page)
        if key not in seen:
            seen.add(key)
            console.print(f"- {source} (page {page})")

# --------------------------------------------------
# Main Loop
# --------------------------------------------------

try:
    while True:
        question = input("You: ").strip()

        # Guard against empty input
        if not question:
            console.print("[yellow]No question entered. Please type something.[/yellow]")
            continue

        if question.lower() == "exit":
            break

        retrieval_start = time.perf_counter()
        raw_results, docs_and_scores = retrieve(question)
        retrieval_time = time.perf_counter() - retrieval_start

        console.print(f"\nRetrieved {len(raw_results)} candidates -> {len(docs_and_scores)} accepted\n")

        if DEBUG:
            console.print("[yellow]Candidate Scores[/yellow]")
            for i, (doc, score) in enumerate(raw_results, start=1):
                console.print(f"{i}. Score={score:.4f} | Page={doc.metadata.get('page', '?')}")
            console.print()

        if not docs_and_scores:
            console.print("[red]No relevant documents matched the similarity threshold.[/red]")
            console.print("\nTry:\n- Rephrasing your question\n- Using different keywords\n- Increasing MAX_DISTANCE\n")
            continue

        console.print("[bold]Retrieved Documents[/bold]\n")
        docs = []
        for i, (doc, score) in enumerate(docs_and_scores, start=1):
            docs.append(doc)
            console.print(f"{i}. {doc.metadata.get('source', 'Unknown')} (page {doc.metadata.get('page', '?')}) score={score:.4f}")

        # Limit context size for Phi-3
        context = "\n\n".join(doc.page_content[:1200] for doc in docs)
        prompt = build_prompt(context=context, question=question)

        generation_start = time.perf_counter()
        try:
            response = llm.invoke(prompt)
        except Exception as e:
            console.print(f"\n[red]LLM Error:[/red] {e}")
            continue
        generation_time = time.perf_counter() - generation_start

        console.print("\n[bold green]Assistant[/bold green]\n")
        console.print(response.content)

        print_sources(docs_and_scores)

        console.print(f"\nRetrieval Time : {retrieval_time:.2f}s")
        console.print(f"Generation Time: {generation_time:.2f}s")
        console.print("\n" + "-" * 70 + "\n")

except KeyboardInterrupt:
    console.print("\n[yellow]Goodbye![/yellow]")
