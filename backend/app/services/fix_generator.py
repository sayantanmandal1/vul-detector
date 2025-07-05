"""
Fix suggestions generator for vulnerabilities
"""

def generate_fixes(description: str, language: str):
    """
    Generate fix suggestions for vulnerabilities
    """
    description_lower = description.lower()
    
    if "eval" in description_lower:
        if language == "python":
            return [
                "Replace eval() with ast.literal_eval() for safe evaluation",
                "Use json.loads() for JSON parsing",
                "Implement proper input validation and sanitization"
            ]
        elif language == "javascript":
            return [
                "Replace eval() with JSON.parse() for JSON parsing",
                "Use Function constructor with proper validation",
                "Implement proper input validation and sanitization"
            ]
    
    elif "sql injection" in description_lower or "execute(" in description_lower:
        if language == "python":
            return [
                "Use parameterized queries with placeholders",
                "Use ORM libraries like SQLAlchemy",
                "Implement proper input validation and sanitization"
            ]
        elif language == "javascript":
            return [
                "Use parameterized queries with placeholders",
                "Use ORM libraries like Sequelize",
                "Implement proper input validation and sanitization"
            ]
        elif language == "java":
            return [
                "Use PreparedStatement instead of raw SQL",
                "Use JPA/Hibernate for database operations",
                "Implement proper input validation and sanitization"
            ]
    
    elif "xss" in description_lower or "innerhtml" in description_lower:
        if language == "javascript":
            return [
                "Use textContent instead of innerHTML",
                "Use DOMPurify for HTML sanitization",
                "Implement proper output encoding"
            ]
        elif language == "html":
            return [
                "Use proper HTML encoding",
                "Avoid inline event handlers",
                "Use Content Security Policy (CSP)"
            ]
    
    elif "buffer overflow" in description_lower or "strcpy" in description_lower:
        if language in ["c", "cpp"]:
            return [
                "Use strncpy() with proper bounds checking",
                "Use strlcpy() if available",
                "Implement proper buffer size validation"
            ]
    
    elif "hardcoded" in description_lower or "password" in description_lower:
        return [
            "Use environment variables for sensitive data",
            "Use secure configuration management",
            "Implement proper secrets management"
        ]
    
    elif "deserialization" in description_lower or "pickle" in description_lower:
        if language == "python":
            return [
                "Use json.loads() instead of pickle.loads()",
                "Implement custom deserialization with validation",
                "Use safe serialization libraries"
            ]
        elif language == "java":
            return [
                "Use JSON libraries like Jackson or Gson",
                "Implement custom deserialization with validation",
                "Use safe serialization libraries"
            ]
    
    return [
        "Implement proper input validation",
        "Use secure coding practices",
        "Follow OWASP security guidelines"
    ] 