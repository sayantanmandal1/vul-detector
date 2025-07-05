"""
Report generator for vulnerability analysis results.
"""

import json
from datetime import datetime
from typing import Any, Dict


def generate_report(analysis_result: Dict[str, Any], format_type: str) -> str | bytes:
    """
    Generate a report in the specified format.
    
    Args:
        analysis_result: Dictionary containing analysis results
        format_type: Format type ('json', 'text', 'html', 'pdf')
        
    Returns:
        Report content as string (or bytes for PDF)
    """
    if format_type == "json":
        return generate_json_report(analysis_result)
    elif format_type == "text":
        return generate_text_report(analysis_result)
    elif format_type == "html":
        return generate_html_report(analysis_result)
    elif format_type == "pdf":
        return generate_pdf_report(analysis_result)
    else:
        raise ValueError(f"Unsupported format: {format_type}")

def generate_json_report(analysis_result: Dict[str, Any]) -> str:
    """Generate JSON report."""
    return json.dumps(analysis_result, indent=2, default=str)

def generate_text_report(analysis_result: Dict[str, Any]) -> str:
    """Generate plain text report."""
    report = []
    report.append("=" * 60)
    report.append("VULNERABILITY ANALYSIS REPORT")
    report.append("=" * 60)
    report.append("")
    
    # Summary
    report.append("SUMMARY:")
    report.append(f"Repository URL: {analysis_result.get('repository_url', 'N/A')}")
    report.append(f"Total Files Analyzed: {analysis_result.get('total_files_analyzed', 0)}")
    report.append(f"Total Vulnerabilities Found: {analysis_result.get('total_vulnerabilities', 0)}")
    report.append(f"Analysis Time: {analysis_result.get('analysis_time', 0):.2f} seconds")
    report.append(f"Timestamp: {analysis_result.get('timestamp', datetime.now())}")
    report.append("")
    
    # Vulnerabilities
    vulnerabilities = analysis_result.get('vulnerabilities', [])
    if vulnerabilities:
        report.append("VULNERABILITIES FOUND:")
        report.append("-" * 40)
        
        for i, vuln in enumerate(vulnerabilities, 1):
            report.append(f"{i}. File: {vuln.get('file', 'Unknown')}")
            report.append(f"   Line: {vuln.get('line', 'Unknown')}")
            report.append(f"   Language: {vuln.get('language', 'Unknown')}")
            report.append(f"   Description: {vuln.get('description', 'No description')}")
            report.append("")
    else:
        report.append("No vulnerabilities found.")
    
    return "\n".join(report)

def generate_html_report(analysis_result: Dict[str, Any]) -> str:
    """Generate HTML report."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Vulnerability Analysis Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .header { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }
            .summary { margin: 20px 0; }
            .vulnerability { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
            .file { font-weight: bold; color: #333; }
            .line { color: #666; }
            .description { margin-top: 10px; }
            .no-vulns { color: green; font-style: italic; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Vulnerability Analysis Report</h1>
        </div>
        
        <div class="summary">
            <h2>Summary</h2>
            <p><strong>Repository URL:</strong> {repository_url}</p>
            <p><strong>Total Files Analyzed:</strong> {total_files}</p>
            <p><strong>Total Vulnerabilities Found:</strong> {total_vulns}</p>
            <p><strong>Analysis Time:</strong> {analysis_time:.2f} seconds</p>
            <p><strong>Timestamp:</strong> {timestamp}</p>
        </div>
        
        <div class="vulnerabilities">
            <h2>Vulnerabilities Found</h2>
            {vulnerabilities_html}
        </div>
    </body>
    </html>
    """
    
    vulnerabilities = analysis_result.get('vulnerabilities', [])
    vulnerabilities_html = ""
    
    if vulnerabilities:
        for vuln in vulnerabilities:
            vulnerabilities_html += f"""
            <div class="vulnerability">
                <div class="file">File: {vuln.get('file', 'Unknown')}</div>
                <div class="line">Line: {vuln.get('line', 'Unknown')} | Language: {vuln.get('language', 'Unknown')}</div>
                <div class="description">{vuln.get('description', 'No description')}</div>
            </div>
            """
    else:
        vulnerabilities_html = '<p class="no-vulns">No vulnerabilities found.</p>'
    
    return html.format(
        repository_url=analysis_result.get('repository_url', 'N/A'),
        total_files=analysis_result.get('total_files_analyzed', 0),
        total_vulns=analysis_result.get('total_vulnerabilities', 0),
        analysis_time=analysis_result.get('analysis_time', 0),
        timestamp=analysis_result.get('timestamp', datetime.now()),
        vulnerabilities_html=vulnerabilities_html
    )

def generate_pdf_report(analysis_result: Dict[str, Any]) -> bytes:
    """Generate PDF report."""
    try:
        from io import BytesIO

        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import (
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )

        # Create PDF buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        story.append(Paragraph("Vulnerability Analysis Report", title_style))
        story.append(Spacer(1, 12))
        
        # Summary
        story.append(Paragraph("Summary", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        summary_data = [
            ['Repository URL', analysis_result.get('repository_url', 'N/A')],
            ['Total Files Analyzed', str(analysis_result.get('total_files_analyzed', 0))],
            ['Total Vulnerabilities Found', str(analysis_result.get('total_vulnerabilities', 0))],
            ['Analysis Time', f"{analysis_result.get('analysis_time', 0):.2f} seconds"],
            ['Timestamp', str(analysis_result.get('timestamp', datetime.now()))]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Vulnerabilities
        story.append(Paragraph("Vulnerabilities Found", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        vulnerabilities = analysis_result.get('vulnerabilities', [])
        if vulnerabilities:
            for i, vuln in enumerate(vulnerabilities, 1):
                vuln_text = f"""
                <b>{i}. File:</b> {vuln.get('file', 'Unknown')}<br/>
                <b>Line:</b> {vuln.get('line', 'Unknown')} | <b>Language:</b> {vuln.get('language', 'Unknown')}<br/>
                <b>Description:</b> {vuln.get('description', 'No description')}
                """
                story.append(Paragraph(vuln_text, styles['Normal']))
                story.append(Spacer(1, 12))
        else:
            story.append(Paragraph("No vulnerabilities found.", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
        
    except ImportError:
        # Fallback to text if reportlab is not available
        text_report = generate_text_report(analysis_result)
        return text_report.encode('utf-8')
    except Exception as e:
        # Fallback to error message
        error_msg = f"PDF generation failed: {str(e)}. Please use JSON or text format instead."
        return error_msg.encode('utf-8') 