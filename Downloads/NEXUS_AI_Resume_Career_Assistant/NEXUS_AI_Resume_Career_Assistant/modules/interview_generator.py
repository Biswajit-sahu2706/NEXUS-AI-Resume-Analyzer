from modules.skills_extractor import extract_skills


def generate_interview_questions(job_description, resume_skills=None, missing_skills=None):
    resume_skills = resume_skills or []
    missing_skills = missing_skills or []
    job_skills = extract_skills(job_description)

    questions = [
        "Tell me about yourself and explain how your experience relates to this role.",
        "Walk me through one project on your resume. What problem did it solve and what was your contribution?",
        "What was the most difficult technical challenge in that project, and how did you solve it?",
        "How do you test and debug your code?",
        "How do you learn a new technology when a project requires it?",
    ]

    for skill in job_skills[:5]:
        questions.append(f"Explain your practical experience with {skill}. Where have you used it?")
    for skill in missing_skills[:3]:
        questions.append(f"This role mentions {skill}. What do you currently know about it, and how would you learn it?")
    return questions[:12]
