import json
import sys
import os
import faiss
from google import genai

from ingest import embed_query
from globals import GENAI_MODEL

# --------------------
# Setup
# --------------------

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("Missing GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
    raise SystemExit("Usage: python ask_tfsa.py \"your question\"")

query = sys.argv[1]

# --------------------
# Load FAISS + metadata
# --------------------

index = faiss.read_index("./embedding/tfsa.faiss")

with open("./embedding/tfsa_embeddings.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

assert index.ntotal == len(metadata), "FAISS index / metadata mismatch"

# --------------------
# Retrieval
# --------------------

def search(query: str, top_k: int = 5):
    query_vec = embed_query(query, client)
    faiss.normalize_L2(query_vec)

    scores, indices = index.search(query_vec, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue

        results.append({
            "score": float(score),
            **metadata[idx]
        })

    return results

# --------------------
# Prompting
# --------------------

def build_context(chunks):
    """
    Structure context so the model can cite sections.
    """
    blocks = []
    for c in chunks:
        blocks.append(
            f"[Section: {c['section']}]\n{c['text']}"
        )
    return "\n\n".join(blocks)

def ask(context: str, question: str):
    prompt = f"""
    You are a regulatory knowledge assistant specializing in Canadian federal tax guidance.

    You answer questions ONLY using the provided CRA TFSA source excerpts.
    You must not use outside knowledge or assumptions.

    Your goals are:
    - Explain rules clearly in plain language
    - Preserve the legal meaning of the CRA text
    - Cite the relevant sections explicitly
    - Avoid giving personalized tax advice

    If the sources do not contain enough information to answer the question, say:
    "I don't have enough information in the provided CRA sources to answer this."

    Do NOT:
    - Invent rules or numbers
    - Guess eligibility
    - Provide optimization strategies
    - Replace professional tax advice

    Always include a "Sources" section listing the CRA sections used.

    Context:
    {context}

    Question:
    {question}
    """

    response = client.models.generate_content(
        model=GENAI_MODEL,
        contents=prompt
    )

    print(response.text)

# --------------------
# Run
# --------------------

results = search(query)

if not results:
    print("No relevant CRA sections found.")
    sys.exit(0)

context = build_context(results)
ask(context, query)
