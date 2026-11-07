from functools import lru_cache

from config import EXPLANATION_BACKEND, LOCAL_EXPLANATION_MODEL
from gemini_client import generate_text
from prompts import explain_prompt


@lru_cache(maxsize=1)
def _local_pipeline():
    from transformers import pipeline

    return pipeline("text2text-generation", model=LOCAL_EXPLANATION_MODEL)


def _local_explain(topic: str) -> str:
    generator = _local_pipeline()
    prompt = (
        "Explain the following topic to a beginner in simple language. "
        "Give meaning, explanation, example and key points. Topic: " + topic
    )
    result = generator(prompt, max_new_tokens=300, do_sample=False)
    return result[0]["generated_text"].strip()


def explain_topic(topic: str) -> str:
    if EXPLANATION_BACKEND == "local":
        try:
            return _local_explain(topic)
        except Exception:
            # Keep the app usable if the optional local model cannot load.
            return generate_text(explain_prompt(topic))
    return generate_text(explain_prompt(topic))
