#!/usr/bin/env python3
"""
Test script to verify Tree-sitter build process
"""
import os
import sys
from tree_sitter import Language

def test_tree_sitter_build():
    """Test the tree-sitter build process"""
    print("Testing Tree-sitter build process...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    services_dir = os.path.join(current_dir, "app", "services")
    
    # Define paths
    build_dir = os.path.join(services_dir, "build")
    lib_path = os.path.join(build_dir, "my-languages.so")
    
    # Grammar directories
    grammar_dirs = [
        os.path.join(services_dir, "tree-sitter-python"),
        os.path.join(services_dir, "tree-sitter-c"),
        os.path.join(services_dir, "tree-sitter-cpp"),
        os.path.join(services_dir, "tree-sitter-javascript"),
        os.path.join(services_dir, "tree-sitter-java"),
    ]
    
    # Check if grammar directories exist
    print("Checking grammar directories...")
    for grammar_dir in grammar_dirs:
        if os.path.exists(grammar_dir):
            print(f"✓ {os.path.basename(grammar_dir)} exists")
        else:
            print(f"✗ {os.path.basename(grammar_dir)} missing")
            return False
    
    # Create build directory if it doesn't exist
    os.makedirs(build_dir, exist_ok=True)
    
    # Build the library
    print("Building Tree-sitter library...")
    try:
        Language.build_library(lib_path, grammar_dirs)
        print("✓ Library built successfully")
    except Exception as e:
        print(f"✗ Failed to build library: {e}")
        return False
    
    # Test loading languages
    print("Testing language loading...")
    try:
        python_lang = Language(lib_path, "python")
        c_lang = Language(lib_path, "c")
        cpp_lang = Language(lib_path, "cpp")
        js_lang = Language(lib_path, "javascript")
        java_lang = Language(lib_path, "java")
        print("✓ All languages loaded successfully")
    except Exception as e:
        print(f"✗ Failed to load languages: {e}")
        return False
    
    # Test parsing
    print("Testing parsing...")
    try:
        from tree_sitter import Parser
        parser = Parser()
        parser.set_language(python_lang)
        
        test_code = "print('Hello, World!')"
        tree = parser.parse(bytes(test_code, "utf8"))
        print("✓ Parsing test successful")
    except Exception as e:
        print(f"✗ Parsing test failed: {e}")
        return False
    
    print("All tests passed!")
    return True

if __name__ == "__main__":
    success = test_tree_sitter_build()
    sys.exit(0 if success else 1) 