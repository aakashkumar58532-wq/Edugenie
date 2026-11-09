
import json
import re

from gemini_client import generate_text
from prompts import quiz_prompt


def generate_quiz(text: str):
    if not text or not text.strip():
        raise ValueError("Please provide a topic or text to generate a quiz.")

    response = generate_text(quiz_prompt(text))

    # Extract JSON if Gemini includes markdown code fences
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", response.strip())

    try:
        quiz_data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError("Gemini returned invalid quiz JSON.") from exc

    questions = quiz_data.get("questions")
    if not isinstance(questions, list):
        raise ValueError("Quiz response does not contain a questions list.")

    for question in questions:
        if (
            not isinstance(question, dict)
            or not isinstance(question.get("options"), list)
            or len(question["options"]) != 4
            or question.get("answer") not in question["options"]
        ):
            raise ValueError("Quiz response has an invalid question format.")

    return quiz_data
