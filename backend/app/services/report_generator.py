import json
from datetime import datetime
from typing import List, Dict, Any, Union
from fpdf import FPDF
import io

class ReportGenerator:
    def __init__(self):
        self.severity_levels = {
            "high": ["eval", "exec", "os.system", "Runtime.getRuntime().exec", "gets", "strcpy", "pickle.loads", "yaml.load("],
            "medium": ["input(", "innerHTML", "document.write", "strcat", "sprintf", "execute(", "cursor.execute("],
            "low": ["subprocess.call", "setTimeout", "Class.forName", "scanf", "malloc", "JSON.parse("]
        }
    
    def _determine_severity(self, description: str) -> str:
        """Determine vulnerability severity based on description."""
        description_lower = description.lower()
        for severity, patterns in self.severity_levels.items():
            for pattern in patterns:
                if pattern.lower() in description_lower:
                    return severity
        return "low"
    
    def _group_by_severity(self, vulnerabilities: List[Dict]) -> Dict[str, List[Dict]]:
        """Group vulnerabilities by severity level."""
        grouped = {"high": [], "medium": [], "low": []}
        for vuln in vulnerabilities:
            severity = self._determine_severity(vuln.get("description", ""))
            grouped[severity].append(vuln)
        return grouped
    
    def _group_by_language(self, vulnerabilities: List[Dict]) -> Dict[str, List[Dict]]:
        """Group vulnerabilities by programming language."""
        grouped = {}
        for vuln in vulnerabilities:
            lang = vuln.get("language", "unknown")
            if lang not in grouped:
                grouped[lang] = []
            grouped[lang].append(vuln)
        return grouped
    
    def generate_pdf_report(self, analysis_result: Dict[str, Any]) -> bytearray:
        """Generate a PDF report with detailed vulnerability information."""
        vulnerabilities = analysis_result.get("vulnerabilities", [])
        
        # Add severity to each vulnerability
        for vuln in vulnerabilities:
            vuln["severity"] = self._determine_severity(vuln.get("description", ""))
        
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Vulnerability Analysis Report", ln=True, align='C')
        pdf.ln(10)
        
        # Report metadata
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Repository: {analysis_result.get('repository_url', 'N/A')}", ln=True)
        pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.cell(0, 10, f"Files Analyzed: {analysis_result.get('total_files_analyzed', 0)}", ln=True)
        pdf.cell(0, 10, f"Total Vulnerabilities: {analysis_result.get('total_vulnerabilities', 0)}", ln=True)
        pdf.ln(10)
        
        # Summary by severity
        grouped_by_severity = self._group_by_severity(vulnerabilities)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Summary by Severity:", ln=True)
        pdf.ln(5)
        
        pdf.set_font("Arial", "", 12)
        for severity in ["high", "medium", "low"]:
            count = len(grouped_by_severity[severity])
            pdf.cell(0, 10, f"{severity.upper()}: {count}", ln=True)
        pdf.ln(10)
        
        # Detailed vulnerabilities by severity
        for severity in ["high", "medium", "low"]:
            vulns = grouped_by_severity[severity]
            if vulns:
                pdf.set_font("Arial", "B", 14)
                pdf.cell(0, 10, f"{severity.upper()} SEVERITY VULNERABILITIES:", ln=True)
                pdf.ln(5)
                
                for i, vuln in enumerate(vulns, 1):
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 10, f"{i}. File: {vuln.get('file', 'N/A')}", ln=True)
                    
                    pdf.set_font("Arial", "", 10)
                    pdf.cell(0, 8, f"Line: {vuln.get('line', 'N/A')}", ln=True)
                    pdf.cell(0, 8, f"Language: {vuln.get('language', 'N/A')}", ln=True)
                    pdf.cell(0, 8, f"Description: {vuln.get('description', 'N/A')}", ln=True)
                    
                    if vuln.get('cwe'):
                        pdf.cell(0, 8, f"CWE: {vuln.get('cwe')}", ln=True)
                    if vuln.get('cve'):
                        pdf.cell(0, 8, f"CVE: {vuln.get('cve')}", ln=True)
                    
                    if vuln.get('suggested_fix'):
                        pdf.cell(0, 8, "Suggested Fix:", ln=True)
                        # Split long text into multiple lines
                        fix_text = vuln.get('suggested_fix', '')
                        words = fix_text.split()
                        line = ""
                        for word in words:
                            if len(line + word) < 80:
                                line += word + " "
                            else:
                                pdf.cell(0, 8, line, ln=True)
                                line = word + " "
                        if line:
                            pdf.cell(0, 8, line, ln=True)
                    
                    pdf.ln(5)
        
        # Return PDF as bytes
        return pdf.output(dest='S')
    
    def generate_json_report(self, analysis_result: Dict[str, Any]) -> str:
        """Generate a JSON report with detailed vulnerability information."""
        vulnerabilities = analysis_result.get("vulnerabilities", [])
        
        # Add severity to each vulnerability
        for vuln in vulnerabilities:
            vuln["severity"] = self._determine_severity(vuln.get("description", ""))
        
        report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "repository_url": analysis_result.get("repository_url", ""),
                "total_files_analyzed": analysis_result.get("total_files_analyzed", 0),
                "total_vulnerabilities": analysis_result.get("total_vulnerabilities", 0)
            },
            "summary": {
                "by_severity": {
                    severity: len(vulns) 
                    for severity, vulns in self._group_by_severity(vulnerabilities).items()
                },
                "by_language": {
                    lang: len(vulns) 
                    for lang, vulns in self._group_by_language(vulnerabilities).items()
                }
            },
            "vulnerabilities": vulnerabilities
        }
        
        return json.dumps(report, indent=2)
    
    def generate_text_report(self, analysis_result: Dict[str, Any]) -> str:
        """Generate a human-readable text report."""
        vulnerabilities = analysis_result.get("vulnerabilities", [])
        grouped_by_severity = self._group_by_severity(vulnerabilities)
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("VULNERABILITY ANALYSIS REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Repository: {analysis_result.get('repository_url', 'N/A')}")
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Files Analyzed: {analysis_result.get('total_files_analyzed', 0)}")
        report_lines.append(f"Total Vulnerabilities: {analysis_result.get('total_vulnerabilities', 0)}")
        report_lines.append("")
        
        # Summary by severity
        report_lines.append("SUMMARY BY SEVERITY:")
        report_lines.append("-" * 30)
        for severity in ["high", "medium", "low"]:
            count = len(grouped_by_severity[severity])
            report_lines.append(f"{severity.upper()}: {count}")
        report_lines.append("")
        
        # Detailed vulnerabilities by severity
        for severity in ["high", "medium", "low"]:
            vulns = grouped_by_severity[severity]
            if vulns:
                report_lines.append(f"{severity.upper()} SEVERITY VULNERABILITIES:")
                report_lines.append("-" * 40)
                for i, vuln in enumerate(vulns, 1):
                    report_lines.append(f"{i}. File: {vuln.get('file', 'N/A')}")
                    report_lines.append(f"   Line: {vuln.get('line', 'N/A')}")
                    report_lines.append(f"   Language: {vuln.get('language', 'N/A')}")
                    report_lines.append(f"   Description: {vuln.get('description', 'N/A')}")
                    if vuln.get('cwe'):
                        report_lines.append(f"   CWE: {vuln.get('cwe')}")
                    if vuln.get('cve'):
                        report_lines.append(f"   CVE: {vuln.get('cve')}")
                    if vuln.get('suggested_fix'):
                        report_lines.append(f"   Suggested Fix: {vuln.get('suggested_fix')}")
                    report_lines.append("")
        
        return "\n".join(report_lines)
    
    def generate_html_report(self, analysis_result: Dict[str, Any]) -> str:
        """Generate an HTML report for web display."""
        vulnerabilities = analysis_result.get("vulnerabilities", [])
        grouped_by_severity = self._group_by_severity(vulnerabilities)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Vulnerability Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .summary {{ margin: 20px 0; }}
                .severity-high {{ color: #d32f2f; }}
                .severity-medium {{ color: #f57c00; }}
                .severity-low {{ color: #388e3c; }}
                .vuln-item {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }}
                .vuln-header {{ font-weight: bold; margin-bottom: 10px; }}
                .fix-section {{ background-color: #f9f9f9; padding: 10px; margin-top: 10px; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Vulnerability Analysis Report</h1>
                <p><strong>Repository:</strong> {analysis_result.get('repository_url', 'N/A')}</p>
                <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Files Analyzed:</strong> {analysis_result.get('total_files_analyzed', 0)}</p>
                <p><strong>Total Vulnerabilities:</strong> {analysis_result.get('total_vulnerabilities', 0)}</p>
            </div>
            
            <div class="summary">
                <h2>Summary by Severity</h2>
                <p><span class="severity-high">High: {len(grouped_by_severity['high'])}</span></p>
                <p><span class="severity-medium">Medium: {len(grouped_by_severity['medium'])}</span></p>
                <p><span class="severity-low">Low: {len(grouped_by_severity['low'])}</span></p>
            </div>
        """
        
        for severity in ["high", "medium", "low"]:
            vulns = grouped_by_severity[severity]
            if vulns:
                html += f'<h2 class="severity-{severity}">{severity.upper()} Severity Vulnerabilities</h2>'
                for vuln in vulns:
                    html += f"""
                    <div class="vuln-item">
                        <div class="vuln-header">
                            File: {vuln.get('file', 'N/A')} | 
                            Line: {vuln.get('line', 'N/A')} | 
                            Language: {vuln.get('language', 'N/A')}
                        </div>
                        <p><strong>Description:</strong> {vuln.get('description', 'N/A')}</p>
                        {f'<p><strong>CWE:</strong> {vuln.get("cwe")}</p>' if vuln.get('cwe') else ''}
                        {f'<p><strong>CVE:</strong> {vuln.get("cve")}</p>' if vuln.get('cve') else ''}
                        {f'<div class="fix-section"><strong>Suggested Fix:</strong><br>{vuln.get("suggested_fix")}</div>' if vuln.get('suggested_fix') else ''}
                    </div>
                    """
        
        html += """
        </body>
        </html>
        """
        
        return html

def generate_report(analysis_result: Dict[str, Any], format_type: str = "json") -> Union[str, bytearray]:
    """Generate a vulnerability report in the specified format."""
    generator = ReportGenerator()
    
    if format_type == "json":
        return generator.generate_json_report(analysis_result)
    elif format_type == "text":
        return generator.generate_text_report(analysis_result)
    elif format_type == "html":
        return generator.generate_html_report(analysis_result)
    elif format_type == "pdf":
        return generator.generate_pdf_report(analysis_result)
    else:
        raise ValueError(f"Unsupported format: {format_type}") 