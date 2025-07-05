import pytest
from app.services.analyzer import analyze_code

def test_detects_eval_usage():
    code = "def unsafe():\n    eval('print(1)')"
    result = analyze_code(code, "python")
    print(result)
    vulnerabilities, _ = result  # Unpack the tuple
    assert len(vulnerabilities) == 1
    assert "eval" in vulnerabilities[0]["description"]
    assert vulnerabilities[0]["line"] == 2  # eval is on line 2 