"""Exercise 1: Hotel agent details retrieval using vector store."""

import sys
from pathlib import Path
from util.configuration import PROJECT_ROOT

QA_PATH_EXTERNAL = PROJECT_ROOT.parent / "bookings-db" / "src"

sys.path.insert(0, str(QA_PATH_EXTERNAL))

from rag_chain import qa_chain

def preprocess_query(query: str) -> str:
    if not query or not query.strip():
        raise ValueError("Empty query")

    query = query.strip()
    return query

def format_response(result: dict) -> str:
    answer = result["result"]
    sources = result.get("source_documents", [])

    md = f"## Hotel Assistant Response\n\n{answer}\n"

    if sources:
        md += "\n---\n**Sources:**\n"
        for doc in sources:
            md += f"- {doc.metadata}\n"

    return md

def hotel_details_agent(query: str):
    query = preprocess_query(query)
    result = qa_chain.invoke(query)
    formatted_response = format_response(result)
    return formatted_response
