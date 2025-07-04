import React, { useState } from "react";
import axios from "axios";
import CodeInput from "./components/CodeInput";
import ResultDisplay from "./components/ResultDisplay";

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (code, language) => {
    setLoading(true);
    setResults(null);
    try {
      const response = await axios.post("http://localhost:8000/analyze", {
        code,
        language,
      });
      setResults(response.data.vulnerabilities);
    } catch (err) {
      alert("Error analyzing code.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <CodeInput onAnalyze={handleAnalyze} />
      {loading ? <p>Analyzing...</p> : <ResultDisplay results={results} />}
    </div>
  );
}

export default App;
