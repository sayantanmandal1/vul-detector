import pytest
from app.services.analyzer import analyze_code

def test_detects_eval_usage():
    code = "def unsafe():\n    eval('print(1)')"
    result = analyze_code(code, "python")
    print(result)
    assert len(result) == 1
    assert "eval" in result[0]["description"]
    assert result[0]["line"] == 1 