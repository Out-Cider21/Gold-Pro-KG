import streamlit as st


def load_css():
    st.markdown("""
    <style>
    .stApp {
        background: #060b14;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background: #0d1422;
        border-right: 1px solid #1f2937;
    }

    .hero {
        background: linear-gradient(135deg,#06121f,#101827,#07131d);
        border: 1px solid #1f2937;
        border-radius: 24px;
        padding: 24px;
        margin-bottom: 18px;
        box-shadow: 0 0 30px rgba(0,255,204,0.07);
    }

    .green {
        color:#00ffcc;
        text-shadow:0 0 12px rgba(0,255,204,.4);
    }

    .red {
        color:#ff4d6d;
        text-shadow:0 0 12px rgba(255,77,109,.4);
    }

    .blue {
        color:#38bdf8;
        text-shadow:0 0 12px rgba(56,189,248,.4);
    }

    .gold {
        color:#facc15;
        text-shadow:0 0 12px rgba(250,204,21,.4);
    }

    .card {
        background: linear-gradient(145deg,#111827,#0b1220);
        border: 1px solid #1f2937;
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 14px;
    }

    .badge {
        padding: 14px;
        border-radius: 14px;
        text-align:center;
        font-weight:900;
        letter-spacing:1px;
        margin-bottom:18px;
    }

    div[data-testid="metric-container"] {
        background: linear-gradient(145deg,#111827,#0b1220);
        border: 1px solid #1f2937;
        border-radius: 18px;
        padding: 16px;
    }
    </style>
    """, unsafe_allow_html=True)
