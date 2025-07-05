#!/usr/bin/env python3
"""
Test script to verify JSON and text report formats work correctly.
"""

import requests
import json
import sys

def test_report_formats():
    """Test different report formats to ensure they work."""
    
    # Sample analysis result
    sample_result = {
        "repository_url": "https://github.com/test/repo",
        "total_files_analyzed": 3,
        "total_vulnerabilities": 2,
        "vulnerabilities": [
            {
                "file": "test.py",
                "line": 10,
                "language": "python",
                "description": "Potential code injection via eval()",
                "cwe": "CWE-78",
                "suggested_fix": "Use ast.literal_eval() instead of eval()"
            },
            {
                "file": "app.js",
                "line": 25,
                "language": "javascript",
                "description": "Potential XSS via innerHTML",
                "cwe": "CWE-79",
                "suggested_fix": "Use textContent instead of innerHTML"
            }
        ],
        "analysis_time": 1.5,
        "timestamp": "2024-01-01T12:00:00"
    }
    
    formats_to_test = ["json", "text", "html"]
    
    print("Testing report formats...")
    print("=" * 50)
    
    for format_type in formats_to_test:
        print(f"\nTesting {format_type.upper()} format:")
        print("-" * 30)
        
        try:
            response = requests.post(
                "https://vul-detector.onrender.com/report",
                json={
                    "analysis_result": sample_result,
                    "format": format_type
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print(f"✅ {format_type.upper()} format: SUCCESS")
                print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
                print(f"   Content-Length: {len(response.content)} bytes")
                
                if format_type == "json":
                    # Verify JSON is valid
                    try:
                        json_content = response.json()
                        print(f"   JSON validation: ✅ Valid JSON")
                        print(f"   Vulnerabilities count: {len(json_content.get('vulnerabilities', []))}")
                    except json.JSONDecodeError as e:
                        print(f"   JSON validation: ❌ Invalid JSON - {e}")
                else:
                    # For text and HTML, just show first 100 chars
                    content = response.text[:100]
                    print(f"   Content preview: {content}...")
                    
            else:
                print(f"❌ {format_type.upper()} format: FAILED")
                print(f"   Status: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {format_type.upper()} format: REQUEST ERROR")
            print(f"   Error: {e}")
    
    print("\n" + "=" * 50)
    print("Format testing completed!")
    print("\nRecommendations:")
    print("- JSON format is the most reliable and recommended")
    print("- Text format is good for human-readable reports")
    print("- HTML format is good for web display")
    print("- PDF format may fail on some systems due to font/dependency issues")

if __name__ == "__main__":
    test_report_formats() 