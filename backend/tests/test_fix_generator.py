from app.services.fix_generator import generate_fixes

def test_generate_fix_safely():
    vuln = {
        "line": 1,
        "description": "Use of 'eval' is insecure and may allow code execution.",
        "code": "def unsafe():\n    eval('print(1)')"
    }

    fixes = generate_fixes(vuln["description"], "python")
    assert len(fixes) > 0
    assert any("literal_eval" in fix.lower() or "safe" in fix.lower() for fix in fixes) 