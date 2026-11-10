
import logging
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import TaskRequest
from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie - Gemini Powered Learning Assistant",
    version="1.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def run_ai(task_name, function, text):
    try:
        result = function(text)
        return {"result": result}

    except Exception as exc:
        logger.exception("%s failed", task_name)

        raise HTTPException(
            status_code=502,
            detail=f"{task_name} failed: {str(exc)}"
        ) from exc


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
async def qa(payload: TaskRequest):
    return run_ai("Question and Answer", answer_question, payload.text)


@app.post("/explain")
async def explain(payload: TaskRequest):
    return run_ai("Explanation", explain_topic, payload.text)


@app.post("/quiz")
async def quiz(payload: TaskRequest):
    return run_ai("Quiz", generate_quiz, payload.text)


@app.post("/summarize")
async def summarize(payload: TaskRequest):
    return run_ai("Summary", summarize_text, payload.text)


@app.post("/learn/recommendations")
async def learning_recommendations(payload: TaskRequest):
    return run_ai(
        "Learning Recommendations",
        get_learning_recommendations,
        payload.text
    )
