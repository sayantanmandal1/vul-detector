# LLM-Based Vulnerability Detection Platform

## 🚀 Overview

A world-class, end-to-end platform for detecting vulnerabilities and malicious code in open-source software repositories using Large Language Models (LLMs), static analysis, and CVE/CWE mapping. This tool is designed for security researchers, developers, and organizations to automatically scan GitHub repositories, identify vulnerabilities, and generate actionable mitigation reports (including PDF downloads).

---

## 🏆 Key Features

- **LLM-Augmented Vulnerability Detection**: Uses OpenAI to suggest secure code fixes and explanations.
- **Multi-Language Support**: Python, JavaScript, Java, C, C++, HTML, CSS (easily extensible).
- **GitHub Repo Scanning**: Clone and recursively scan any public GitHub repository.
- **Static & Pattern-Based Analysis**: Combines AST parsing (Tree-sitter) and regex for deep code inspection.
- **CVE/CWE Mapping**: Maps detected patterns to known vulnerabilities using open databases.
- **Automated Mitigation**: Generates detailed, context-aware fix suggestions.
- **Professional Reports**: Download results as JSON, text, HTML, or PDF.
- **Modern Frontend**: React UI with code/repo analysis, progress tracking, and report downloads.
- **Extensible & Modular**: Easily add new languages, rules, or report formats.

---

## 📦 Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/                # FastAPI routes
│   │   ├── core/               # Configs & constants
│   │   ├── data/               # CVE/CWE mapping data
│   │   ├── models/             # Pydantic models
│   │   ├── services/           # Analysis, scanning, reporting
│   │   ├── utils/              # Utilities
│   │   └── main.py             # FastAPI entry point
│   ├── requirements.txt        # Backend dependencies
│   ├── .env                    # API keys & config
│   └── tests/                  # Pytest test suite
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── App.js              # Main app
│   │   └── ...
│   ├── package.json            # Frontend dependencies
│   └── ...
└── README.md                   # This file
```

---

## 🛠️ Setup & Installation

### 1. **Clone the Repository**
```bash
git clone https://github.com/sayantanmandal1/vul-detector.git
cd llm-vuln-detector
```

### 2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### **Clone Tree-sitter Grammars**
```bash
cd app/services
# Required grammars for all supported languages
for repo in tree-sitter-python tree-sitter-c tree-sitter-cpp tree-sitter-javascript tree-sitter-java; do
  git clone https://github.com/tree-sitter/$repo.git
  done
cd ../../../
```

#### **.env Configuration**
Create a `backend/.env` file:
```
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-3.5-turbo
```

### 3. **Frontend Setup**
```bash
cd ../frontend
npm install
```

---

## 🚦 Running the App

### **Start the Backend**
```bash
cd backend
uvicorn app.main:app --reload
```

### **Start the Frontend**
```bash
cd frontend
npm start
```

---

## 🌐 Usage

### **Analyze a GitHub Repository**
1. Open the frontend in your browser (usually at `http://localhost:3000`).
2. Paste a public GitHub repository URL (e.g., `https://github.com/username/repo`).
3. Click **Analyze Repository**.
4. View vulnerabilities, suggested fixes, and download reports (JSON, text, HTML, PDF).

### **Analyze a Code Snippet**
1. Switch to the **Code Analysis** tab.
2. Paste your code and select the language.
3. Click **Analyze Code**.

---

## 🧠 Architecture & Workflow

1. **Frontend** (React):
    - User submits GitHub repo URL or code snippet.
    - Shows progress, results, and allows report downloads.
2. **Backend** (FastAPI):
    - Clones repo, walks files, detects language.
    - Runs static analysis (Tree-sitter for code, regex for HTML/CSS).
    - Maps findings to CVEs/CWEs.
    - Calls OpenAI for mitigation suggestions.
    - Generates and returns detailed reports.
3. **Reporting**:
    - Reports can be downloaded in JSON, text, HTML, or PDF formats.

---

## 🔍 Supported Vulnerabilities

- **Code Injection**: `eval`, `exec`, `Function`, `os.system`, etc.
- **SQL Injection**: `execute`, `cursor.execute`, `query`, `mysql_query`, etc.
- **Insecure Deserialization**: `pickle.loads`, `yaml.load`, `ObjectInputStream`, `JSON.parse`
- **Hardcoded Secrets**: `password`, `api_key`, `secret`, `token` patterns
- **XSS**: `<script>`, `onerror=`, `onclick=`, `javascript:` in HTML/JS
- **Buffer Overflows**: `gets`, `strcpy`, `strcat`, `sprintf`
- **Command Injection**: `os.system`, `Runtime.getRuntime().exec`
- **And more...** (easily extensible)

---

## 📚 Data Sources
- [CVE Details](https://cvedetails.com/)
- [CWE List](https://cwe.mitre.org/data/definitions/1000.html)
- [SARD](https://samate.nist.gov/SARD/)
- [VulnCode-DB](https://github.com/google/vulncode-db)
- [Juliet Test Suite](https://samate.nist.gov/SRD/testsuite.php)

---

## 🏗️ Extending the Platform
- **Add new languages**: Clone the Tree-sitter grammar, add to loader and rules.
- **Add new rules**: Update `vuln_rules.py` with new patterns.
- **Add new report formats**: Extend `report_generator.py`.
- **Integrate more LLMs**: Swap OpenAI for other providers via `.env`.

---

## 🤝 Contributing

1. Fork the repo and create your branch: `git checkout -b feature/your-feature`
2. Commit your changes: `git commit -am 'Add new feature'`
3. Push to the branch: `git push origin feature/your-feature`
4. Open a Pull Request

---

## 🛡️ Security & Disclaimer
- **Never share your OpenAI API key.**
- This tool is for educational and research purposes. Always review findings before acting on them in production.

---

## 📧 Contact & Support
- **Author:** [Sayantan Mandal]
- **Email:** msayantan05@gmail.com
- **Issues:** [GitHub Issues](https://github.com/sayantanmandal1/vul-detector/issues)

---

## ⭐ Acknowledgements
- OpenAI, Tree-sitter, FastAPI, React, ReportLab, WeasyPrint, and the open-source security community. 