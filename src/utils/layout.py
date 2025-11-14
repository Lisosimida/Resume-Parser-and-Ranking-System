import streamlit as st
import base64

def set_background_color(hex_color="#0d3f4c"):
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-color: {hex_color};
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

def load_logo(path="D:\\Y3S1\\Modules\\Investigation (FYP)\\FYP SEM 1 (Code)\\Job Dataset\\src\\assets\\transParslyst.png", width=150):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <div style="text-align: left; margin-top:-5rem; margin-bottom: -3rem;">
            <img src="data:image/png;base64,{data}" width="{width}">
        </div>
        """,
        unsafe_allow_html=True
    )

def set_sidebar_style():
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background-color: #0b3642;
            color: white;
        }
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        /* Selected menu item (active) */
        [data-testid="stSidebar"] .css-1v0mbdj:hover,
        [data-testid="stSidebar"] .css-1v0mbdj:focus,
        [data-testid="stSidebar"] .css-1v0mbdj:active {
            background-color: #145364;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    
def set_custom_style():
    st.markdown("""
        <style>
        /* Hide the "app" label in the sidebar only */
        [data-testid="stSidebarNav"] > ul > li:first-child {
            display: none;
        }
                
        /* Header (Deploy button bar) */
        [data-testid="stHeader"] {
            background-color: #092c36;
        }

        /* Optional: Hide blank space padding */
        header[data-testid="stHeader"] {
            height: 4.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

