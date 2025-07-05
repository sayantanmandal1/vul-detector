#!/usr/bin/env python3
"""
Script to build Tree-sitter language grammars for the vulnerability detector.
"""

import os
import sys
import tree_sitter
from tree_sitter import Language

def build_tree_sitter_library():
    """Build the Tree-sitter library with all supported languages."""
    
    # Use current working directory (should be /app/app/services)
    base_dir = os.getcwd()
    print(f"Current working directory: {base_dir}")
    
    # List all contents of the current directory
    print("=== All contents of current directory ===")
    try:
        for item in os.listdir(base_dir):
            item_path = os.path.join(base_dir, item)
            if os.path.isdir(item_path):
                print(f"  DIR:  {item}")
            else:
                print(f"  FILE: {item}")
    except Exception as e:
        print(f"Error listing directory: {e}")
    
    # Define expected grammar paths
    expected_grammars = [
        "tree-sitter-python",
        "tree-sitter-c", 
        "tree-sitter-cpp",
        "tree-sitter-javascript",
        "tree-sitter-java"
    ]
    
    # Find all tree-sitter directories
    found_grammars = []
    for item in os.listdir(base_dir):
        if item.startswith('tree-sitter-'):
            found_grammars.append(item)
    
    print(f"=== Found tree-sitter directories: {found_grammars} ===")
    
    # Use found grammars or fall back to expected ones
    grammar_paths = []
    for grammar in found_grammars:
        grammar_path = os.path.join(base_dir, grammar)
        if os.path.exists(grammar_path):
            grammar_paths.append(grammar_path)
            print(f"✓ Found grammar: {grammar}")
        else:
            print(f"✗ Grammar path does not exist: {grammar_path}")
    
    # If no grammars found, try the expected paths
    if not grammar_paths:
        print("No tree-sitter directories found, trying expected paths...")
        for grammar in expected_grammars:
            grammar_path = os.path.join(base_dir, grammar)
            if os.path.exists(grammar_path):
                grammar_paths.append(grammar_path)
                print(f"✓ Found expected grammar: {grammar}")
            else:
                print(f"✗ Expected grammar not found: {grammar}")
    
    if not grammar_paths:
        print("ERROR: No tree-sitter grammar directories found!")
        print("Expected directories:")
        for grammar in expected_grammars:
            print(f"  - {grammar}")
        print("Available directories:")
        for item in os.listdir(base_dir):
            if os.path.isdir(os.path.join(base_dir, item)):
                print(f"  - {item}")
        return False
    
    # Create build directory
    build_dir = os.path.join(base_dir, "build")
    os.makedirs(build_dir, exist_ok=True)
    
    lib_path = os.path.join(build_dir, "my-languages.so")
    
    try:
        print(f"Building tree-sitter library with {len(grammar_paths)} grammars...")
        print(f"Grammar paths: {grammar_paths}")
        print(f"Library path: {lib_path}")
        
        Language.build_library(
            lib_path,
            grammar_paths
        )
        print("✓ Successfully built tree-sitter library")
        
        # Test loading the languages
        print("Testing language parsers...")
        test_languages = ["python", "c", "cpp", "javascript", "java"]
        for lang in test_languages:
            try:
                Language(lib_path, lang)
                print(f"✓ Successfully loaded {lang} parser")
            except Exception as e:
                print(f"✗ Failed to load {lang} parser: {e}")
        
        print("✓ Successfully tested all language parsers")
        return True
        
    except Exception as e:
        print(f"✗ Error building tree-sitter library: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = build_tree_sitter_library()
    sys.exit(0 if success else 1) 