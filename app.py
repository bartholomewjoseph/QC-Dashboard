import sys
import os

# Force project root into Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from pages.dashboard import render_dashboard
from pages.audio_transcription import render_audio_page

st.set_page_config(
    page_title="Mortality Pilot Dashboard",
    layout="wide"
)

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Audio Transcription"]
)

if page == "Dashboard":
    render_dashboard()
else:
    render_audio_page()
