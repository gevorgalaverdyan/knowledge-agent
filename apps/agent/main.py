from google import genai
import os

from ingest import ingest
from globals import GENAI_MODEL

api_key = os.getenv("GEMINI_API_KEY")
print(f"Using API Key: {api_key}")
client = genai.Client(api_key=api_key)

# response = client.models.generate_content(
#     model=GENAI_MODEL, contents="Explain how AI works in a few words"
# )

ingest(client)