"""
CVE/CWE mapping for vulnerabilities
"""

def map_vulnerabilities_to_cve(description: str, language: str):
    """
    Map vulnerability description to CVE/CWE information
    """
    description_lower = description.lower()
    if "eval" in description_lower:
        return {
            "cwe": "CWE-78",
            "cve_examples": ["CVE-2021-44228", "CVE-2020-1472"],
            "description": "OS Command Injection"
        }
    elif "sql injection" in description_lower or "execute(" in description_lower:
        return {
            "cwe": "CWE-89",
            "cve_examples": ["CVE-2021-44228", "CVE-2020-1472"],
            "description": "SQL Injection"
        }
    elif "xss" in description_lower or "innerhtml" in description_lower:
        return {
            "cwe": "CWE-79",
            "cve_examples": ["CVE-2021-44228", "CVE-2020-1472"],
            "description": "Cross-site Scripting"
        }
    elif "buffer overflow" in description_lower or "strcpy" in description_lower:
        return {
            "cwe": "CWE-119",
            "cve_examples": ["CVE-2021-44228", "CVE-2020-1472"],
            "description": "Buffer Overflow"
        }
    elif "hardcoded" in description_lower or "password" in description_lower:
        return {
            "cwe": "CWE-259",
            "cve_examples": ["CVE-2021-44228", "CVE-2020-1472"],
            "description": "Use of Hard-coded Password"
        }
    elif "deserialization" in description_lower or "pickle" in description_lower:
        return {
            "cwe": "CWE-502",
            "cve_examples": ["CVE-2021-44228", "CVE-2020-1472"],
            "description": "Deserialization of Untrusted Data"
        }
    return None 