import streamlit as st


def load_css():

    st.markdown('''
    <style>

    .stApp {
        background-color: #070b14;
        color: white;
    }

    .main-header {
        background: linear-gradient(135deg,#0f172a,#111827);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid #1f2937;
         margin-bottom: 20px;
    }

    div[data-testid="metric-container"] {
        background: #111827;
        border: 1px solid #1f2937;
        padding: 15px;
        border-radius: 16px;
    }

    </style>
    ''', unsafe_allow_html=True)
