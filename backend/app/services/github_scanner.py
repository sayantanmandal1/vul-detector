import os
import tempfile
from git import Repo
from pathlib import Path

SUPPORTED_EXTENSIONS = {
    "python": [".py"],
    "javascript": [".js", ".jsx", ".ts", ".tsx"],
    "java": [".java"],
    "c": [".c"],
    "cpp": [".cpp", ".cc", ".cxx", ".hpp", ".h"],
    "html": [".html", ".htm"],
    "css": [".css"]
}

def clone_and_collect_files(repo_url):
    """
    Clone a GitHub repository and collect all supported code files.
    
    Args:
        repo_url (str): GitHub repository URL
        
    Returns:
        tuple: (list of code files with metadata, temp directory path)
    """
    temp_dir = tempfile.mkdtemp()
    try:
        Repo.clone_from(repo_url, temp_dir)
        code_files = []
        
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = Path(root) / file
                for lang, exts in SUPPORTED_EXTENSIONS.items():
                    if any(file.endswith(ext) for ext in exts):
                        # Get relative path from temp_dir
                        relative_path = os.path.relpath(file_path, temp_dir)
                        code_files.append({
                            "path": str(file_path),
                            "relative_path": relative_path,
                            "language": lang,
                            "filename": file
                        })
                        break  # Found language, move to next file
        
        return code_files, temp_dir
    except Exception as e:
        # Clean up temp directory on error
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise e

def analyze_repository_files(repo_url):
    """
    Clone repository and analyze all supported code files for vulnerabilities.
    
    Args:
        repo_url (str): GitHub repository URL
        
    Returns:
        dict: Analysis results with file metadata and vulnerabilities
    """
    from app.services.analyzer import analyze_code
    
    files, temp_dir = clone_and_collect_files(repo_url)
    all_vulns = []
    
    for file_info in files:
        try:
            with open(file_info["path"], "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
            
            vulns = analyze_code(code, file_info["language"])
            
            # Add file metadata to each vulnerability
            for vuln in vulns:
                vuln.update({
                    "file": file_info["relative_path"],
                    "filename": file_info["filename"],
                    "language": file_info["language"]
                })
            
            all_vulns.extend(vulns)
            
        except Exception as e:
            # Log error but continue with other files
            print(f"Error analyzing {file_info['path']}: {e}")
            continue
    
    # Clean up temp directory
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
    
    return {
        "repository_url": repo_url,
        "total_files_analyzed": len(files),
        "total_vulnerabilities": len(all_vulns),
        "vulnerabilities": all_vulns
    } 