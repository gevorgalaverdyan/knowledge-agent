import faiss
import json
from rag.ingest import embed_query
import logging

logger = logging.getLogger(__name__)

class FaissRetriever:
    def __init__(self, index_path: str, metadata_path: str, client):
        self.index = faiss.read_index(index_path)

        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        assert self.index.ntotal == len(self.metadata)
        self.client = client

    def search(self, query: str, top_k: int = 5):
        query_vec = embed_query(query, self.client)
        scores, indices = self.index.search(query_vec, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append({
                "score": float(score),
                **self.metadata[idx]
            })
        return results
