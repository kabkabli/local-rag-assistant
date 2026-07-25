from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

DOCS_DIR = "docs"
DB_DIR = "chroma_db"

embeddings = OllamaEmbeddings(model="nomic-embed-text")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

documents = []

for pdf in Path(DOCS_DIR).glob("*.pdf"):
    print(f"Loading {pdf.name}")
    loader = PyPDFLoader(str(pdf))
    documents.extend(loader.load())

chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")

db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=DB_DIR
)

print("Knowledge base created successfully!")