from gemini_client import generate_text
from prompts import summary_prompt


def summarize_text(text: str) -> str:
    return generate_text(summary_prompt(text))
