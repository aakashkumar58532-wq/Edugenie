from gemini_client import generate_text
from prompts import qa_prompt


def answer_question(question: str) -> str:
    return generate_text(qa_prompt(question))
