# Importa Streamlit para insertar estilos CSS
import streamlit as st


def cargar_estilos():
    """Carga una apariencia moderna tipo asistente virtual para Streamlit."""

    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg-primary: #050816;
        --bg-card: rgba(15, 23, 42, 0.78);
        --bg-card-strong: rgba(15, 23, 42, 0.94);
        --border-soft: rgba(148, 163, 184, 0.20);
        --accent: #38bdf8;
        --accent-two: #8b5cf6;
        --success: #34d399;
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 12% 8%, rgba(56, 189, 248, 0.22), transparent 28%),
            radial-gradient(circle at 88% 18%, rgba(139, 92, 246, 0.22), transparent 30%),
            radial-gradient(circle at 50% 95%, rgba(16, 185, 129, 0.12), transparent 30%),
            linear-gradient(135deg, #020617 0%, #0f172a 48%, #111827 100%);
        color: var(--text-main);
    }

    .block-container {
        max-width: 1180px;
        padding-top: 1.6rem;
        padding-bottom: 8rem;
    }

    header[data-testid="stHeader"] {
        background: rgba(2, 6, 23, 0);
    }

    .main-hero {
        position: relative;
        overflow: hidden;
        padding: 34px 34px 30px 34px;
        border-radius: 30px;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.88), rgba(30, 41, 59, 0.62));
        border: 1px solid rgba(148, 163, 184, 0.20);
        box-shadow: 0 24px 70px rgba(0, 0, 0, 0.42);
        backdrop-filter: blur(18px);
        margin-bottom: 28px;
    }

    .main-hero::before {
        content: "";
        position: absolute;
        width: 360px;
        height: 360px;
        right: -150px;
        top: -160px;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.30), transparent 68%);
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 13px;
        border-radius: 999px;
        background: rgba(56, 189, 248, 0.12);
        color: #bae6fd;
        border: 1px solid rgba(56, 189, 248, 0.25);
        font-size: 0.86rem;
        font-weight: 700;
        margin-bottom: 16px;
    }

    .hero-title {
        font-size: clamp(2.2rem, 5vw, 4.1rem);
        line-height: 1.02;
        font-weight: 850;
        letter-spacing: -1.5px;
        margin: 0;
        color: #f8fafc;
    }

    .hero-gradient {
        background: linear-gradient(90deg, #38bdf8, #a78bfa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        max-width: 760px;
        margin-top: 15px;
        color: #cbd5e1;
        font-size: 1.05rem;
        line-height: 1.7;
    }

    .feature-row {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 14px;
        margin-top: 22px;
    }

    .feature-card {
        padding: 15px 16px;
        border-radius: 20px;
        background: rgba(2, 6, 23, 0.45);
        border: 1px solid rgba(148, 163, 184, 0.16);
    }

    .feature-card strong {
        color: #e0f2fe;
        display: block;
        margin-bottom: 5px;
    }

    .feature-card span {
        color: var(--text-muted);
        font-size: 0.92rem;
    }

    .glass-panel {
        padding: 24px;
        border-radius: 26px;
        background: var(--bg-card);
        border: 1px solid var(--border-soft);
        box-shadow: 0 18px 50px rgba(0, 0, 0, 0.28);
        backdrop-filter: blur(16px);
        margin-bottom: 18px;
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 800;
        margin-bottom: 12px;
        color: #e0f2fe;
    }

    .empty-chat {
        text-align: center;
        padding: 34px 22px;
        border-radius: 24px;
        border: 1px dashed rgba(148, 163, 184, 0.25);
        background: rgba(2, 6, 23, 0.34);
        color: #cbd5e1;
    }

    .chat-box {
        padding: 20px;
        border-radius: 24px;
        background: rgba(2, 6, 23, 0.48);
        border: 1px solid rgba(148, 163, 184, 0.16);
        margin-bottom: 18px;
    }

    .msg-label {
        font-size: 0.78rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-weight: 800;
        color: var(--text-muted);
        margin-bottom: 8px;
    }

    .user-bubble, .bot-bubble {
        padding: 15px 17px;
        border-radius: 18px;
        line-height: 1.65;
        margin-bottom: 14px;
    }

    .user-bubble {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.22), rgba(56, 189, 248, 0.10));
        border: 1px solid rgba(56, 189, 248, 0.22);
    }

    .bot-bubble {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.16), rgba(139, 92, 246, 0.10));
        border: 1px solid rgba(52, 211, 153, 0.20);
    }

    div[data-testid="stTextArea"] label {
        color: #e0f2fe !important;
        font-weight: 800 !important;
    }

    textarea {
        min-height: 142px !important;
        background: rgba(2, 6, 23, 0.78) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(56, 189, 248, 0.30) !important;
        border-radius: 22px !important;
        padding: 16px !important;
        font-size: 1rem !important;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02), 0 16px 35px rgba(0,0,0,0.22) !important;
    }

    textarea:focus {
        border-color: rgba(56, 189, 248, 0.75) !important;
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.14) !important;
    }

    .stButton > button {
        width: 100%;
        border-radius: 18px;
        background: linear-gradient(135deg, #2563eb, #06b6d4 55%, #10b981);
        color: white;
        font-weight: 850;
        border: 0;
        padding: 0.82rem 1rem;
        transition: all 0.22s ease;
        box-shadow: 0 14px 30px rgba(37, 99, 235, 0.28);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        filter: brightness(1.08);
        color: white;
        box-shadow: 0 18px 35px rgba(56, 189, 248, 0.30);
    }

    .stButton > button[kind="secondary"] {
        background: rgba(15, 23, 42, 0.82);
        border: 1px solid rgba(148, 163, 184, 0.24);
        box-shadow: none;
    }

    div[data-testid="stAlert"] {
        border-radius: 18px;
        border: 1px solid rgba(251, 191, 36, 0.30);
        background: rgba(251, 191, 36, 0.10);
    }

    hr {
        border-color: rgba(148, 163, 184, 0.16);
    }

    .stPyplot {
        background: #f8fafc;
        border-radius: 22px;
        padding: 14px;
        border: 1px solid rgba(148, 163, 184, 0.18);
    }

    footer { visibility: hidden; }

    @media (max-width: 800px) {
        .feature-row {
            grid-template-columns: 1fr;
        }
        .main-hero, .glass-panel {
            padding: 22px;
        }
    }
                
/* RESPONSIVE PARA TELÉFONO */
@media (max-width: 768px) {

    .block-container {
        padding: 1rem !important;
        max-width: 100% !important;
    }

    .main-hero {
        padding: 1.2rem !important;
        text-align: center !important;
    }

    .hero-title {
        font-size: 2rem !important;
        line-height: 1.2 !important;
    }

    .hero-subtitle {
        font-size: 0.95rem !important;
    }

    .feature-row {
        display: flex !important;
        flex-direction: column !important;
        gap: 0.8rem !important;
    }

    .feature-card {
        width: 100% !important;
    }

    .glass-panel {
        padding: 1rem !important;
        margin-top: 1rem !important;
    }

    .chat-box {
        padding: 1rem !important;
        border-radius: 16px !important;
    }

    .user-bubble,
    .bot-bubble {
        max-width: 100% !important;
        font-size: 0.95rem !important;
        overflow-wrap: break-word !important;
    }

    textarea {
        min-height: 120px !important;
        font-size: 1rem !important;
    }

    .stButton > button {
        width: 100% !important;
        margin-top: 0.5rem !important;
    }

    div[data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
    }
}
    </style>
    """, unsafe_allow_html=True)
