import streamlit as st
from pyresparser import ResumeParser
import tempfile
import os
import PyPDF2
import joblib
import numpy as np
import base64
import re
import nltk
import random
from io import BytesIO
from docx import Document
from utils.sidebar import render_sidebar
from utils.layout import set_background_color, load_logo, set_sidebar_style, set_custom_style

import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

st.set_page_config(page_title="Resume Parsing", page_icon="📤", layout="wide")

# Apply layout
set_background_color("#0d3f4c")
set_custom_style()
set_sidebar_style()
render_sidebar()
load_logo()

# Load models
model = joblib.load("D:\\Y3S1\\Modules\\Investigation (FYP)\\FYP SEM 1 (Code)\\Job Dataset\\src\\models\\xgboost_model.pkl")
tfidf_vectorizer = joblib.load("D:\\Y3S1\\Modules\\Investigation (FYP)\\FYP SEM 1 (Code)\\Job Dataset\\src\\models\\tfidf_vectorizer.pkl")
label_encoder = joblib.load("D:\\Y3S1\\Modules\\Investigation (FYP)\\FYP SEM 1 (Code)\\Job Dataset\\src\\models\\label_encoder.pkl")

# Upload + title
def run():
    st.title("Resume Upload Page")
    # Your upload logic here

st.title("📤 Resume Parsing & Job Fit Suggestions")
st.markdown("Upload your resume to extract structured information and receive top 3 recommended job categories based on content and skills.")

