import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=True)
def load_excel(path):
    return pd.read_excel(path, sheet_name=None, engine="openpyxl")
