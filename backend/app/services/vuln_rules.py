"""
Vulnerability patterns and rules for static analysis
"""

def get_vulnerability_patterns(language: str):
    """Get vulnerability patterns for a specific language"""
    
    patterns = {
        "python": [
            {"pattern": "eval(", "description": "Use of 'eval' is insecure and may allow code execution vulnerabilities."},
            {"pattern": "exec(", "description": "Use of 'exec' is insecure and may allow arbitrary code execution."},
            {"pattern": "input(", "description": "Use of 'input' without validation may lead to injection attacks."},
            {"pattern": "os.system(", "description": "Use of 'os.system' may lead to command injection vulnerabilities."},
            {"pattern": "subprocess.call(", "description": "Use of 'subprocess.call' without proper validation may be unsafe."},
            {"pattern": "pickle.loads(", "description": "Use of 'pickle.loads' may lead to arbitrary code execution."},
            {"pattern": "yaml.load(", "description": "Use of 'yaml.load' without Loader parameter may be unsafe."},
            {"pattern": "password = ", "description": "Hardcoded passwords in code are a security risk."},
            {"pattern": "secret = ", "description": "Hardcoded secrets in code are a security risk."},
            {"pattern": "api_key = ", "description": "Hardcoded API keys in code are a security risk."}
        ],
        "javascript": [
            {"pattern": "eval(", "description": "Use of 'eval' is insecure and may allow code execution vulnerabilities."},
            {"pattern": "Function(", "description": "Use of 'Function' constructor may lead to code injection."},
            {"pattern": "innerHTML = ", "description": "Direct assignment to innerHTML may lead to XSS vulnerabilities."},
            {"pattern": "document.write(", "description": "Use of 'document.write' may lead to XSS vulnerabilities."},
            {"pattern": "localStorage.setItem(", "description": "Storing sensitive data in localStorage may be insecure."},
            {"pattern": "sessionStorage.setItem(", "description": "Storing sensitive data in sessionStorage may be insecure."},
            {"pattern": "password: ", "description": "Hardcoded passwords in code are a security risk."},
            {"pattern": "apiKey: ", "description": "Hardcoded API keys in code are a security risk."},
            {"pattern": "secret: ", "description": "Hardcoded secrets in code are a security risk."},
            {"pattern": "token: ", "description": "Hardcoded tokens in code are a security risk."}
        ],
        "java": [
            {"pattern": "Runtime.getRuntime().exec(", "description": "Use of 'Runtime.exec' may lead to command injection vulnerabilities."},
            {"pattern": "ProcessBuilder(", "description": "Use of 'ProcessBuilder' without validation may be unsafe."},
            {"pattern": "ObjectInputStream(", "description": "Use of 'ObjectInputStream' may lead to deserialization vulnerabilities."},
            {"pattern": "XMLDecoder(", "description": "Use of 'XMLDecoder' may lead to arbitrary code execution."},
            {"pattern": "password = ", "description": "Hardcoded passwords in code are a security risk."},
            {"pattern": "secret = ", "description": "Hardcoded secrets in code are a security risk."},
            {"pattern": "apiKey = ", "description": "Hardcoded API keys in code are a security risk."},
            {"pattern": "token = ", "description": "Hardcoded tokens in code are a security risk."},
            {"pattern": "String password = ", "description": "Hardcoded passwords in code are a security risk."},
            {"pattern": "String secret = ", "description": "Hardcoded secrets in code are a security risk."}
        ],
        "c": [
            {"pattern": "strcpy(", "description": "Use of 'strcpy' may lead to buffer overflow vulnerabilities."},
            {"pattern": "strcat(", "description": "Use of 'strcat' may lead to buffer overflow vulnerabilities."},
            {"pattern": "sprintf(", "description": "Use of 'sprintf' may lead to buffer overflow vulnerabilities."},
            {"pattern": "gets(", "description": "Use of 'gets' is unsafe and may lead to buffer overflow."},
            {"pattern": "scanf(", "description": "Use of 'scanf' without proper format validation may be unsafe."},
            {"pattern": "system(", "description": "Use of 'system' may lead to command injection vulnerabilities."},
            {"pattern": "popen(", "description": "Use of 'popen' may lead to command injection vulnerabilities."},
            {"pattern": "malloc(", "description": "Use of 'malloc' without proper bounds checking may be unsafe."},
            {"pattern": "free(", "description": "Use of 'free' without proper memory management may lead to vulnerabilities."},
            {"pattern": "memcpy(", "description": "Use of 'memcpy' without proper bounds checking may lead to buffer overflow."}
        ],
        "cpp": [
            {"pattern": "strcpy(", "description": "Use of 'strcpy' may lead to buffer overflow vulnerabilities."},
            {"pattern": "strcat(", "description": "Use of 'strcat' may lead to buffer overflow vulnerabilities."},
            {"pattern": "sprintf(", "description": "Use of 'sprintf' may lead to buffer overflow vulnerabilities."},
            {"pattern": "gets(", "description": "Use of 'gets' is unsafe and may lead to buffer overflow."},
            {"pattern": "scanf(", "description": "Use of 'scanf' without proper format validation may be unsafe."},
            {"pattern": "system(", "description": "Use of 'system' may lead to command injection vulnerabilities."},
            {"pattern": "popen(", "description": "Use of 'popen' may lead to command injection vulnerabilities."},
            {"pattern": "new ", "description": "Use of 'new' without proper memory management may lead to vulnerabilities."},
            {"pattern": "delete ", "description": "Use of 'delete' without proper memory management may lead to vulnerabilities."},
            {"pattern": "memcpy(", "description": "Use of 'memcpy' without proper bounds checking may lead to buffer overflow."}
        ],
        "html": [
            {"pattern": "onclick=", "description": "Inline event handlers may lead to XSS vulnerabilities."},
            {"pattern": "onload=", "description": "Inline event handlers may lead to XSS vulnerabilities."},
            {"pattern": "onerror=", "description": "Inline event handlers may lead to XSS vulnerabilities."},
            {"pattern": "javascript:", "description": "JavaScript protocol in URLs may lead to XSS vulnerabilities."},
            {"pattern": "data:text/html", "description": "Data URLs may be used for XSS attacks."}
        ],
        "css": [
            {"pattern": "expression(", "description": "CSS expressions may lead to code execution vulnerabilities."},
            {"pattern": "url(javascript:", "description": "JavaScript URLs in CSS may lead to XSS vulnerabilities."},
            {"pattern": "behavior:", "description": "CSS behaviors may lead to security vulnerabilities."}
        ]
    }
    
    return patterns.get(language.lower(), []) 