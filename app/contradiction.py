from app.retriever import get_vectorstore
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

def find_contradictions(query: str, top_k: int = 6):
    
    # Step 1: Get relevant chunks from vector DB
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search(query, k=top_k)
    
    # Step 2: Group chunks by source document
    doc_chunks = defaultdict(list)
    for chunk in results:
        source = chunk.metadata.get("source", "unknown")
        doc_chunks[source].append(chunk.page_content)
    
    # Step 3: If only 1 document found
    if len(doc_chunks) < 2:
        return {
            "query": query,
            "contradiction_found": False,
            "message": "Need chunks from at least 2 documents to compare.",
            "sources_used": list(doc_chunks.keys()),
            "analysis": "Not enough sources to compare."
        }
    
    # Step 4: Build sources text
    sources_text = ""
    for source, chunks in doc_chunks.items():
        combined = " ".join(chunks)
        sources_text += f"\n\n📄 SOURCE: {source}\n{combined}"
    
    # Step 5: Givingg prompt
    prompt = PromptTemplate(
        input_variables=["query", "sources"],
        template="""
You are an expert document analyst.

User Question: {query}

Below are excerpts from multiple documents:
{sources}

Your task:
1. Identify if any documents CONTRADICT each other on this topic
2. If contradiction exists, clearly explain WHAT contradicts WHAT
3. Quote the specific conflicting parts
4. Give a final verdict

Format your response as:
CONTRADICTION FOUND: Yes/No
EXPLANATION: ...
DOCUMENT 1 SAYS: ...
DOCUMENT 2 SAYS: ...
VERDICT: ...
"""
    )
    
    # Step 6: Groq LLM (free!)
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    
    chain = prompt | llm
    response = chain.invoke({
        "query": query,
        "sources": sources_text
    })
    
    return {
        "query": query,
        "contradiction_found": True,
        "analysis": response.content,
        "sources_used": list(doc_chunks.keys())
    }