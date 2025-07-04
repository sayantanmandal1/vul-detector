from app.services.fix_generator import suggest_fix as generate_fix

def test_generate_fix_safely():
    vuln = {
        "line": 1,
        "description": "Use of 'eval' is insecure and may allow code execution.",
        "code": "def unsafe():\n    eval('print(1)')"
    }

    fix = generate_fix(vuln["code"], vuln["description"])
    assert "safe" in fix.lower() or "avoid" in fix.lower() or "literal_eval" in fix.lower() 