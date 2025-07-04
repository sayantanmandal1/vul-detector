import React, { useState } from 'react';
import './App.css';
import CodeInput from './components/CodeInput';
import RepoAnalyzer from './components/RepoAnalyzer';
import ResultDisplay from './components/ResultDisplay';

function App() {
  const [activeTab, setActiveTab] = useState('code');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCodeAnalysis = async (code, language) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/analyze/code', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code: code,
          language: language
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
      console.error('Analysis failed:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRepoAnalysis = async (repoUrl) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/analyze/repo', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          repository_url: repoUrl,
          branch: 'main'
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
      console.error('Repository analysis failed:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🔒 Vulnerability Detector</h1>
        <p>AI-Powered Static Analysis for Security Vulnerabilities</p>
      </header>

      <main className="App-main">
        <div className="tab-container">
          <div className="tab-buttons">
            <button
              className={`tab-button ${activeTab === 'code' ? 'active' : ''}`}
              onClick={() => setActiveTab('code')}
            >
              📝 Code Analysis
            </button>
            <button
              className={`tab-button ${activeTab === 'repo' ? 'active' : ''}`}
              onClick={() => setActiveTab('repo')}
            >
              📁 Repository Analysis
            </button>
          </div>

          <div className="tab-content">
            {activeTab === 'code' && (
              <CodeInput onAnalyze={handleCodeAnalysis} />
            )}
            {activeTab === 'repo' && (
              <RepoAnalyzer onAnalyze={handleRepoAnalysis} />
            )}
          </div>
        </div>

        <ResultDisplay 
          result={result} 
          loading={loading} 
          error={error} 
        />
      </main>

      <footer className="App-footer">
        <p>Built with ❤️ for National-Level Security Analysis</p>
      </footer>
    </div>
  );
}

export default App;