uploaded_file = st.file_uploader("📎 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

# Category skill sets (same as yours)
category_keywords = {
    "IT Infrastructure": {
        "python", "java", "c++", "sql", "html", "css", "javascript", "react", "angular", "node.js",
        "express.js", "mongoDB", "flask", "django", "fastapi", "kubernetes", "docker", "linux", "devops", "git",
        "agile methodology", "scrum", "ci/cd", "cloud computing", "aws", "google cloud platform (gcp)",
        "microsoft azure", "serverless architecture", "lambda functions", "microservices", "api integration",
        "restful apis", "graphql", "socket.io", "websockets", "web development", "backend development",
        "frontend development", "full-stack development", "software development", "mobile development",
        "ios development", "android development"
    },
    "Software Development": {
        "python", "java", "c++", "c#", "ruby", "go", "javascript", "typescript", "html", "css", "react", "angular",
        "vue.js", "node.js", "flask", "django", "spring boot", "express.js", "php", "laravel", "dotnet", ".net core",
        "api development", "microservices", "docker", "kubernetes", "git", "github", "gitlab", "bitbucket",
        "agile", "scrum", "jira", "test-driven development", "unit testing", "integration testing"
    },
    "Business Operations": {
        "project management", "communication", "strategy", "business development", "sales", "product management",
        "market research", "customer development", "lean startup", "crm", "hubspot", "zendesk", "intercom",
        "microsoft dynamics", "erp systems", "sap", "oracle", "microsoft excel", "content strategy"
    },
    "Communications": {
        "content marketing", "email marketing", "social media marketing", "seo", "sem", "ppc",
        "google analytics", "facebook ads", "linkedin ads", "copywriting", "editing", "proofreading"
    },
    "Digital Marketing": {
        "digital campaigns", "email automation", "content calendar", "google ads", "facebook pixel", "tiktok ads",
        "influencer marketing", "hubspot", "semrush", "ahrefs", "buffer", "hootsuite", "campaign reporting",
        "marketing automation", "klaviyo", "mailchimp"
    },
    "Cybersecurity": {
        "cybersecurity", "network security", "firewalls", "encryption", "malware analysis",
        "penetration testing", "forensics", "incident response", "threat intelligence", "siem",
        "identity and access management", "mfa", "iam", "digital forensics", "zero trust", "vulnerability scanning"
    },
    "Law": {
        "legal research", "contract law", "corporate governance", "compliance", "regulatory frameworks",
        "intellectual property", "litigation", "civil law", "criminal law", "trademark law", "case analysis",
        "legal writing", "lexisnexis", "westlaw"
    },
    "UI/UX & Digital Design": {
        "figma", "sketch", "adobe xd", "invision", "wireframing", "prototyping", "responsive design",
        "user research", "ux/ui design", "accessibility", "interaction design", "material design",
        "illustrator", "photoshop", "adobe creative suite"
    },
    "Engineering": {
        "mechanical", "hardware", "matlab", "simulation", "design", "electrical", "robotics", "circuit design",
        "system architecture", "embedded systems", "autocad", "solidworks", "control systems", "mechatronics"
    },
    "Art & Design": {
        "adobe photoshop", "illustrator", "indesign", "figma", "sketch", "adobe premiere pro", "after effects",
        "video editing", "audio editing", "animation", "motion graphics", "wireframing", "prototyping",
        "typography", "color theory", "layout design"
    },
    "Science": {
        "data analysis", "statistics", "research", "qualitative analysis", "quantitative analysis", "spss", "r",
        "pandas", "numpy", "scikit-learn", "matplotlib", "seaborn", "data visualization", "data mining",
        "predictive analytics", "descriptive analytics", "prescriptive analytics", "nlp", "text mining"
    },
    "Healthcare": {
        "medical data analysis", "epidemiology", "clinical research", "biostatistics", "patient management",
        "electronic health records", "health informatics", "medical imaging", "ocr", "speech recognition"
    },
    "Sales and Marketing": {
        "lead generation", "salesforce", "hubspot", "customer relationship management (crm)",
        "email marketing", "digital marketing", "campaign management", "conversion rate optimization", "a/b testing"
    },
    "Social Media": {
        "social media strategy", "content planning", "hashtag research", "social media ads", "instagram analytics",
        "facebook business manager", "tiktok growth", "community management", "influencer collaboration",
        "brand engagement"
    },
    "Banking and Finance": {
        "finance", "accounting", "data warehousing", "etl", "power bi", "reporting", "analytics",
        "forecasting", "risk analysis", "compliance", "investment analysis", "financial modeling"
    },
    "Hospitality": {
        "customer support", "technical support", "ticketing systems", "servicenow", "hospitality management",
        "event planning", "reservation systems", "point of sale (pos)", "food and beverage service"
    },
    "Education": {
        "teaching", "curriculum development", "instructional design", "e-learning",
        "learning management systems", "moodle", "blackboard", "educational research", "assessment", "content creation"
    },
    "Transportation": {
        "logistics", "supply chain", "fleet management", "route optimization", "dispatching",
        "gps systems", "transportation planning", "warehouse management"
    },
    "Construction": {
        "construction management", "project planning", "autocad", "site supervision", "blueprint reading",
        "contractor coordination", "building codes", "architecture"
    },
    "Agriculture": {
        "crop management", "soil science", "irrigation", "agronomy", "precision agriculture", "farming",
        "livestock management", "sustainable agriculture", "agricultural engineering"
    },
    "Human Resources": {
        "recruitment", "hr analytics", "performance appraisal", "training & development", "payroll", "labour law",
        "compensation", "employee relations", "talent acquisition", "hrms", "interviewing", "job evaluation"
    },
    "Data & Analytics": {
        "data analysis", "sql", "power bi", "python", "r", "excel", "tableau", "dashboards", "data wrangling",
        "data cleaning", "machine learning", "statistics", "matplotlib", "seaborn", "data storytelling"
    }
}

# Fallback education keyword detection if pyresparser fails or returns empty
edu_keywords = {
    "bachelor", "master", "phd", "mba", "msc", "bsc", "m.eng", "b.eng",
    "degree", "diploma", "certificate", "associate", "graduate", "undergraduate",
    "postgraduate", "higher education", "vocational", "training", "apprenticeship",
}

def extract_text(file, file_bytes):
    if file.type == "application/pdf":
        pdf = PyPDF2.PdfReader(BytesIO(file_bytes))
        return " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(BytesIO(file_bytes))
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return ""

def parse_with_pyresparser(file_bytes, file_type):
    suffix = ".pdf" if file_type == "application/pdf" else ".docx"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file_bytes)
        temp_path = tmp.name
    try:
        parsed = ResumeParser(temp_path).get_extracted_data()
    except Exception as e:
        parsed = {"error": str(e)}
    os.remove(temp_path)
    return parsed

