import React, { useState } from 'react';
import './RepoAnalyzer.css';

const RepoAnalyzer = ({ onAnalyze }) => {
  const [repoUrl, setRepoUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!repoUrl.trim()) {
      alert('Please enter a GitHub repository URL');
      return;
    }

    setLoading(true);
    try {
      await onAnalyze(repoUrl.trim());
    } catch (error) {
      console.error('Repository analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };



  return (
    <div className="repo-analyzer">
      <div className="analyzer-header">
        <h2>🔍 Repository Vulnerability Scanner</h2>
        <p>Analyze entire GitHub repositories for security vulnerabilities</p>
      </div>

      <form onSubmit={handleSubmit} className="analyzer-form">
        <div className="input-group">
          <label htmlFor="repoUrl">GitHub Repository URL:</label>
          <input
            type="url"
            id="repoUrl"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            placeholder="https://github.com/username/repository"
            disabled={loading}
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading || !repoUrl.trim()}
          className="analyze-btn"
        >
          {loading ? (
            <>
              <span className="spinner"></span>
              Analyzing Repository...
            </>
          ) : (
            '🔍 Analyze Repository'
          )}
        </button>
      </form>

      <div className="features">
        <h3>What gets analyzed:</h3>
        <ul>
          <li>✅ Multiple programming languages (Python, JavaScript, Java, C/C++)</li>
          <li>✅ Static code analysis for security vulnerabilities</li>
          <li>✅ CVE/CWE mapping for known vulnerabilities</li>
          <li>✅ AI-powered mitigation suggestions</li>
          <li>✅ Detailed reports in multiple formats</li>
        </ul>
      </div>

      <div className="example-repos">
        <h3>Example repositories to test:</h3>
        <div className="repo-examples">
          <button
            onClick={() => setRepoUrl('https://github.com/sayantanmandal1/sign-recognition')}
            className="example-btn"
          >
            sayantanmandal1/sign-recognition
          </button>
          <button
            onClick={() => setRepoUrl('https://github.com/sayantanmandal1/ai-resume-checker')}
            className="example-btn"
          >
            sayantanmandal1/ai-resume-checker
          </button>
          <button
            onClick={() => setRepoUrl('https://github.com/sayantanmandal1/fake-bill-detector')}
            className="example-btn"
          >
            sayantanmandal1/fake-bill-detector
          </button>
        </div>
      </div>
    </div>
  );
};

export default RepoAnalyzer; 