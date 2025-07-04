import time

from app.services.cve_mapper import map_vulnerabilities_to_cve
from app.services.fix_generator import generate_fixes
from app.services.static_analysis import run_static_analysis


def analyze_code(code: str, language: str, file: str = "unknown"):
    """
    Analyze code for vulnerabilities and return comprehensive results
    """
    start_time = time.time()
    
    # Run static analysis
    vulnerabilities = run_static_analysis(code, language, file)
    
    # Map to CVE/CWE if possible
    for vuln in vulnerabilities:
        cve_info = map_vulnerabilities_to_cve(vuln["description"], language)
        if cve_info:
            vuln["cwe"] = cve_info.get("cwe")
            vuln["cve"] = cve_info.get("cve_examples", [])
    
    # Generate fix suggestions
    for vuln in vulnerabilities:
        fixes = generate_fixes(vuln["description"], language)
        if fixes:
            vuln["suggested_fix"] = fixes[0] if fixes else None
    
    analysis_time = time.time() - start_time
    return vulnerabilities, analysis_time 