# Process resume
if uploaded_file:
    # ➕ Read the uploaded file into bytes
    file_bytes = uploaded_file.read()

    parsed_data = parse_with_pyresparser(file_bytes, uploaded_file.type)
    
    # ➕ Pass the bytes to extract_text()
    resume_text = extract_text(uploaded_file, file_bytes)
    resume_clean = re.sub(r'[^a-zA-Z0-9\s]', ' ', resume_text.lower())

    name = parsed_data.get("name", "Not found")
    email = parsed_data.get("email", "Not found")
    phone = parsed_data.get("mobile_number", "Not found")
    education = parsed_data.get("education", [])

    # Trigger fallback only if education is not found or is empty
    if not education or (isinstance(education, list) and not education):
        edu_matches = set()
        for match in re.findall(r'\b[\w.]+\b', resume_text.lower()):
            if match in edu_keywords:
                edu_matches.add(match)
        education = sorted(edu_matches) if edu_matches else ["Not found"]

    skills = parsed_data.get("skills", ["Not found"])

    tfidf_input = tfidf_vectorizer.transform([resume_clean])
    probs = model.predict_proba(tfidf_input)[0]
    top3_idx = np.argsort(probs)[::-1][:3]
    top3_cats = label_encoder.inverse_transform(top3_idx)
    top3_scores = [round(probs[i] * 100, 2) for i in top3_idx]

    # Display results
    st.markdown("---")
    st.subheader("📄 Parsed Resume Info")
    st.markdown(f"**👤 Name:** {name}")
    st.markdown(f"**📧 Email:** {email}")
    st.markdown(f"**📞 Phone:** {phone}")
    st.markdown(f"**🎓 Education:** `{', '.join(education)}`")
    st.markdown(f"**🛠️ Skills:** `{', '.join([s.lower() for s in skills])}`")

    st.markdown("---")
    # Confidence threshold (adjustable)
    CONFIDENCE_THRESHOLD = 50.0

    st.subheader("📌 Top 3 Predicted Job Categories")

    # Check if the top score meets minimum threshold
    if top3_scores[0] < CONFIDENCE_THRESHOLD:
        st.warning("⚠️ The resume does not strongly match any job category. Please review the resume content.")
    else:
        for i in range(3):
            st.markdown(f"### {i+1}. **{top3_cats[i]}** — *{top3_scores[i]:.2f}% confidence*")

            resume_tokens = set()
            for skill in skills:
                if isinstance(skill, str):
                    tokens = re.findall(r'\b\w+\b', skill.lower())
                    resume_tokens.update(tokens)

            category_skills_raw = category_keywords.get(top3_cats[i], set())
            category_tokens = set()
            for skill in category_skills_raw:
                category_tokens.update(re.findall(r'\b\w+\b', skill.lower()))

            matched = resume_tokens & category_tokens
            missing = category_tokens - matched

            st.markdown(f"**🔍 Why this job?**")
            st.markdown(f"- ✅ Matched skills: `{', '.join(sorted(matched)) if matched else 'None'}`")
            if missing:
                suggested_skills = random.sample(sorted(missing), k=min(5, len(missing)))
                st.markdown(f"- 💡 *To improve for this role, consider adding:* `{', '.join(suggested_skills)}`")

    st.markdown("---")
    st.subheader("📄 Resume Preview")
    if uploaded_file.type == "application/pdf":
        uploaded_file.seek(0)
        base64_pdf = base64.b64encode(uploaded_file.read()).decode("utf-8")
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        # Write the DOCX file to a temp path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(file_bytes)
            temp_path = tmp.name

        # Read the saved DOCX as binary and convert to base64
        with open(temp_path, "rb") as f:
            docx_bytes = f.read()
            base64_docx = base64.b64encode(docx_bytes).decode("utf-8")

        st.markdown("📥 **Click below to preview resume in Word**")
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{base64_docx}" download="{uploaded_file.name}" target="_blank">📄 Open Resume in Word</a>'
        st.markdown(href, unsafe_allow_html=True)

        # Optional: remove temp file
        os.remove(temp_path)

    with st.expander("🧪 Raw pyresparser Output"):
        st.json(parsed_data)
