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

if not os.path.exists(LIB_PATH):
    Language.build_library(
        LIB_PATH,
        GRAMMAR_DIRS
    )

PY_LANGUAGE = Language(LIB_PATH, "python")
C_LANGUAGE = Language(LIB_PATH, "c")
CPP_LANGUAGE = Language(LIB_PATH, "cpp")
JS_LANGUAGE = Language(LIB_PATH, "javascript")
JAVA_LANGUAGE = Language(LIB_PATH, "java")

LANGUAGE_MAP = {
    "python": PY_LANGUAGE,
    "c": C_LANGUAGE,
    "cpp": CPP_LANGUAGE,
    "javascript": JS_LANGUAGE,
    "java": JAVA_LANGUAGE,
} 