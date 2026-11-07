import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "EduGenie"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
EXPLANATION_BACKEND = os.getenv("EXPLANATION_BACKEND", "gemini").strip().lower()
LOCAL_EXPLANATION_MODEL = os.getenv(
    "LOCAL_EXPLANATION_MODEL", "MBZUAI/LaMini-Flan-T5-783M"
).strip()
MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", "1200"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.4"))
