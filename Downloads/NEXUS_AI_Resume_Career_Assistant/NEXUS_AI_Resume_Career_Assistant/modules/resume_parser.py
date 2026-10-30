import re
import pdfplumber
from docx import Document


def extract_resume_text(uploaded_file):
    """Extract text from a PDF or DOCX Streamlit UploadedFile."""
    filename = uploaded_file.name.lower()
    uploaded_file.seek(0)

    if filename.endswith(".pdf"):
        pages = []
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                pages.append(page.extract_text() or "")
        return "\n".join(pages).strip()

    if filename.endswith(".docx"):
        document = Document(uploaded_file)
        parts = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
        for table in document.tables:
            for row in table.rows:
                parts.append(" | ".join(cell.text.strip() for cell in row.cells))
        return "\n".join(parts).strip()

    raise ValueError("Unsupported file type. Upload PDF or DOCX.")


def extract_email(text):
    match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text)
    return match.group(0) if match else None


def extract_phone(text):
    candidates = re.findall(r"(?:\+?\d[\d\s().-]{7,}\d)", text)
    for candidate in candidates:
        digits = re.sub(r"\D", "", candidate)
        if 10 <= len(digits) <= 13:
            return candidate.strip()
    return None


def extract_candidate_name(text):
    """A conservative heuristic: inspect the first non-empty lines."""
    ignored = ("resume", "curriculum vitae", "cv", "email", "phone", "mobile",
               "linkedin", "github", "portfolio", "address")
    for line in text.splitlines()[:8]:
        cleaned = re.sub(r"[^A-Za-z .'-]", "", line).strip()
        words = cleaned.split()
        if 2 <= len(words) <= 4 and not any(x in cleaned.lower() for x in ignored):
            if all(len(word) > 1 for word in words):
                return cleaned
    return None


SECTION_ALIASES = {
    "Summary": ["summary", "professional summary", "profile", "career objective", "objective"],
    "Skills": ["skills", "technical skills", "core skills", "technical expertise"],
    "Experience": ["experience", "work experience", "professional experience", "employment history"],
    "Education": ["education", "academic background", "qualification", "qualifications"],
    "Projects": ["projects", "personal projects", "academic projects"],
    "Certifications": ["certifications", "certificates", "licenses"],
}


def extract_resume_sections(text):
    found = {}
    for standard_name, aliases in SECTION_ALIASES.items():
        for line in text.splitlines():
            normalized = re.sub(r"[^a-z ]", "", line.lower()).strip()
            if normalized in aliases:
                found[standard_name] = line.strip()
                break
    return found
