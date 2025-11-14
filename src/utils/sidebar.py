import streamlit as st

def render_sidebar():
    st.sidebar.markdown("## 📁 Parslyst Info")

    # Welcome message or quick intro
    st.sidebar.markdown("Welcome to **Parslyst** — your intelligent resume parsing & ranking assistant!")

    # Upload format reminder (practical UX)
    st.sidebar.markdown("📌 **Supported formats:** `.pdf`, `.docx`")
    
    # Tips section
    with st.sidebar.expander("💡 Tips for Best Results"):
        st.markdown("""
        - Use clear section headers like *Education*, *Experience*, *Skills*.
        - List technical skills in bullet points.
        - Avoid using images or tables.
        - Upload resumes individually for better results.
        """)

    # Credits / Footer
    st.sidebar.markdown("---")
    st.sidebar.caption("2025 Parslyst | Final Year Project")
    st.sidebar.caption("Asia Pacific University of Technology & Innovation")
    st.sidebar.caption("Developed by Soh Guan Li | TP068671 | APU3F2408CS(DA)")