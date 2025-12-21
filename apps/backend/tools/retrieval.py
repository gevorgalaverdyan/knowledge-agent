from typing import List

from core.setup import retriever
from schemas.chat import Section

def find_relevant_sections(query: str, top_k: int = 5) -> List[Section]:
    """
    Returns relevant TFSA sections using FAISS.
    """
    results = retriever.search(query, top_k)

    filtered = []
    for r in results:
        section = Section(
            id=r["id"],
            section=r["section"],
            topic=r.get("topic", ""),
            text=r["text"],
            document=r.get("document", "CRA"),
            jurisdiction=r.get("jurisdiction", "Canada"),
            year=r.get("year", 2025)
        )
        filtered.append(section)
    
    return filtered
