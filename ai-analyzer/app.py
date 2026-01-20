from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory state for dashboard display
LAST_RESULT = {
    "status": "UNSTABLE",
    "failure_type": "TEST_FAILURE",
    "recommendation": "Fix assertion or update expected value"
}

class FailureLog(BaseModel):
    log: str

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "status": LAST_RESULT["status"],
            "failure_type": LAST_RESULT["failure_type"],
            "recommendation": LAST_RESULT["recommendation"],
            "status_class": LAST_RESULT["status"]
        }
    )

@app.post("/analyze")
def analyze_failure(data: FailureLog):
    log = data.log

    # ✅ Simple AI logic (rule-based) — replace with OpenAI later if needed
    if "AssertionError" in log:
        LAST_RESULT["status"] = "UNSTABLE"
        LAST_RESULT["failure_type"] = "TEST_FAILURE"
        LAST_RESULT["recommendation"] = "Fix assertion or update expected value"
    elif "Timeout" in log or "Connection refused" in log:
        LAST_RESULT["status"] = "FAILURE"
        LAST_RESULT["failure_type"] = "ENVIRONMENT_ISSUE"
        LAST_RESULT["recommendation"] = "Check network/browser/driver/infra"
    else:
        LAST_RESULT["status"] = "FAILURE"
        LAST_RESULT["failure_type"] = "APPLICATION_BUG"
        LAST_RESULT["recommendation"] = "Create defect and block deployment"

    return {"analysis": LAST_RESULT}
