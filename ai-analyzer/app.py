from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from classifier import classify_failure
from log_parser import parse_log

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

last_result = {}

class LogPayload(BaseModel):
    log: str

@app.post("/analyze")
def analyze(payload: LogPayload):
    global last_result
    parsed = parse_log(payload.log)
    result = classify_failure(parsed)
    last_result = result
    return {"analysis": result}

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": last_result}
    )
