SYSTEM = """You are EduGenie, a friendly educational assistant.\n\nRules:\n- Explain accurately and clearly for a student.\n- Prefer simple language and short sections.\n- Do not invent sources or facts.\n- If the user's request is ambiguous, state the assumption briefly.\n"""


def qa_prompt(question: str) -> str:
    return f"""{SYSTEM}\nAnswer the following academic/general-knowledge question. Give the direct answer first, then a concise explanation.\n\nQuestion:\n{question}"""


def explain_prompt(topic: str) -> str:
    return f"""{SYSTEM}\nExplain this concept to a beginner. Use: 1) Meaning, 2) Simple explanation, 3) Example, 4) Key points. Keep it easy to revise.\n\nTopic:\n{topic}"""


def summary_prompt(text: str) -> str:
    return f"""{SYSTEM}\nSummarize the following educational text. Preserve the important ideas, names, facts, relationships, and conclusions. Use a short heading and bullet points where useful. Do not add information that is absent from the text.\n\nText:\n{text}"""


def learning_path_prompt(topic: str) -> str:
    return f"""{SYSTEM}\nCreate a personalized learning path for the topic below. Organize it from Beginner to Intermediate to Advanced. Include suggested timeline, prerequisites, practice activities, and resource types (videos, documentation, articles, books). Do not fabricate specific URLs.\n\nTopic:\n{topic}"""


def quiz_prompt(text: str) -> str:
    return f"""{SYSTEM}\nGenerate exactly 3 multiple-choice questions from the provided topic/text. Each question must have exactly 4 options and exactly one correct answer. Return ONLY valid JSON with this shape:\n{{\n  \"questions\": [\n    {{\"question\": \"...\", \"options\": [\"A\", \"B\", \"C\", \"D\"], \"answer\": \"A\", \"explanation\": \"...\"}}\n  ]\n}}\nThe answer field must exactly match one option.\n\nSource/topic:\n{text}"""
