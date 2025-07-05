"""
GitHub repository scanner for vulnerability detection.
"""

import os
import tempfile
import subprocess
import time
from typing import Dict, Any, List
from pathlib import Path

from .analyzer import analyze_code

def analyze_repository_files(repository_url: str) -> Dict[str, Any]:
    """
    Analyze a GitHub repository for vulnerabilities.
    
    Args:
        repository_url: URL of the GitHub repository to analyze
        
    Returns:
        Dictionary containing analysis results
    """
    start_time = time.time()
    
    try:
        # Create a temporary directory for cloning
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"Cloning repository: {repository_url}")
            
            # Clone the repository
            clone_result = subprocess.run(
                ["git", "clone", "--depth", "1", repository_url, temp_dir],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if clone_result.returncode != 0:
                raise Exception(f"Failed to clone repository: {clone_result.stderr}")
            
            print(f"Repository cloned successfully to {temp_dir}")
            
            # Find all code files
            code_files = find_code_files(temp_dir)
            print(f"Found {len(code_files)} code files to analyze")
            
            # Log file types found
            file_types = {}
            for file_path in code_files:
                ext = file_path.suffix.lower()
                file_types[ext] = file_types.get(ext, 0) + 1
            print(f"File types found: {file_types}")
            
            all_vulnerabilities = []
            analyzed_files = 0
            
            # Analyze each file
            for file_path in code_files:
                try:
                    language = detect_language(file_path)
                    if language:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            code_content = f.read()
                        
                        # Analyze the file using the full analysis pipeline
                        vulnerabilities, _ = analyze_code(
                            code_content, 
                            language, 
                            str(file_path)
                        )
                        
                        # Add file information to vulnerabilities
                        for vuln in vulnerabilities:
                            vuln['file'] = str(file_path)
                            vuln['line'] = vuln.get('line', 0)
                        
                        all_vulnerabilities.extend(vulnerabilities)
                        analyzed_files += 1
                        
                        # Debug logging for files with vulnerabilities
                        if vulnerabilities:
                            print(f"Found {len(vulnerabilities)} vulnerabilities in {file_path} ({language})")
                            for vuln in vulnerabilities:
                                print(f"  - {vuln['description']} at line {vuln['line']}")
                        
                        if analyzed_files % 10 == 0:
                            print(f"Analyzed {analyzed_files}/{len(code_files)} files...")
                            
                except Exception as e:
                    print(f"Error analyzing {file_path}: {e}")
                    continue
            
            analysis_time = time.time() - start_time
            
            return {
                "vulnerabilities": all_vulnerabilities,
                "total_files_analyzed": analyzed_files,
                "total_files_found": len(code_files),
                "analysis_time": analysis_time,
                "repository_url": repository_url
            }
            
    except Exception as e:
        print(f"Error analyzing repository: {e}")
        return {
            "vulnerabilities": [],
            "total_files_analyzed": 0,
            "total_files_found": 0,
            "analysis_time": time.time() - start_time,
            "repository_url": repository_url,
            "error": str(e)
        }

def find_code_files(directory: str) -> List[Path]:
    """
    Find all code files in the given directory.
    
    Args:
        directory: Directory to search for code files
        
    Returns:
        List of Path objects for code files
    """
    code_extensions = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp', '.cc', '.cxx',
        '.h', '.hpp', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala'
    }
    
    code_files = []
    
    for root, dirs, files in os.walk(directory):
        # Skip common directories that shouldn't be analyzed
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', 'venv', 'env', 'build', 'dist'}]
        
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in code_extensions:
                code_files.append(file_path)
    
    return code_files

def detect_language(file_path: Path) -> str:
    """
    Detect the programming language based on file extension.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Language identifier string
    """
    extension = file_path.suffix.lower()
    
    language_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',  # TypeScript should have its own patterns
        '.jsx': 'javascript',
        '.tsx': 'typescript',  # TypeScript JSX
        '.java': 'java',
        '.c': 'c',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        '.h': 'c',
        '.hpp': 'cpp',
        '.cs': 'csharp',  # Not supported yet, but could be added
        '.php': 'php',    # Not supported yet, but could be added
        '.rb': 'ruby',    # Not supported yet, but could be added
        '.go': 'go',      # Not supported yet, but could be added
        '.rs': 'rust',    # Not supported yet, but could be added
        '.swift': 'swift', # Not supported yet, but could be added
        '.kt': 'kotlin',  # Not supported yet, but could be added
        '.scala': 'scala' # Not supported yet, but could be added
    }
    
    return language_map.get(extension, '') 