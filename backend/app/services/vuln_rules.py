def get_vulnerability_patterns(language: str):
    if language == "python":
        return [
            {
                "pattern": "exec",
                "description": "Use of 'exec' is dangerous and can lead to code injection."
            },
            {
                "pattern": "eval",
                "description": "Use of 'eval' is insecure and may allow code execution."
            },
            {
                "pattern": "input(",
                "description": "Use of 'input()' without validation can lead to injection attacks."
            },
            {
                "pattern": "os.system",
                "description": "Use of 'os.system' can lead to command injection vulnerabilities."
            },
            {
                "pattern": "subprocess.call",
                "description": "Use of 'subprocess.call' without proper input validation can be dangerous."
            },
            # SQL Injection patterns
            {
                "pattern": "execute(",
                "description": "Raw SQL execution without parameterization can lead to SQL injection."
            },
            {
                "pattern": "cursor.execute(",
                "description": "Database cursor execution without proper parameterization can lead to SQL injection."
            },
            # Insecure Deserialization
            {
                "pattern": "pickle.loads",
                "description": "Use of pickle.loads can lead to insecure deserialization attacks."
            },
            {
                "pattern": "yaml.load(",
                "description": "Use of yaml.load() without Loader parameter can lead to code execution."
            },
            # Hardcoded Secrets
            {
                "pattern": "password = \"",
                "description": "Hardcoded password in source code is a security risk."
            },
            {
                "pattern": "api_key = \"",
                "description": "Hardcoded API key in source code is a security risk."
            },
            {
                "pattern": "secret = \"",
                "description": "Hardcoded secret in source code is a security risk."
            },
            {
                "pattern": "token = \"",
                "description": "Hardcoded token in source code is a security risk."
            }
        ]
    elif language == "javascript":
        return [
            {
                "pattern": "eval(",
                "description": "Use of 'eval()' is insecure and may allow code execution."
            },
            {
                "pattern": "Function(",
                "description": "Use of 'Function()' constructor can lead to code injection."
            },
            {
                "pattern": "innerHTML",
                "description": "Setting innerHTML can lead to XSS attacks if not properly sanitized."
            },
            {
                "pattern": "document.write",
                "description": "Use of 'document.write' can lead to XSS vulnerabilities."
            },
            {
                "pattern": "setTimeout(",
                "description": "Using setTimeout with user input can lead to code injection."
            },
            # SQL Injection patterns
            {
                "pattern": "query(",
                "description": "Raw database queries without parameterization can lead to SQL injection."
            },
            {
                "pattern": "execute(",
                "description": "Database execution without proper parameterization can lead to SQL injection."
            },
            # Insecure Deserialization
            {
                "pattern": "JSON.parse(",
                "description": "JSON.parse without validation can lead to prototype pollution."
            },
            # Hardcoded Secrets
            {
                "pattern": "password: \"",
                "description": "Hardcoded password in JavaScript is a security risk."
            },
            {
                "pattern": "apiKey: \"",
                "description": "Hardcoded API key in JavaScript is a security risk."
            },
            {
                "pattern": "secret: \"",
                "description": "Hardcoded secret in JavaScript is a security risk."
            }
        ]
    elif language == "java":
        return [
            {
                "pattern": "Runtime.getRuntime().exec",
                "description": "Use of Runtime.exec can lead to command injection vulnerabilities."
            },
            {
                "pattern": "ProcessBuilder",
                "description": "ProcessBuilder without input validation can be dangerous."
            },
            {
                "pattern": "Class.forName",
                "description": "Dynamic class loading can lead to security issues."
            },
            # SQL Injection patterns
            {
                "pattern": "executeQuery(",
                "description": "Raw SQL execution without prepared statements can lead to SQL injection."
            },
            {
                "pattern": "executeUpdate(",
                "description": "Raw SQL execution without prepared statements can lead to SQL injection."
            },
            # Insecure Deserialization
            {
                "pattern": "ObjectInputStream",
                "description": "Use of ObjectInputStream can lead to insecure deserialization."
            },
            # Hardcoded Secrets
            {
                "pattern": "password = \"",
                "description": "Hardcoded password in Java code is a security risk."
            },
            {
                "pattern": "apiKey = \"",
                "description": "Hardcoded API key in Java code is a security risk."
            }
        ]
    elif language in ["c", "cpp"]:
        return [
            {
                "pattern": "gets",
                "description": "Use of 'gets' is unsafe and can cause buffer overflows."
            },
            {
                "pattern": "strcpy",
                "description": "Use of 'strcpy' without bounds checking can lead to buffer overflows."
            },
            {
                "pattern": "strcat",
                "description": "Use of 'strcat' without bounds checking can lead to buffer overflows."
            },
            {
                "pattern": "sprintf",
                "description": "Use of 'sprintf' without bounds checking can lead to buffer overflows."
            },
            {
                "pattern": "scanf",
                "description": "Use of 'scanf' without format string validation can be dangerous."
            },
            {
                "pattern": "malloc",
                "description": "Use of 'malloc' without proper error checking can lead to issues."
            },
            # SQL Injection patterns (if using database libraries)
            {
                "pattern": "mysql_query",
                "description": "Raw MySQL queries without parameterization can lead to SQL injection."
            },
            {
                "pattern": "sqlite3_exec",
                "description": "Raw SQLite queries without parameterization can lead to SQL injection."
            }
        ]
    elif language == "html":
        return [
            {
                "pattern": "<script>",
                "description": "Inline <script> tags can lead to XSS vulnerabilities."
            },
            {
                "pattern": "onerror=",
                "description": "Use of onerror attribute can be exploited for XSS."
            },
            {
                "pattern": "javascript:",
                "description": "javascript: URIs can be used for XSS attacks."
            },
            {
                "pattern": "onclick=",
                "description": "Inline onclick handlers can lead to XSS vulnerabilities."
            },
            {
                "pattern": "onload=",
                "description": "Inline onload handlers can lead to XSS vulnerabilities."
            }
        ]
    elif language == "css":
        return [
            {
                "pattern": "expression(",
                "description": "CSS expression() is deprecated and can be a security risk."
            },
            {
                "pattern": "behavior:",
                "description": "CSS behavior property can be used for malicious actions in IE."
            }
        ]
    return [] 