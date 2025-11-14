import streamlit as st
from utils.layout import set_background_color, set_sidebar_style, set_custom_style, load_logo
from utils.sidebar import render_sidebar

# === PAGE SETUP (must be first!) ===
st.set_page_config(page_title="Parslyst", page_icon="📄", layout="wide")

# === Apply Layout & Styling ===
set_background_color("#0d3f4c")
set_custom_style()
set_sidebar_style()
render_sidebar()
load_logo()

# === Optional Welcome Message ===
st.title("👋 Welcome to Parslyst")
st.markdown("Navigate using the sidebar to begin parsing or ranking resumes.")
