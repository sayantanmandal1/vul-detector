from app.services.tree_sitter_loader import LANGUAGE_MAP
from app.services.vuln_rules import get_vulnerability_patterns
from tree_sitter import Parser


def run_static_analysis(code: str, language: str, file: str = "unknown"):
    # For HTML/CSS, use simple text matching (no Tree-sitter needed)
    if language in ["html", "css"]:
        patterns = get_vulnerability_patterns(language)
        vulnerabilities = []
        seen_patterns = set()  # Track which patterns have been reported
        
        lines = code.split('\n')
        for line_num, line in enumerate(lines, 1):
            for pattern in patterns:
                if pattern["pattern"] in line and pattern["pattern"] not in seen_patterns:
                    vulnerabilities.append({
                        "file": file,
                        "line": line_num,
                        "language": language,
                        "description": pattern["description"]
                    })
                    seen_patterns.add(pattern["pattern"])
        
        return vulnerabilities
    
    # For programming languages, use Tree-sitter
    if language not in LANGUAGE_MAP or LANGUAGE_MAP[language] is None:
        # Fallback to simple text matching if tree-sitter is not available
        patterns = get_vulnerability_patterns(language)
        vulnerabilities = []
        seen_patterns = set()
        
        lines = code.split('\n')
        for line_num, line in enumerate(lines, 1):
            for pattern in patterns:
                if pattern["pattern"] in line and pattern["pattern"] not in seen_patterns:
                    vulnerabilities.append({
                        "file": file,
                        "line": line_num,
                        "language": language,
                        "description": pattern["description"]
                    })
                    seen_patterns.add(pattern["pattern"])
        
        return vulnerabilities

    try:
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
                        "file": file,
                        "line": node.start_point[0] + 1,
                        "language": language,
                        "description": pattern["description"]
                    })
                    seen_patterns.add(pattern["pattern"])
            for child in node.children:
                visit(child)

        visit(root_node)
        return vulnerabilities
    except Exception as e:
        # Fallback to simple text matching if tree-sitter fails
        print(f"Warning: Tree-sitter analysis failed for {language}: {e}")
        patterns = get_vulnerability_patterns(language)
        vulnerabilities = []
        seen_patterns = set()
        
        lines = code.split('\n')
        for line_num, line in enumerate(lines, 1):
            for pattern in patterns:
                if pattern["pattern"] in line and pattern["pattern"] not in seen_patterns:
                    vulnerabilities.append({
                        "file": file,
                        "line": line_num,
                        "language": language,
                        "description": pattern["description"]
                    })
                    seen_patterns.add(pattern["pattern"])
        
        return vulnerabilities 