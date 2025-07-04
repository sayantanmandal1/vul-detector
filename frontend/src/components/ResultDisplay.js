import React, { useState } from 'react';
import './ResultDisplay.css';

const ResultDisplay = ({ result, loading, error }) => {
  const [downloadFormat, setDownloadFormat] = useState('json');

  const downloadReport = async (format) => {
    if (!result) return;

    try {
      const response = await fetch('http://localhost:8000/report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          analysis_result: result,
          format: format
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Get the filename from the Content-Disposition header
      const contentDisposition = response.headers.get('Content-Disposition');
      let filename = `vulnerability_report.${format}`;
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename=(.+)/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }

      // Handle different content types
      const contentType = response.headers.get('Content-Type');
      
      if (format === 'pdf' || contentType?.includes('application/pdf')) {
        // Handle PDF as blob
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        // Handle text-based formats
        const content = await response.text();
        const blob = new Blob([content], { 
          type: contentType || 'text/plain' 
        });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (error) {
      console.error('Download failed:', error);
      alert('Failed to download report. Please try again.');
    }
  };

  const getSeverityColor = (description) => {
    const highPatterns = ['eval', 'exec', 'os.system', 'Runtime.getRuntime().exec', 'gets', 'strcpy'];
    const mediumPatterns = ['input(', 'innerHTML', 'document.write', 'strcat', 'sprintf'];
    
    const desc = description.toLowerCase();
    if (highPatterns.some(pattern => desc.includes(pattern.toLowerCase()))) {
      return '#d32f2f'; // Red for high
    } else if (mediumPatterns.some(pattern => desc.includes(pattern.toLowerCase()))) {
      return '#f57c00'; // Orange for medium
    }
    return '#388e3c'; // Green for low
  };

  if (loading) {
    return (
      <div className="result-display">
        <div className="loading">
          <div className="spinner"></div>
          <p>Analyzing code for vulnerabilities...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="result-display">
        <div className="error">
          <h3>Error</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="result-display">
        <div className="no-result">
          <p>No analysis result to display. Please analyze some code first.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="result-display">
      <div className="result-header">
        <h2>Analysis Results</h2>
        <div className="download-section">
          <select 
            value={downloadFormat} 
            onChange={(e) => setDownloadFormat(e.target.value)}
            className="format-select"
          >
            <option value="json">JSON</option>
            <option value="text">Text</option>
            <option value="html">HTML</option>
            <option value="pdf">PDF</option>
          </select>
          <button 
            onClick={() => downloadReport(downloadFormat)}
            className="download-btn"
          >
            Download Report
          </button>
        </div>
      </div>

      <div className="result-summary">
        <div className="summary-item">
          <span className="label">Repository:</span>
          <span className="value">{result.repository_url || 'N/A'}</span>
        </div>
        <div className="summary-item">
          <span className="label">Files Analyzed:</span>
          <span className="value">{result.total_files_analyzed}</span>
        </div>
        <div className="summary-item">
          <span className="label">Total Vulnerabilities:</span>
          <span className="value">{result.total_vulnerabilities}</span>
        </div>
        {result.analysis_time && (
          <div className="summary-item">
            <span className="label">Analysis Time:</span>
            <span className="value">{result.analysis_time.toFixed(2)}s</span>
          </div>
        )}
      </div>

      {result.vulnerabilities && result.vulnerabilities.length > 0 ? (
        <div className="vulnerabilities-list">
          <h3>Detected Vulnerabilities</h3>
          {result.vulnerabilities.map((vuln, index) => (
            <div key={index} className="vulnerability-item">
              <div className="vuln-header">
                <span className="vuln-file">{vuln.file}</span>
                <span className="vuln-line">Line {vuln.line}</span>
                <span className="vuln-language">{vuln.language}</span>
                <span 
                  className="vuln-severity"
                  style={{ color: getSeverityColor(vuln.description) }}
                >
                  {vuln.severity || 'Unknown'}
                </span>
              </div>
              <div className="vuln-description">
                <strong>Description:</strong> {vuln.description}
              </div>
              {vuln.cwe && (
                <div className="vuln-cwe">
                  <strong>CWE:</strong> {vuln.cwe}
                </div>
              )}
              {vuln.cve && (
                <div className="vuln-cve">
                  <strong>CVE:</strong> {vuln.cve}
                </div>
              )}
              {vuln.suggested_fix && (
                <div className="vuln-fix">
                  <strong>Suggested Fix:</strong>
                  <pre>{vuln.suggested_fix}</pre>
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="no-vulnerabilities">
          <h3>No Vulnerabilities Detected</h3>
          <p>Great! No security vulnerabilities were found in the analyzed code.</p>
        </div>
      )}
    </div>
  );
};

export default ResultDisplay; 