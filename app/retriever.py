from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from app.ingest import load_documents, chunk_documents

CHROMA_PATH = "chroma_db"

def build_vectorstore():
    docs = load_documents()
    chunks = chunk_documents(docs)
    
    # Free embeddings — no API key needed
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    
    vectorstore = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=CHROMA_PATH
    )
    
    print("✅ Vector DB built!")
    return vectorstore

def get_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )