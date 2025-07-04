from app.services.tree_sitter_loader import LANGUAGE_MAP
from app.services.vuln_rules import get_vulnerability_patterns
from tree_sitter import Parser

def run_static_analysis(code: str, language: str):
    if language not in LANGUAGE_MAP:
        return [{"line": 1, "description": f"Language '{language}' not supported."}]

    parser = Parser()
    parser.set_language(LANGUAGE_MAP[language])
    tree = parser.parse(bytes(code, "utf8"))
    root_node = tree.root_node

    patterns = get_vulnerability_patterns(language)
    vulnerabilities = []
    seen_patterns = set()  # Track which patterns have been reported

    def visit(node):
        text = code[node.start_byte:node.end_byte]
        for pattern in patterns:
            if pattern["pattern"] in text and pattern["pattern"] not in seen_patterns:
                vulnerabilities.append({
                    "line": node.start_point[0] + 1,
                    "description": pattern["description"]
                })
                seen_patterns.add(pattern["pattern"])
        for child in node.children:
            visit(child)

    visit(root_node)
    return vulnerabilities 