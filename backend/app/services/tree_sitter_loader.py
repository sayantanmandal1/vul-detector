import os
from tree_sitter import Language, Parser

BASE_DIR = os.path.dirname(__file__)
LIB_PATH = os.path.join(BASE_DIR, "build", "my-languages.so")

GRAMMAR_DIRS = [
    os.path.join(BASE_DIR, "tree-sitter-python"),
    os.path.join(BASE_DIR, "tree-sitter-c"),
    os.path.join(BASE_DIR, "tree-sitter-cpp"),
    os.path.join(BASE_DIR, "tree-sitter-javascript"),
    os.path.join(BASE_DIR, "tree-sitter-java"),
]

# Check if we're in a Docker environment (production)
IS_DOCKER = os.path.exists('/.dockerenv') or os.environ.get('DOCKER_ENV') == 'true'

if not os.path.exists(LIB_PATH) and not IS_DOCKER:
    # Only build if not in Docker and library doesn't exist
    # In Docker, the library should be pre-built
    try:
        Language.build_library(
            LIB_PATH,
            GRAMMAR_DIRS
        )
    except Exception as e:
        print(f"Warning: Could not build tree-sitter library: {e}")
        # Continue with None values for languages
        PY_LANGUAGE = None
        C_LANGUAGE = None
        CPP_LANGUAGE = None
        JS_LANGUAGE = None
        JAVA_LANGUAGE = None
else:
    try:
        PY_LANGUAGE = Language(LIB_PATH, "python")
        C_LANGUAGE = Language(LIB_PATH, "c")
        CPP_LANGUAGE = Language(LIB_PATH, "cpp")
        JS_LANGUAGE = Language(LIB_PATH, "javascript")
        JAVA_LANGUAGE = Language(LIB_PATH, "java")
    except Exception as e:
        print(f"Warning: Could not load tree-sitter languages: {e}")
        # Fallback to None values
        PY_LANGUAGE = None
        C_LANGUAGE = None
        CPP_LANGUAGE = None
        JS_LANGUAGE = None
        JAVA_LANGUAGE = None

LANGUAGE_MAP = {
    "python": PY_LANGUAGE,
    "c": C_LANGUAGE,
    "cpp": CPP_LANGUAGE,
    "javascript": JS_LANGUAGE,
    "java": JAVA_LANGUAGE,
} 