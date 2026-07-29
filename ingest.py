from pathlib import Path
import shutil

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# ------------------------------------
# Configuration
# ------------------------------------
DOCS_DIR = "docs"
DB_DIR = "chroma_db"

# Reset database (simple for now, later we’ll switch to incremental ingestion)
if Path(DB_DIR).exists():
    shutil.rmtree(DB_DIR)

embeddings = OllamaEmbeddings(model="nomic-embed-text")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

documents = []

# Load PDFs and TXT notes
for file in Path(DOCS_DIR).glob("*"):
    if file.suffix == ".pdf":
        print(f"Loading {file.name}")
        loader = PyPDFLoader(str(file))
    elif file.suffix == ".txt":
        print(f"Loading {file.name}")
        loader = TextLoader(str(file))
    else:
        continue
    documents.extend(loader.load())

print(f"\nLoaded {len(documents)} documents")

chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=DB_DIR,
    collection_metadata={"hnsw:space": "cosine"},
)

print("\n✅ Knowledge base created successfully!")
