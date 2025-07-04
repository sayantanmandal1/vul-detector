import json
from pathlib import Path

with open(Path(__file__).parent.parent / "data/cwe_mappings.json") as f:
    CWE_DB = json.load(f)

def map_to_cve_cwe(desc: str):
    for item in CWE_DB:
        if item["keyword"].lower() in desc.lower():
            return item["cwe"], item["cve"]
    return None, None 