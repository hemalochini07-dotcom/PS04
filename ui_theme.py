import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    :root { color-scheme: dark; }
    .stApp { background: radial-gradient(ellipse at 10% -5%, rgba(14,165,233,.18), transparent 38%), radial-gradient(ellipse at 90% 15%, rgba(20,184,166,.10), transparent 32%), linear-gradient(145deg,#070c16,#0b1424 52%,#07101b); color:#eef6ff; }
    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
    [data-testid="stHeader"] { background:transparent; }
    [data-testid="stSidebar"] { background:linear-gradient(180deg,#0b1627,#08111e); border-right:1px solid rgba(125,211,252,.14); }
    [data-testid="stSidebar"] * { color:#dceaf8; }
    h1,h2,h3 { font-family:'Space Grotesk',sans-serif !important; letter-spacing:-.025em; color:#f3f8ff; }
    p, label, .stCaption { color:#aebfd2; }
    [data-testid="stMetric"] { background:linear-gradient(145deg,rgba(20,40,64,.92),rgba(12,25,42,.92)); border:1px solid rgba(125,211,252,.16); padding:17px 18px; border-radius:17px; box-shadow:0 12px 30px rgba(0,0,0,.13); }
    [data-testid="stMetricLabel"] { color:#a9bfd5 !important; }
    [data-testid="stMetricValue"] { color:#f4f9ff !important; font-family:'Space Grotesk',sans-serif; }
    div[data-testid="stPlotlyChart"] { border:1px solid rgba(125,211,252,.12); border-radius:16px; padding:6px; background:rgba(11,24,40,.35); }
    div[data-testid="stDataFrame"],div[data-testid="stTable"] { border:1px solid rgba(125,211,252,.14); border-radius:13px; overflow:hidden; }
    div.stButton > button, div.stDownloadButton > button { border-radius:10px; border:1px solid rgba(94,234,212,.35); background:linear-gradient(90deg,#0e7490,#0f766e); color:white; font-weight:600; }
    div.stButton > button:hover, div.stDownloadButton > button:hover { border-color:#5eead4; filter:brightness(1.1); }
    [data-baseweb="select"] > div, [data-baseweb="input"] > div, [data-baseweb="textarea"] > div { background:rgba(7,19,32,.9); border-color:rgba(125,211,252,.2); }
    hr { border-color:rgba(125,211,252,.13); }
    .cs-hero { background:linear-gradient(115deg,rgba(16,43,70,.96),rgba(12,29,49,.92) 62%,rgba(12,54,60,.75)); border:1px solid rgba(56,189,248,.25); border-radius:22px; padding:28px 32px; margin:4px 0 24px; box-shadow:0 18px 45px rgba(0,0,0,.17); }
    .cs-eyebrow { font-size:.72rem; letter-spacing:.16em; text-transform:uppercase; color:#5eead4; font-weight:700; }
    .cs-hero h1 { font-size:clamp(2.4rem,5vw,3.8rem); line-height:1.05; margin:.45rem 0 .8rem; }
    .cs-hero h1 span { color:#5eead4; }
    .cs-hero p { max-width:800px; font-size:1rem; line-height:1.7; color:#bfd0e2; }
    .cs-pill { display:inline-block; border:1px solid rgba(94,234,212,.28); border-radius:999px; padding:7px 12px; color:#b8f7ed; background:rgba(3,15,27,.35); font-size:.74rem; letter-spacing:.05em; }
    .section-note { color:#9eb3ca; font-size:.88rem; }
    </style>
    """, unsafe_allow_html=True)
