import React, { useState } from "react";

const CodeInput = ({ onAnalyze }) => {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");

  const handleSubmit = (e) => {
    e.preventDefault();
    onAnalyze(code, language);
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Code Vulnerability Analyzer</h2>
      <select value={language} onChange={(e) => setLanguage(e.target.value)}>
        <option value="python">Python</option>
        <option value="javascript">JavaScript</option>
        {/* Add more languages as supported */}
      </select>
      <br />
      <textarea
        rows="10"
        cols="70"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="Paste your code here..."
      />
      <br />
      <button type="submit">Analyze Code</button>
    </form>
  );
};

export default CodeInput; 