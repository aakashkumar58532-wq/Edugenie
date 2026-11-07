from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import TaskRequest
from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="EduGenie - Gemini Powered Learning Assistant", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


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
    return {"result": answer_question(payload.text)}


@app.post("/explain")
async def explain(payload: TaskRequest):
    return {"result": explain_topic(payload.text)}


@app.post("/quiz")
async def quiz(payload: TaskRequest):
    return {"result": generate_quiz(payload.text)}


@app.post("/summarize")
async def summarize(payload: TaskRequest):
    return {"result": summarize_text(payload.text)}


@app.post("/learn/recommendations")
async def learning_recommendations(payload: TaskRequest):
    return {"result": get_learning_recommendations(payload.text)}
