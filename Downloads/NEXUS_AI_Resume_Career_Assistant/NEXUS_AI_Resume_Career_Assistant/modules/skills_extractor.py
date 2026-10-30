import re

# Extend this dictionary as your project grows.
SKILL_ALIASES = {
    "Python": ["python", "python3"],
    "Java": ["java"],
    "C++": ["c++", "cpp"],
    "C": ["c programming", " c language"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    "React": ["react", "react.js"],
    "Node.js": ["node.js", "nodejs"],
    "Express": ["express.js", "express"],
    "Streamlit": ["streamlit"],
    "Flask": ["flask"],
    "Django": ["django"],
    "FastAPI": ["fastapi"],
    "SQL": ["sql", "structured query language"],
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MongoDB": ["mongodb", "mongo db"],
    "SQLite": ["sqlite"],
    "DBMS": ["dbms", "database management system"],
    "Git": ["git"],
    "GitHub": ["github"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["microsoft azure", "azure"],
    "GCP": ["google cloud", "gcp"],
    "Linux": ["linux"],
    "REST API": ["rest api", "restful api", "rest apis"],
    "GraphQL": ["graphql"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning"],
    "NLP": ["natural language processing", "nlp"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Power BI": ["power bi"],
    "Tableau": ["tableau"],
    "Excel": ["microsoft excel", "excel"],
    "Figma": ["figma"],
    "Agile": ["agile"],
    "OOP": ["object oriented programming", "oop"],
}


def _contains_term(text, term):
    """Match phrases without accidentally matching inside unrelated words."""
    pattern = r"(?<![a-z0-9])" + re.escape(term.lower().strip()) + r"(?![a-z0-9])"
    return re.search(pattern, text.lower()) is not None


def extract_skills(text):
    if not text:
        return []
    found = []
    for canonical, aliases in SKILL_ALIASES.items():
        if any(_contains_term(text, alias) for alias in aliases):
            found.append(canonical)
    return sorted(found, key=str.lower)
