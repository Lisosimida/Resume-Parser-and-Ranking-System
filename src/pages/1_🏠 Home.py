import streamlit as st
from utils.sidebar import render_sidebar
from utils.layout import set_background_color, load_logo, set_sidebar_style, set_custom_style
# === Title & Description ===

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

# Apply layout
set_background_color("#0d3f4c")
set_custom_style()
set_sidebar_style()
render_sidebar()
load_logo()

st.title("🏠 Welcome to the Resume Matcher System")

st.markdown("""
Welcome to the **Parslyst Resume Matcher** — a smart recruitment tool built using Natural Language Processing (NLP) and Machine Learning.

Whether you're a **candidate** looking to explore suitable job categories, or an **HR professional** seeking to efficiently screen resumes — you're in the right place. 🚀
""")

# === How it Works Section ===
st.subheader("🔧 This System Consist of 2 Main Parts: ")
st.markdown("""
            
**For HR Professionals:**
- 📤 Upload multiple resumes (PDF or DOCX format)
- 📊 Rank multiple candidates against job requirements
- 📝 Easily to scan through enormous number of CVs
            
**For Normal Users/Candidates:**
- 📥 Upload your resume (PDF or DOCX format)
- 🧠 Extract job-relevant information like:
  - Skills
  - Education
  - Contact Info
- 🏷️ Predict the top 3 job categories you fit into
- 💡 Get improvement suggestions based on missing skills
            
""")

# === Technology Section ===
st.subheader("⚙️ Powered By")
st.markdown("""
- **Streamlit** – Interactive UI  
- **Pyresparser** – Extraction of resume data 
- **Scikit-learn** – Machine Learning  
- **TF-IDF** – Text Vectorization  
""")

# === Tip or Note Section ===
with st.expander("💡 Tip: Need Help Getting Started?"):
    st.markdown("""
    Use the **sidebar** to:
    - Rank candidates based on a job description via **Candidate Ranking**
    - Upload and parse a single resume on **Resume Upload**
    
    You can return to this home page anytime by clicking **🏠 Home**.
    """)

# === Footer ===
st.markdown("---")
st.caption("Final Year Project | Asia Pacific University | Soh Guan Li | Supervisor: Justin Gilbert Alexius Silvester")
