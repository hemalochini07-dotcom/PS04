import streamlit as st

from ui_theme import apply_theme
st.title("Settings")
st.caption("Configure the demonstration experience.")

st.subheader("Detection settings")
sensitivity = st.select_slider("Detection sensitivity", options=["Conservative", "Balanced", "Sensitive"], value="Balanced")
cooldown = st.slider("Alert cooldown (hours)", min_value=1, max_value=72, value=24)
st.session_state["detection_sensitivity"] = sensitivity
st.session_state["alert_cooldown"] = cooldown
st.info("These settings are stored for the current session. The starter detector currently uses its built-in robust threshold; connect sensitivity and cooldown values to detector.py when extending the system.")

st.subheader("About Campaign Sentinel")
st.write("Campaign Sentinel detects unusual campaign behaviour, explains changes, and aims to reduce alert fatigue.")
st.write("Background styling is inspired by the contour-line aesthetic of Scrolltide. No external Scrolltide assets are required.")
