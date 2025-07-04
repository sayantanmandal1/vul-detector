from pydantic import BaseModel
from typing import List, Optional

class Vulnerability(BaseModel):
    line: int
    description: str
    cwe: Optional[str]
    cve: Optional[str]
    suggested_fix: Optional[str]

class AnalyzeRequest(BaseModel):
    code: str
    language: str  # e.g., "python", "c", "cpp", "java"

class AnalyzeResponse(BaseModel):
    vulnerabilities: List[Vulnerability] 