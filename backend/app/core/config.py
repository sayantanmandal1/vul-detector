import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "LLM Vulnerability Detector"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY") or ""
    MODEL_NAME: str = "gpt-3.5-turbo"  # used only for mitigation suggestion

settings = Settings()