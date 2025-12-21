import os

class Settings:
    GENAI_MODEL = os.getenv("GEMINI_GENAI_MODEL", "gemini-3-flash-preview")

settings = Settings()
