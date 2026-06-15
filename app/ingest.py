from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def load_documents(pdf_folder="data/"):
    all_docs = []
    
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(pdf_folder, filename))
            pages = loader.load()
            
            # Tagging each chunk with source filename
            for page in pages:
                page.metadata["source"] = filename
            
            all_docs.extend(pages)
    
    return all_docs

def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)
    return chunks