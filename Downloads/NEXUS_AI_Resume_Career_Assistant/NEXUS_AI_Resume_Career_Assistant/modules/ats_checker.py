import re
from modules.resume_parser import extract_email, extract_phone, extract_resume_sections


def check_ats(text):
    """A transparent, heuristic ATS-readiness checklist (not a real ATS score)."""
    words = re.findall(r"\b[\w+#.-]+\b", text)
    word_count = len(words)
    sections = extract_resume_sections(text)

    checks = []

    def add(name, passed, detail):
        checks.append({
            "Check": name,
            "Status": "Pass" if passed else "Review",
            "Details": detail,
        })

    add("Contact email", bool(extract_email(text)),
        "Email address detected." if extract_email(text) else "Add a professional email address.")
    add("Phone number", bool(extract_phone(text)),
        "Phone number detected." if extract_phone(text) else "Add a reachable phone number.")
    add("Skills section", "Skills" in sections,
        "Standard skills heading detected." if "Skills" in sections else "Add a clearly labelled Skills section.")
    add("Education section", "Education" in sections,
        "Education heading detected." if "Education" in sections else "Add an Education section.")
    add("Experience section", "Experience" in sections,
        "Experience heading detected." if "Experience" in sections else "Add Experience or relevant internship details if applicable.")
    add("Projects section", "Projects" in sections,
        "Projects heading detected." if "Projects" in sections else "Add a Projects section, especially for fresher/developer roles.")
    add("Readable text length", 150 <= word_count <= 1200,
        f"Extracted approximately {word_count} words. A useful resume is often concise; review if unusually short or long.")
    add("Bullet-like descriptions", bool(re.search(r"(^|\n)\s*[-•*]", text)),
        "Bullet points detected." if re.search(r"(^|\n)\s*[-•*]", text) else "Use concise bullet points for responsibilities and achievements.")
    add("Action-oriented wording",
        bool(re.search(r"\b(developed|built|created|implemented|designed|improved|analyzed|managed|led|automated)\b", text, re.I)),
        "Action verbs detected." if re.search(r"\b(developed|built|created|implemented|designed|improved|analyzed|managed|led|automated)\b", text, re.I) else "Use action verbs to describe your contributions.")
    add("Potentially useful metrics", bool(re.search(r"\b\d+%?\b", text)),
        "Numbers detected; verify they describe genuine outcomes." if re.search(r"\b\d+%?\b", text) else "Add truthful measurable outcomes where possible.")

    passed = sum(item["Status"] == "Pass" for item in checks)
    total = len(checks)
    score = round((passed / total) * 100) if total else 0
    issues = [f"{item['Check']}: {item['Details']}" for item in checks if item["Status"] != "Pass"]

    return {
        "score": score,
        "passed": passed,
        "total": total,
        "checks": checks,
        "issues": issues,
        "word_count": word_count,
    }
