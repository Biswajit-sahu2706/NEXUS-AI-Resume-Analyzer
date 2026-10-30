import streamlit as st
import pandas as pd

from modules.resume_parser import (
    extract_resume_text, extract_email, extract_phone,
    extract_candidate_name, extract_resume_sections
)
from modules.skills_extractor import extract_skills
from modules.resume_analyzer import analyze_resume, generate_improvement_suggestions
from modules.ats_checker import check_ats
from modules.interview_generator import generate_interview_questions
from modules.report_generator import create_pdf_report


st.set_page_config(
    page_title="NEXUS AI | Resume & Career Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- THEME --------------------
st.markdown("""
<style>
.stApp { background:#101B2D; color:#E8EFF7; }
header[data-testid="stHeader"] { background:#101B2D; }
[data-testid="stSidebar"] { background:#17283D; border-right:1px solid #30465C; }
[data-testid="stSidebar"] * { color:#E8EFF7; }
h1,h2,h3,h4 { color:#E8EFF7 !important; }
p,label { color:#C6D5E4; }
.hero { background:linear-gradient(110deg,#19364E,#173D50);
        border:1px solid #326579; border-radius:16px; padding:25px; margin-bottom:20px; }
.hero-title { color:#5CE0E6; font-size:29px; font-weight:800; }
.hero-subtitle { color:#C5D8E8; font-size:15px; }
.brand { font-size:24px; font-weight:800; color:#55D6DF; padding:10px 0; }
div[data-testid="stMetric"] { background:#1B3047; border:1px solid #34536B;
    border-radius:12px; padding:15px; }
div[data-testid="stMetric"] label { color:#B9CDDF !important; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color:#55D6DF; }
div[data-testid="stVerticalBlockBorderWrapper"] {
    background:#17283D; border-color:#34536B; border-radius:12px; }
.stTextArea textarea,.stTextInput input {
    background:#17283D !important; color:#E8EFF7 !important;
    border:1px solid #456078 !important; border-radius:9px !important; }
.stButton > button { background:#167F91; color:white; border:1px solid #35C6D0;
    border-radius:8px; min-height:42px; font-weight:650; }
.stButton > button:hover { background:#1C9EAD; color:white; }
.stDownloadButton > button { background:#176D68; color:white;
    border:1px solid #43BFA0; border-radius:9px; }
hr { border-color:#30465C; }
.footer { text-align:center; color:#8FA7BD; padding:22px;
    border-top:1px solid #30465C; margin-top:25px; }
</style>
""", unsafe_allow_html=True)

# -------------------- SESSION STATE --------------------
defaults = {
    "resume_text": "",
    "resume_name": "",
    "analysis": None,
    "ats_result": None,
    "job_description": "",
    "applications": [],
    "interview_questions": [],
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def load_resume(uploaded_file):
    """Extract a PDF/DOCX resume and reset old analysis when file changes."""
    if uploaded_file is None:
        return
    if uploaded_file.name == st.session_state.resume_name:
        return
    try:
        text = extract_resume_text(uploaded_file)
        if not text.strip():
            st.error("No readable text found. This may be a scanned PDF; OCR is not enabled.")
            return
        st.session_state.resume_text = text
        st.session_state.resume_name = uploaded_file.name
        st.session_state.analysis = None
        st.session_state.ats_result = None
        st.session_state.interview_questions = []
        st.success("Resume uploaded and text extracted successfully.")
    except Exception as exc:
        st.error(f"Could not read this file: {exc}")


def show_tags(items):
    if items:
        st.write(" · ".join(str(item) for item in items))
    else:
        st.caption("None detected.")


def render_ats(result):
    st.subheader("ATS compatibility check")
    a, b, c = st.columns(3)
    a.metric("ATS readiness score", f"{result['score']}/100")
    b.metric("Checks passed", f"{result['passed']}/{result['total']}")
    c.metric("Needs attention", len(result["issues"]))
    st.progress(result["score"] / 100)
    st.caption("This is a heuristic checklist, not a score from a real employer's ATS.")
    table = pd.DataFrame(result["checks"])
    st.dataframe(table, use_container_width=True, hide_index=True)
    if result["issues"]:
        st.markdown("**Recommended fixes**")
        for issue in result["issues"]:
            st.warning(issue)
    else:
        st.success("All checks in this basic checklist passed.")


def make_report_text():
    analysis = st.session_state.analysis or {}
    ats = st.session_state.ats_result or {}
    return f"""NEXUS AI - RESUME & CAREER ANALYSIS REPORT

Resume: {st.session_state.resume_name}
Candidate: {extract_candidate_name(st.session_state.resume_text) or 'Not detected'}
Email: {extract_email(st.session_state.resume_text) or 'Not detected'}
Phone: {extract_phone(st.session_state.resume_text) or 'Not detected'}

SKILL MATCH: {analysis.get('skill_match', 'Not analyzed')}%
TEXT SIMILARITY: {analysis.get('similarity', 'Not analyzed')}%
ATS READINESS: {ats.get('score', 'Not analyzed')}/100

MATCHED SKILLS:
{', '.join(analysis.get('matched_skills', []))}

MISSING SKILLS:
{', '.join(analysis.get('missing_skills', []))}

IMPROVEMENT SUGGESTIONS:
{chr(10).join('- ' + x for x in analysis.get('suggestions', []))}

ATS ISSUES:
{chr(10).join('- ' + x for x in ats.get('issues', []))}

DISCLAIMER:
Scores are heuristic estimates for guidance only. They do not guarantee
shortlisting or represent the scoring system of any employer's ATS.
"""


# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown('<div class="brand">⚡ NEXUS AI</div>', unsafe_allow_html=True)
    st.caption("RESUME & CAREER ASSISTANT")
    st.divider()
    page = st.radio(
        "Workspace",
        ["Dashboard", "My Resume", "Job Analysis", "ATS Checker",
         "AI Suggestions", "Interview Preparation", "My Applications", "About"],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("### ANALYSIS ENGINE")
    st.caption("🟢 PDF / DOCX Parser")
    st.caption("🟢 NLP Skill Extraction")
    st.caption("🟢 Job Matching")
    st.caption("🟢 ATS Checklist")
    st.caption("🟢 Interview Question Generator")
    st.divider()
    st.caption("Built with Python + Streamlit")


# -------------------- DASHBOARD --------------------
if page == "Dashboard":
    st.markdown("""
    <div class="hero">
      <div class="hero-title">⚡ Welcome to NEXUS AI</div>
      <div class="hero-subtitle">
        Understand your resume, identify skill gaps, check ATS basics,
        and prepare for your next interview.
      </div>
    </div>
    """, unsafe_allow_html=True)

    x, y, z = st.columns(3)
    x.metric("Resume", "Uploaded" if st.session_state.resume_text else "Not uploaded")
    y.metric("Saved analyses", len(st.session_state.applications))
    z.metric("Latest analysis", "Ready" if st.session_state.analysis else "Pending")

    st.subheader("Your career workflow")
    cards = [
        ("📄 Upload Resume", "Extract candidate details and skills."),
        ("🎯 Match a Job", "Compare your resume with a job description."),
        ("🧾 Check ATS Basics", "Review headings, contact details and readability."),
        ("🧠 Improve & Prepare", "Get practical suggestions and interview questions."),
    ]
    cols = st.columns(2)
    for i, (title, desc) in enumerate(cards):
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.write(desc)

    st.info("Start in **My Resume** by uploading a PDF or DOCX file.")


# -------------------- MY RESUME --------------------
elif page == "My Resume":
    st.title("📄 My Resume")
    st.write("Upload a text-based PDF or Word document.")
    uploaded = st.file_uploader("Choose resume", type=["pdf", "docx"], key="main_resume")
    load_resume(uploaded)

    if st.session_state.resume_text:
        text = st.session_state.resume_text
        st.success(f"Active file: {st.session_state.resume_name}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Candidate", extract_candidate_name(text) or "Not detected")
        c2.metric("Email", extract_email(text) or "Not detected")
        c3.metric("Phone", extract_phone(text) or "Not detected")

        st.subheader("Detected skills")
        show_tags(extract_skills(text))

        st.subheader("Detected resume sections")
        sections = extract_resume_sections(text)
        if sections:
            st.write(" · ".join(sections.keys()))
        else:
            st.info("No standard section headings detected yet.")

        with st.expander("View extracted resume text"):
            st.text_area("Extracted text", text, height=300, disabled=True)
    else:
        st.info("No resume uploaded yet.")


# -------------------- JOB ANALYSIS --------------------
elif page == "Job Analysis":
    st.title("🎯 Resume and Job Compatibility")
    st.write("Upload your resume and paste the job description.")
    uploaded = st.file_uploader("Upload resume", type=["pdf", "docx"], key="job_resume")
    load_resume(uploaded)

    job = st.text_area(
        "Job description",
        value=st.session_state.job_description,
        height=220,
        placeholder="Paste the full job description, including responsibilities and required skills...",
    )

    if st.button("⚡ Analyze Resume", type="primary", use_container_width=True):
        if not st.session_state.resume_text:
            st.error("Upload a resume first.")
        elif not job.strip():
            st.error("Paste a job description first.")
        else:
            with st.spinner("Analyzing resume and job description..."):
                st.session_state.job_description = job
                result = analyze_resume(st.session_state.resume_text, job)
                result["suggestions"] = generate_improvement_suggestions(
                    st.session_state.resume_text,
                    result["missing_skills"],
                    result["matched_skills"],
                )
                st.session_state.analysis = result
                st.session_state.ats_result = check_ats(st.session_state.resume_text)
                st.session_state.interview_questions = generate_interview_questions(
                    job, result["matched_skills"], result["missing_skills"]
                )
            st.success("Analysis completed.")

    result = st.session_state.analysis
    if result:
        st.divider()
        st.subheader("Analysis overview")
        a, b, c = st.columns(3)
        a.metric("Skill match", f"{result['skill_match']}%")
        b.metric("Text similarity", f"{result['similarity']}%")
        c.metric("Missing skills", len(result["missing_skills"]))
        st.caption("Skill match is based on detected skills. Text similarity is a separate TF-IDF estimate.")
        st.progress(min(max(result["skill_match"] / 100, 0), 1))

        left, right = st.columns(2)
        with left:
            with st.container(border=True):
                st.markdown("**🟢 Matched skills**")
                show_tags(result["matched_skills"])
        with right:
            with st.container(border=True):
                st.markdown("**🔴 Missing skills**")
                show_tags(result["missing_skills"])

        st.subheader("Skill-by-skill report")
        st.dataframe(pd.DataFrame(result["skill_table"]), use_container_width=True, hide_index=True)

        if st.session_state.ats_result:
            render_ats(st.session_state.ats_result)

        st.subheader("Suggested improvements")
        for item in result["suggestions"]:
            st.info(item)

        with st.expander("Candidate details"):
            st.write("**Name:**", extract_candidate_name(st.session_state.resume_text) or "Not detected")
            st.write("**Email:**", extract_email(st.session_state.resume_text) or "Not detected")
            st.write("**Phone:**", extract_phone(st.session_state.resume_text) or "Not detected")

        job_title = st.text_input("Label this analysis (e.g. Python Developer - ABC Ltd)")
        if st.button("Save this analysis"):
            if job_title.strip():
                st.session_state.applications.append({
                    "Job": job_title.strip(),
                    "Resume": st.session_state.resume_name,
                    "Skill match": f"{result['skill_match']}%",
                    "ATS score": f"{st.session_state.ats_result['score']}/100",
                })
                st.success("Analysis saved in this session.")
            else:
                st.warning("Enter a job title or company name.")


# -------------------- ATS CHECKER --------------------
elif page == "ATS Checker":
    st.title("🧾 ATS Resume Checker")
    st.write("Check basic resume structure and text readability.")
    uploaded = st.file_uploader("Upload resume", type=["pdf", "docx"], key="ats_resume")
    load_resume(uploaded)
    if st.session_state.resume_text:
        result = check_ats(st.session_state.resume_text)
        st.success(f"Checking: {st.session_state.resume_name}")
        render_ats(result)
        st.caption("Tip: use standard headings such as Summary, Skills, Experience, Education and Projects.")
    else:
        st.info("Upload a resume to run the ATS checklist.")


# -------------------- AI SUGGESTIONS --------------------
elif page == "AI Suggestions":
    st.title("✨ Resume Improvement Suggestions")
    st.write("Get practical suggestions based on the content detected in your resume.")
    uploaded = st.file_uploader("Upload resume", type=["pdf", "docx"], key="suggest_resume")
    load_resume(uploaded)
    if st.session_state.resume_text:
        text = st.session_state.resume_text
        skills = extract_skills(text)
        ats = check_ats(text)
        suggestions = generate_improvement_suggestions(text, [], skills)
        st.subheader("Detected skills")
        show_tags(skills)
        st.subheader("Suggestions")
        for suggestion in suggestions:
            st.info(suggestion)
        st.subheader("ATS checklist")
        render_ats(ats)
        st.warning("Review every suggestion. Do not add skills, metrics or achievements that are not true.")
    else:
        st.info("Upload your resume to receive suggestions.")


# -------------------- INTERVIEW PREPARATION --------------------
elif page == "Interview Preparation":
    st.title("🎤 Interview Preparation")
    st.write("Generate practice questions from a job description and detected skills.")
    uploaded = st.file_uploader("Upload resume (optional)", type=["pdf", "docx"], key="interview_resume")
    load_resume(uploaded)
    job = st.text_area("Paste job description", height=180, key="interview_job")
    if st.button("Generate interview questions", type="primary"):
        if not job.strip():
            st.warning("Paste a job description first.")
        else:
            skills = extract_skills(st.session_state.resume_text) if st.session_state.resume_text else []
            job_skills = extract_skills(job)
            missing = [s for s in job_skills if s.lower() not in {x.lower() for x in skills}]
            st.session_state.interview_questions = generate_interview_questions(job, skills, missing)
    if st.session_state.interview_questions:
        st.subheader("Practice questions")
        for i, question in enumerate(st.session_state.interview_questions, 1):
            with st.expander(f"Question {i}"):
                st.write(question)
                st.text_area("Your practice answer", key=f"answer_{i}", height=90)


# -------------------- APPLICATIONS --------------------
elif page == "My Applications":
    st.title("📁 My Applications")
    if st.session_state.applications:
        df = pd.DataFrame(st.session_state.applications)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button("Download CSV", df.to_csv(index=False), "nexus_applications.csv", "text/csv")
        if st.button("Clear session history"):
            st.session_state.applications = []
            st.rerun()
    else:
        st.info("No saved analyses in this browser session yet. Run a Job Analysis and save it.")


# -------------------- ABOUT --------------------
elif page == "About":
    st.title("🤖 About NEXUS AI")
    st.write(
        "NEXUS AI is a resume and career assistant prototype. It extracts text, "
        "detects skills, compares resume content with a job description, checks "
        "basic ATS-friendly practices and creates interview practice questions."
    )
    st.subheader("Technology stack")
    st.write("Python · Streamlit · PDFPlumber · python-docx · Pandas · Scikit-learn · TF-IDF")
    st.subheader("Current limitations")
    st.write(
        "- Scanned PDFs need OCR, which is not included.\n"
        "- Skill detection uses a configurable keyword dictionary.\n"
        "- ATS checks are general heuristics, not a real employer ATS score.\n"
        "- Analysis history is stored in Streamlit session state, not a permanent database.\n"
        "- Suggestions are rule-based; no external generative AI API is connected."
    )
    st.subheader("Privacy")
    st.write("This starter project processes uploaded files in the running app. Add secure storage, deletion controls and access control before deploying for public use.")


# -------------------- REPORT DOWNLOADS --------------------
if page in ["Job Analysis", "ATS Checker", "AI Suggestions"] and st.session_state.resume_text:
    if st.session_state.analysis or st.session_state.ats_result:
        st.divider()
        st.subheader("Download your report")
        report_text = make_report_text()
        st.download_button(
            "📥 Download text report",
            report_text,
            file_name="NEXUS_AI_Resume_Report.txt",
            mime="text/plain",
        )
        try:
            pdf_bytes = create_pdf_report(report_text)
            st.download_button(
                "📄 Download PDF report",
                pdf_bytes,
                file_name="NEXUS_AI_Resume_Report.pdf",
                mime="application/pdf",
            )
        except Exception as exc:
            st.warning(f"PDF report could not be generated: {exc}")


st.markdown("""
<div class="footer">
  ⚡ NEXUS AI — Intelligent Resume & Career Assistant<br>
  Built with Python · Streamlit · NLP
</div>
""", unsafe_allow_html=True)
