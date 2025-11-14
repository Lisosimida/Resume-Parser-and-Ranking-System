import streamlit as st
import pandas as pd
import numpy as np
import PyPDF2
from docx import Document
import joblib
import base64
import spacy
from spacy.matcher import Matcher
import re
from pyresparser import ResumeParser
import tempfile
import os
from utils.sidebar import render_sidebar
from utils.layout import set_background_color, load_logo, set_sidebar_style, set_custom_style

st.set_page_config(page_title="HR Ranking System", page_icon="📊", layout="wide")

# Apply layout
set_background_color("#0d3f4c")
set_custom_style()
set_sidebar_style()
render_sidebar()
load_logo()

# === Load models ===
model = joblib.load("D:\\Y3S1\\Modules\\Investigation (FYP)\\FYP SEM 1 (Code)\\Job Dataset\\src\\models\\xgboost_model.pkl")
tfidf_vectorizer = joblib.load("D:\\Y3S1\\Modules\\Investigation (FYP)\\FYP SEM 1 (Code)\\Job Dataset\\src\\models\\tfidf_vectorizer.pkl")
label_encoder = joblib.load("D:\\Y3S1\\Modules\\Investigation (FYP)\\FYP SEM 1 (Code)\\Job Dataset\\src\\models\\label_encoder.pkl")
nlp = spacy.load("en_core_web_sm")

# === Page setup ===
st.title("📊 Resume Ranking System")
st.markdown("Upload resumes and input job requirements to rank candidates based on relevance.")

# === Upload resumes ===
uploaded_files = st.file_uploader("Upload up to 100 Resumes (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

# === Job Inputs ===
st.subheader("🧾 Job Requirements")
job_title = st.text_input("Job Title")
job_description = st.text_area("Paste the job description")
required_skills = st.text_area("Required skills (comma-separated)")
qualification = st.selectbox("Required Qualification", ["BCA", "MCA", "B.Tech", "M.Tech", "MBA", "Other"])

# === Helper Functions ===
def extract_text(file):
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip() != ""])
    return ""

def clean_text(text):
    return ''.join([c.lower() if c.isalnum() or c.isspace() else ' ' for c in text])

def match_score(resume_text, job_text):
    tfidf = tfidf_vectorizer.transform([job_text, resume_text])
    return round(np.dot(tfidf[1].toarray(), tfidf[0].toarray().T).flatten()[0] * 100, 2)

def extract_name(text, file):
    suffix = ".pdf" if file.type == "application/pdf" else ".docx"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file.read())
        temp_path = tmp.name

    try:
        data = ResumeParser(temp_path).get_extracted_data()
        name = data.get("name", "Not found")
    except Exception as e:
        name = "Not found"

    os.remove(temp_path)
    return name

# === Process Resumes ===
if uploaded_files:
    if not job_description or not required_skills:
        st.warning("Please fill in job description and required skills to proceed.")
    else:
        results = []
        job_input_text = f"{job_title} {job_description} {required_skills} {qualification}"

        for file in uploaded_files:
            file_bytes = file.read()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf" if file.type == "application/pdf" else ".docx") as tmp:
                tmp.write(file_bytes)
                temp_path = tmp.name

            try:
                parsed_data = ResumeParser(temp_path).get_extracted_data()
                name = parsed_data.get("name", "Not found")
            except Exception:
                name = "Not found"
            os.remove(temp_path)

            resume_text = extract_text(file)
            resume_clean = clean_text(resume_text)

            tfidf_input = tfidf_vectorizer.transform([resume_clean])
            pred = model.predict(tfidf_input)[0]
            predicted_category = label_encoder.inverse_transform([pred])[0]
            score = match_score(resume_clean, job_input_text)

            results.append({
                "Candidate Name": name,
                "File Name": file.name,
                "Predicted Category": predicted_category,
                "Match Score (%)": score
            })

        # Normalize match scores
        numeric_scores = [r['Match Score (%)'] for r in results if isinstance(r['Match Score (%)'], (int, float)) and r['Match Score (%)'] > 0]
        total_score = sum(numeric_scores)

        if total_score > 0:
            for r in results:
                if isinstance(r['Match Score (%)'], (int, float)) and r['Match Score (%)'] > 0:
                    r['Match Score (%)'] = round((r['Match Score (%)'] / total_score) * 100, 2)

        # Display top 10 ranked candidates
        st.subheader("🏆 Top 10 Ranked Candidates")
        result_df = pd.DataFrame(results).sort_values(by="Match Score (%)", ascending=False).head(10)
        st.dataframe(result_df, use_container_width=True)
else:
    st.info("Please upload resume files to start ranking.")
