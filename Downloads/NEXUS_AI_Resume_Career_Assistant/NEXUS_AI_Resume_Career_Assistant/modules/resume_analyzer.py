from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from modules.skills_extractor import extract_skills
from modules.resume_parser import extract_resume_sections


def _similarity_score(resume_text, job_description):
    if not resume_text.strip() or not job_description.strip():
        return 0
    try:
        matrix = TfidfVectorizer(stop_words="english").fit_transform(
            [resume_text, job_description]
        )
        return round(float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0]) * 100, 2)
    except ValueError:
        return 0


def analyze_resume(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    resume_set = {skill.lower() for skill in resume_skills}
    matched = [skill for skill in job_skills if skill.lower() in resume_set]
    missing = [skill for skill in job_skills if skill.lower() not in resume_set]

    skill_match = round((len(matched) / len(job_skills)) * 100, 2) if job_skills else 0
    similarity = _similarity_score(resume_text, job_description)

    skill_table = [
        {"Required skill": skill,
         "Status": "Matched" if skill.lower() in resume_set else "Missing"}
        for skill in job_skills
    ]

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "skill_match": skill_match,
        "similarity": similarity,
        "skill_table": skill_table,
    }


def generate_improvement_suggestions(resume_text, missing_skills=None, matched_skills=None):
    missing_skills = missing_skills or []
    text = resume_text.lower()
    suggestions = []
    sections = extract_resume_sections(resume_text)

    if "Summary" not in sections:
        suggestions.append("Add a short professional summary tailored to the roles you are applying for.")
    if "Skills" not in sections:
        suggestions.append("Add a clearly labelled Skills or Technical Skills section.")
    if "Projects" not in sections:
        suggestions.append("Add 2–3 relevant projects and explain your individual contribution.")
    if "Experience" not in sections and "Education" in sections:
        suggestions.append("If you have internship, volunteering or practical experience, add a clearly labelled Experience section.")
    if not any(word in text for word in ["achieved", "improved", "reduced", "increased", "built", "developed", "implemented"]):
        suggestions.append("Use specific action verbs to explain what you did in projects or work experience.")
    if missing_skills:
        suggestions.append("If you genuinely have experience with these job skills, add evidence in your resume: " + ", ".join(missing_skills[:8]) + ".")
    if not any(char.isdigit() for char in resume_text):
        suggestions.append("Where accurate, include measurable project outcomes (for example users, response time or data volume). Do not invent numbers.")
    if len(resume_text.split()) < 150:
        suggestions.append("Your resume text is quite short. Add relevant project details, responsibilities and outcomes if applicable.")
    if not suggestions:
        suggestions.append("Your resume includes several standard sections. Tailor the wording and project evidence to each job description.")
    return suggestions
