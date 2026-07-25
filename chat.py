from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings

DB_DIR = "chroma_db"

embeddings = OllamaEmbeddings(model="nomic-embed-text")

db = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embeddings
)

llm = ChatOllama(
    model="phi3",
    temperature=0,
    num_predict=300,
    repeat_penalty=1.2,
    top_k=20
)

print("=== Local RAG Assistant ===")
print("Type 'exit' to quit.\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":
        break

    # Recherche
    docs_and_scores = db.similarity_search_with_score(question, k=5)

    docs = [doc for doc, score in docs_and_scores]

    print(f"\nRetrieved {len(docs)} documents\n")

    if not docs:
        print("No relevant documents found.\n")
        continue

    print("Retrieved documents:\n")

    for i, (doc, score) in enumerate(docs_and_scores, start=1):
        page = doc.metadata.get("page", "?")

        print(f"Document {i}")
        print(f"Source : {doc.metadata.get('source','Unknown')}")
        print(f"Page   : {page}")
        print(f"Score  : {score:.4f}")
        print()

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are an AI tutor.

Use ONLY the information contained in the Context.

Never use outside knowledge.

If the answer is not completely found in the Context, reply exactly:

I don't know based on my knowledge base.

Do not invent information.
Do not answer questions outside the Context.

Always answer using:
- short paragraphs
- bullet points
- simple English
- one simple example if possible

Context:
{context}

Question:
{question}

Answer:
"""

    try:
        response = llm.invoke(prompt)

        print("\nAssistant:\n")
        print(response.content)

    except Exception as e:
        print(f"\nError: {e}")

    print("\n" + "-" * 60 + "\n")