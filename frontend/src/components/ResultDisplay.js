import React from "react";

const ResultDisplay = ({ results }) => {
  if (!results) return null;

  return (
    <div>
      <h3>Analysis Results:</h3>
      {results.length === 0 ? (
        <p>No vulnerabilities found!</p>
      ) : (
        <ul>
          {results.map((vuln, idx) => (
            <li key={idx}>
              <strong>Line:</strong> {vuln.line} <br />
              <strong>Description:</strong> {vuln.description} <br />
              <strong>Fix:</strong>
              <pre>{vuln.suggested_fix}</pre>
              <hr />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ResultDisplay; 