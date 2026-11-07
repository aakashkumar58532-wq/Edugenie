from gemini_client import generate_text
from prompts import learning_path_prompt


def get_learning_recommendations(topic: str) -> str:
    return generate_text(learning_path_prompt(topic))
