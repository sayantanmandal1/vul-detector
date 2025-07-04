from fastapi import APIRouter
from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.analyzer import analyze_code

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    result = analyze_code(request.code, request.language)
    return {"vulnerabilities": result} 

@router.get("/ping")
def ping():
    return {"status": "ok"}

@router.get("/version")
def version():
    return {"version": "1.0.0"}
