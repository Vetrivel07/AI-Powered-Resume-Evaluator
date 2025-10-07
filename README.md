# AI-Powered Resume Evaluator

The AI-Powered Resume Evaluator automatically reviews a candidate’s resume (PDF) against a given job description using Google Gemini 2.5 Flash.
It simulates both a human recruiter and an Applicant Tracking System (ATS) to evaluate how well a resume matches the job role.
The app provides a detailed report including job expectations, resume alignment, match percentage, and professional feedback — all in real time through a clean Streamlit web interface.


## 🚀 Features

- 📄 Upload PDF resume and paste job description
- 🧠 Uses Gemini Flash 2.5 for multimodal reasoning (reads PDFs directly)
- 🧾 Returns 4-section detailed report
    - About the Job
    - Your Resume
    - Match Percentage
    - Summary & Feedback
- 🔍 Emphasizes experience, skills, and projects
- 🔒 Automatically deletes uploaded files after analysis
- 🎨 Includes custom CSS styling and inline colored “loading” indicator
- ⚡ Lightweight, single-file deployable Streamlit app


## 📦 Tech Stack

| Layer                | Technology              | Purpose                             |
| -------------------- | ----------------------- | ----------------------------------- |
| **Frontend / UI**    | Streamlit               | Interactive web interface           |
| **Backend / Logic**  | Python 3.9+             | Workflow and LLM orchestration      |
| **LLM Engine**       | Google Gemini 2.5 Flash | Core multimodal model (text + PDF)  |
| **Environment Mgmt** | python-dotenv           | Secure API-key handling             |
| **Styling**          | Custom CSS              | UI consistency and branding         |
| **Optional Libs**    | pillow, pdf2image       | Image/PDF preprocessing (if needed) |



## 📁 Project Structure

```
User
 ├── Upload Resume (PDF)
 ├── Paste Job Description
 ▼
[ Streamlit UI ]
 ├── Build Prompt + PDF Handle
 ▼
[ Gemini Flash Model ]
 ├── Compare Resume ↔ JD
 ├── Generate JSON Output
 ▼
[ Streamlit Renderer ]
 ├── Parse JSON → Show 4 Sections
 ├── Delete Uploaded File
 ▼
Result: ATS-style evaluation

```

## 📸 Screenshots

![Index](static/Index.png)

## ⚙️ Environment Setup

### Create Virtual Environment
```
python -m venv venv
source venv/bin/activate      # (Windows: venv\Scripts\activate)
```

### Install Dependencies
```
pip install streamlit google-generativeai python-dotenv pillow pdf2image
```

### Run the App
```
streamlit run app.py
```

## Author

👤 **[Vetrivel Maheswaran](https://github.com/Vetrivel07)**

## Connect With Me 🌐

**[![LinkedIn](https://img.shields.io/badge/LinkedIn-Vetrivel%20Maheswaran-green)](https://www.linkedin.com/in/vetrivel-maheswaran/)**

**[![PortFolio](https://img.shields.io/badge/Portfolio-Vetrivel%20Maheswaran-blue)](https://vetrivel07.github.io/vetrivel-maheswaran)**

<p align="center"><b>© Created by Vetrivel Maheswaran</b></p?
