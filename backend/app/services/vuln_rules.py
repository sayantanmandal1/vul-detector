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
            }
        ]
    return [] 