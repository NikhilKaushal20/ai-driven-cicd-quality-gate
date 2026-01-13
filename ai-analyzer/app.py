from fastapi import FastAPI
from pydantic import BaseModel
from classifier import classify_failure

class FailureLog(BaseModel):
    log: str

app = FastAPI()

@app.post("/analyze")
def analyze_failure(data: FailureLog):
    analysis = classify_failure(data.log)
    return {
        "analysis": analysis
    }
