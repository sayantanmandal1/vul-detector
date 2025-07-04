import time
from app.services.static_analysis import run_static_analysis
from app.services.cve_mapper import map_to_cve_cwe
from app.services.fix_generator import suggest_fix

def analyze_code(code: str, language: str, file: str = "snippet"):
    start_time = time.time()
    
    vulns = run_static_analysis(code, language, file)
    for vuln in vulns:
        cwe, cve = map_to_cve_cwe(vuln["description"])
        vuln["cwe"] = cwe
        vuln["cve"] = cve
        vuln["suggested_fix"] = suggest_fix(code, vuln["description"])
        vuln["file"] = vuln.get("file", file)
        vuln["language"] = vuln.get("language", language)
    
    analysis_time = time.time() - start_time
    return vulns, analysis_time 