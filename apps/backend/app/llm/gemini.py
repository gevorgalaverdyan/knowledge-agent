from google import genai

from app.core.config import get_settings

def get_gemini_client():
    api_key = get_settings().GEMINI_API_KEY
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY")
    return genai.Client(api_key=api_key)
