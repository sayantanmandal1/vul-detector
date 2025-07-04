import React, { useState } from 'react';
import './CodeInput.css';

const CodeInput = ({ onAnalyze }) => {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!code.trim()) {
      alert('Please enter some code to analyze');
      return;
    }
    onAnalyze(code, language);
  };

  const exampleCode = {
    python: `# Example vulnerable Python code
user_input = input("Enter your name: ")
eval(user_input)  # Dangerous!

import os
os.system("rm -rf /")  # Very dangerous!

import pickle
data = pickle.loads(user_input)  # Insecure deserialization`,
    
    javascript: `// Example vulnerable JavaScript code
const userInput = prompt("Enter your name:");
eval(userInput);  // Dangerous!

document.getElementById("output").innerHTML = userInput;  // XSS vulnerability

const data = JSON.parse(userInput);  // Potential injection`,
    
    java: `// Example vulnerable Java code
import java.lang.reflect.Method;

String userInput = request.getParameter("input");
Class.forName(userInput);  // Dangerous reflection

Runtime.getRuntime().exec(userInput);  // Command injection`,
    
    c: `// Example vulnerable C code
#include <stdio.h>
#include <string.h>

char buffer[100];
gets(buffer);  // Buffer overflow vulnerability

strcpy(buffer, userInput);  // Another buffer overflow

sprintf(buffer, userInput);  // Format string vulnerability`,
    
    cpp: `// Example vulnerable C++ code
#include <iostream>
#include <string>

std::string userInput;
std::cin >> userInput;

system(userInput.c_str());  // Command injection

char* buffer = new char[100];
strcpy(buffer, userInput.c_str());  // Buffer overflow`
  };

  const loadExample = () => {
    setCode(exampleCode[language] || '');
  };

  return (
    <div className="code-input">
      <div className="input-header">
        <h2>📝 Code Vulnerability Analyzer</h2>
        <p>Analyze individual code snippets for security vulnerabilities</p>
      </div>

      <form onSubmit={handleSubmit} className="code-form">
        <div className="form-row">
          <div className="input-group">
            <label htmlFor="language">Programming Language:</label>
            <select
              id="language"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="language-select"
            >
              <option value="python">Python</option>
              <option value="javascript">JavaScript</option>
              <option value="java">Java</option>
              <option value="c">C</option>
              <option value="cpp">C++</option>
            </select>
          </div>
          
          <button
            type="button"
            onClick={loadExample}
            className="example-btn"
          >
            📋 Load Example
          </button>
        </div>

        <div className="input-group">
          <label htmlFor="code">Code to Analyze:</label>
          <textarea
            id="code"
            rows="15"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="Paste your code here to analyze for security vulnerabilities..."
            className="code-textarea"
            required
          />
        </div>

        <button type="submit" className="analyze-btn">
          🔍 Analyze Code
        </button>
      </form>

      <div className="features">
        <h3>Supported vulnerability types:</h3>
        <ul>
          <li>🚨 Code Injection (eval, exec, system calls)</li>
          <li>🌐 Cross-Site Scripting (XSS)</li>
          <li>💾 SQL Injection</li>
          <li>🔓 Buffer Overflows</li>
          <li>🔐 Insecure Deserialization</li>
          <li>🔑 Hardcoded Secrets</li>
          <li>📝 Format String Vulnerabilities</li>
        </ul>
      </div>
    </div>
  );
};

export default CodeInput; 