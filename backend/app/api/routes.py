from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
from typing import Dict, Any
import io
import json
from datetime import datetime

from ..models.schemas import (
    CodeAnalysisRequest, 
    RepoAnalysisRequest, 
    AnalysisResult, 
    ReportRequest,
    PDFResponse,
    ReportResponse,
    Vulnerability
)
from ..services.analyzer import analyze_code
from ..services.github_scanner import analyze_repository_files
from ..services.report_generator import generate_report

router = APIRouter()

@router.post("/analyze/code", response_model=AnalysisResult)
async def analyze_code_endpoint(request: CodeAnalysisRequest):
    """Analyze a single code snippet for vulnerabilities."""
    try:
        vulnerabilities = analyze_code(request.code, request.language, file="snippet")
        # Convert to Vulnerability models
        vulnerabilities = [Vulnerability(**v) for v in vulnerabilities]
        return AnalysisResult(
            repository_url="",
            total_files_analyzed=1,
            total_vulnerabilities=len(vulnerabilities),
            vulnerabilities=vulnerabilities,
            analysis_time=0,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/repo", response_model=AnalysisResult)
async def analyze_repo_endpoint(request: RepoAnalysisRequest):
    """Analyze a GitHub repository for vulnerabilities."""
    try:
        result = analyze_repository_files(request.repository_url)
        vulnerabilities = result.get("vulnerabilities", [])
        vulnerabilities = [Vulnerability(**v) for v in vulnerabilities]
        return AnalysisResult(
            repository_url=request.repository_url,
            total_files_analyzed=result.get("total_files_analyzed", 0),
            total_vulnerabilities=len(vulnerabilities),
            vulnerabilities=vulnerabilities,
            analysis_time=result.get("analysis_time", 0),
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/report")
async def generate_report_endpoint(request: ReportRequest):
    """Generate a report in the specified format."""
    try:
        # Convert Pydantic model to dict for report generation
        analysis_dict = request.analysis_result.dict()
        
        # Convert vulnerability models to dicts
        vulnerabilities = []
        for vuln in analysis_dict.get("vulnerabilities", []):
            if hasattr(vuln, 'dict'):
                vulnerabilities.append(vuln.dict())
            else:
                vulnerabilities.append(vuln)
        analysis_dict["vulnerabilities"] = vulnerabilities
        
        if request.format == "pdf":
            # Handle PDF generation specially
            pdf_content = generate_report(analysis_dict, "pdf")
            
            # Create a proper PDF response
            filename = f"vulnerability_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            # Ensure pdf_content is bytes
            if isinstance(pdf_content, str):
                pdf_content = pdf_content.encode('utf-8')
            elif isinstance(pdf_content, bytearray):
                pdf_content = bytes(pdf_content)
                
            return StreamingResponse(
                io.BytesIO(pdf_content),
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename={filename}",
                    "Content-Type": "application/pdf"
                }
            )
        else:
            # Handle other formats
            content = generate_report(analysis_dict, request.format)
            filename = f"vulnerability_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{request.format}"
            
            content_type_map = {
                "json": "application/json",
                "text": "text/plain",
                "html": "text/html"
            }
            
            return Response(
                content=content,
                media_type=content_type_map.get(request.format, "text/plain"),
                headers={
                    "Content-Disposition": f"attachment; filename={filename}"
                }
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
