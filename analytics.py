"""Shared cached analytics so all Streamlit pages reuse the same detector result."""
import streamlit as st
from detector import detect_anomalies, evaluate_detection

@st.cache_data(show_spinner=False, max_entries=8)
def get_analysis(df):
    alerts = detect_anomalies(df)
    metrics = evaluate_detection(df, alerts)
    return alerts, metrics
