# NEXUS AI – Resume & Career Assistant

A Python + Streamlit project that extracts resume text, detects skills, compares a resume with a job description, performs a basic ATS-readiness checklist, suggests improvements and generates interview practice questions.

## Features

- PDF and DOCX resume text extraction
- Candidate email and phone detection
- Configurable technical skill dictionary
- Resume/job skill matching
- TF-IDF and cosine-similarity text comparison
- Heuristic ATS-readiness checklist
- Rule-based resume improvement suggestions
- Job-specific interview practice questions
- TXT, PDF and CSV downloads
- Dark developer-oriented Streamlit interface

## Project structure

```text
NEXUS_AI_Resume_Career_Assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── modules/
│   ├── __init__.py
│   ├── resume_parser.py
│   ├── skills_extractor.py
│   ├── resume_analyzer.py
│   ├── ats_checker.py
│   ├── interview_generator.py
│   └── report_generator.py
└── sample_resumes/
```

## Windows setup

Open PowerShell in the project folder.

### 1. Create a virtual environment

```powershell
python -m venv venv
```

### 2. Activate it

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Run the application

```powershell
python -m streamlit run app.py
```

Open the local URL printed in the terminal, usually:

`http://localhost:8501`

## How to use

1. Open **My Resume** and upload a PDF or DOCX resume.
2. Open **Job Analysis** and paste a job description.
3. Select **Analyze Resume**.
4. Review skill match, missing skills, text similarity and ATS checks.
5. Open **AI Suggestions** for improvement ideas.
6. Open **Interview Preparation** to generate practice questions.
7. Download your report.

## Important limitations

- Scanned/image-only PDFs are not OCR processed. Use a text-based PDF or add an OCR engine.
- Skill extraction is dictionary/keyword based. Add relevant aliases in `modules/skills_extractor.py`.
- TF-IDF similarity is a text-overlap estimate, not a semantic understanding score.
- ATS readiness is a transparent heuristic checklist, not a score from a real employer's ATS.
- Suggestions and interview questions are rule-based; no external generative AI model is connected.
- Application history uses Streamlit session state and is not permanent. Add a database and authentication before offering multi-user persistent accounts.
- Do not claim or invent skills, experience, certifications or numerical achievements. Users should verify every suggested change.

## Suggested next steps

1. Add OCR for scanned resumes.
2. Add sentence embeddings for semantic matching.
3. Add an LLM API with user consent for grounded rewrite suggestions.
4. Add SQLite/PostgreSQL persistence and secure authentication.
5. Add automated tests and deploy the application.
