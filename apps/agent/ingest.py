import os
import json
import faiss
import numpy as np
from globals import EMBEDDING_MODEL
from utils import chunk_text

def embed_batch(texts: list[str], client):
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts
    )
    return [e.values for e in response.embeddings]

def embed_query(query: str, client):
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query
    )
    vector = np.array(
        [response.embeddings[0].values],
        dtype="float32"
    )

    faiss.normalize_L2(vector)
    return vector
    
def ingest(client):
    knowledge_dir = os.path.join(os.path.dirname(__file__), "knowledge")
    if not os.path.isdir(knowledge_dir):
        raise SystemExit(f"Missing knowledge folder at {knowledge_dir}")

    records = []
    texts_to_embed = []

    for filename in sorted(os.listdir(knowledge_dir)):
        path = os.path.join(knowledge_dir, filename)
        if not filename.lower().endswith(".txt"):
            continue

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            record = {
                "id": f"{filename}_{i:03}",
                "section": chunk["section"],
                "topic": chunk["section"].lower().replace(" ", "_"),
                "text": chunk["text"],
                "source": "CRA",
                "document": "RC4466 - TFSA Guide",
                "jurisdiction": "Canada",
                "year": 2025
            }

            records.append(record)
            texts_to_embed.append(chunk["text"])

    embeddings = embed_batch(texts_to_embed, client)

    for record, vector in zip(records, embeddings):
        record["embedding"] = vector

    with open("./embedding/tfsa_embeddings.json", "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    print(f"Embedded and indexed {len(records)} chunks")

    vectors = np.array(
        [r["embedding"] for r in records],
        dtype="float32"
    )

    dimension = vectors.shape[1]

    index = faiss.IndexFlatIP(dimension)

    faiss.normalize_L2(vectors)

    index.add(vectors)

    print(f"FAISS index built with {index.ntotal} vectors")

    faiss.write_index(index, "./embedding/tfsa.faiss")


