import streamlit as st

def sidebar_filter(label, df, column):
    if column not in df.columns:
        return "All"
    return st.sidebar.selectbox(
        label,
        ["All"] + sorted(df[column].dropna().astype(str).unique())
    )
