from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

class Vulnerability(BaseModel):
    file: str
    line: int
    language: str
    description: str
    cwe: Optional[str] = None
    cve: Optional[List[str]] = None
    suggested_fix: Optional[str] = None
    severity: Optional[str] = None

class AnalysisResult(BaseModel):
    repository_url: str
    total_files_analyzed: int
    total_vulnerabilities: int
    vulnerabilities: List[Vulnerability]
    analysis_time: Optional[float] = None
    timestamp: Optional[datetime] = None

class CodeAnalysisRequest(BaseModel):
    code: str
    language: str

class RepoAnalysisRequest(BaseModel):
    repository_url: str
    branch: Optional[str] = "main"

class ReportRequest(BaseModel):
    analysis_result: AnalysisResult
    format: str = "json"  # json, text, html, pdf

class PDFResponse(BaseModel):
    content: bytes
    filename: str
    content_type: str = "application/pdf"

class ReportResponse(BaseModel):
    content: Union[str, bytes]
    filename: str
    content_type: str
    format: str 