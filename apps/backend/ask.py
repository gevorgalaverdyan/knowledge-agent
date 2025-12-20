import json
import sys
import os
import faiss
from google import genai

from ingest import embed_query

# --------------------
# Setup
# --------------------

api_key = os.getenv("GEMINI_API_KEY")
GENAI_MODEL = os.getenv("GEMINI_GENAI_MODEL", "gemini-3-flash-preview")
if not api_key:
    raise RuntimeError("Missing GEMINI_API_KEY")
if not GENAI_MODEL:
    raise RuntimeError("Missing GEMINI_GENAI_MODEL")

client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
    raise SystemExit("Usage: python ask_tfsa.py \"your question\"")

user_query = sys.argv[1]

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

def search(search_query: str, top_k: int = 5):
    query_vec = embed_query(search_query, client)
    faiss.normalize_L2(query_vec)

    scores, indices = index.search(query_vec, top_k)

    search_results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue

        search_results.append({
            "score": float(score),
            **metadata[idx]
        })

    return search_results

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

def ask(context_text: str, question: str):
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
    {context_text}

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

RESULTS = search(user_query)

if not RESULTS:
    print("No relevant CRA sections found.")
    sys.exit(0)

CONTEXT = build_context(RESULTS)
ask(CONTEXT, user_query)
