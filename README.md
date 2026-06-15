# ⚡ ContraDoc AI
### Multi-document Contradiction Finder using RAG

> "Don't just answer questions — find where your sources disagree."

# What it does
Upload multiple PDFs and ask a question. ContraDoc AI finds 
where documents **contradict each other** using RAG pipeline.

## Tech Stack
- **LangChain** — RAG pipeline
- **ChromaDB** — Vector database
- **HuggingFace** — Embeddings 
- **Groq LLaMA 3.3** — LLM inference 
- **FastAPI** — REST API backend
- **Streamlit** — Frontend UI

## How to Run
```bash
# Install dependencies
pip install -r requirements.txt

# Start backend
uvicorn app.api:app --host 0.0.0.0 --port 8000

# Start frontend
streamlit run ui/streamlit_app.py
```

# Use Cases
- Legal document analysis
- Medical research comparison  
- Academic paper contradiction detection
