import os
import sys
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

# Initialize language variables
PY_LANGUAGE = None
C_LANGUAGE = None
CPP_LANGUAGE = None
JS_LANGUAGE = None
JAVA_LANGUAGE = None

# Try to load the pre-built library
if os.path.exists(LIB_PATH):
    try:
        print(f"Attempting to load tree-sitter library from: {LIB_PATH}")
        PY_LANGUAGE = Language(LIB_PATH, "python")
        C_LANGUAGE = Language(LIB_PATH, "c")
        CPP_LANGUAGE = Language(LIB_PATH, "cpp")
        JS_LANGUAGE = Language(LIB_PATH, "javascript")
        JAVA_LANGUAGE = Language(LIB_PATH, "java")
        print("Successfully loaded pre-built tree-sitter languages")
    except Exception as e:
        print(f"Warning: Could not load pre-built tree-sitter languages: {e}")
        print(f"Library path: {LIB_PATH}")
        print(f"Library exists: {os.path.exists(LIB_PATH)}")
        if os.path.exists(LIB_PATH):
            try:
                import subprocess
                result = subprocess.run(['file', LIB_PATH], capture_output=True, text=True)
                print(f"Library file type: {result.stdout}")
            except Exception as file_error:
                print(f"Could not check file type: {file_error}")
        
        # Try to rebuild if in development environment
        if not IS_DOCKER:
            try:
                print("Attempting to rebuild tree-sitter library...")
                Language.build_library(
                    LIB_PATH,
                    GRAMMAR_DIRS
                )
                PY_LANGUAGE = Language(LIB_PATH, "python")
                C_LANGUAGE = Language(LIB_PATH, "c")
                CPP_LANGUAGE = Language(LIB_PATH, "cpp")
                JS_LANGUAGE = Language(LIB_PATH, "javascript")
                JAVA_LANGUAGE = Language(LIB_PATH, "java")
                print("Successfully rebuilt and loaded tree-sitter languages")
            except Exception as rebuild_error:
                print(f"Warning: Could not rebuild tree-sitter library: {rebuild_error}")
                # Continue with None values for languages
                PY_LANGUAGE = None
                C_LANGUAGE = None
                CPP_LANGUAGE = None
                JS_LANGUAGE = None
                JAVA_LANGUAGE = None
        else:
            # In Docker, just continue with None values
            PY_LANGUAGE = None
            C_LANGUAGE = None
            CPP_LANGUAGE = None
            JS_LANGUAGE = None
            JAVA_LANGUAGE = None
elif not IS_DOCKER:
    # Only try to build if not in Docker and library doesn't exist
    try:
        print("Building tree-sitter library...")
        Language.build_library(
            LIB_PATH,
            GRAMMAR_DIRS
        )
        PY_LANGUAGE = Language(LIB_PATH, "python")
        C_LANGUAGE = Language(LIB_PATH, "c")
        CPP_LANGUAGE = Language(LIB_PATH, "cpp")
        JS_LANGUAGE = Language(LIB_PATH, "javascript")
        JAVA_LANGUAGE = Language(LIB_PATH, "java")
        print("Successfully built and loaded tree-sitter languages")
    except Exception as e:
        print(f"Warning: Could not build tree-sitter library: {e}")
        # Continue with None values for languages
        PY_LANGUAGE = None
        C_LANGUAGE = None
        CPP_LANGUAGE = None
        JS_LANGUAGE = None
        JAVA_LANGUAGE = None
else:
    print("Running in Docker environment - tree-sitter library should be pre-built")

LANGUAGE_MAP = {
    "python": PY_LANGUAGE,
    "c": C_LANGUAGE,
    "cpp": CPP_LANGUAGE,
    "javascript": JS_LANGUAGE,
    "java": JAVA_LANGUAGE,
} 