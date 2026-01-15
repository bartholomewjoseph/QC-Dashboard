import streamlit as st
import plotly.express as px
import os

from config.settings import EXCEL_PATH, MAIN_SHEET, FEMALE_SHEET
from utils.data_loader import load_excel
from utils.filters import sidebar_filter
from utils.helpers import safe_unique
from utils.metrics import calculate_pregnancy_metrics
from utils.quality_checks import duplicate_households, pregnancy_mismatch


def render_dashboard():

    st.title("📊 Pilot – Data Quality & Coverage Dashboard")

    if not os.path.exists(EXCEL_PATH):
        st.error("Excel file not found. Check config/settings.py")
        st.stop()

    sheets = load_excel(EXCEL_PATH)

    df = sheets.get(MAIN_SHEET)
    female = sheets.get(FEMALE_SHEET)

    if df is None:
        st.error("Main sheet not found")
        st.stop()

    st.sidebar.title("🔎 Filters")

    lga = sidebar_filter("LGA", df, "Q2. LGA")
    ward = sidebar_filter("Ward", df, "Your Ward is")
    community = sidebar_filter("Community", df, "Confirm your community")
    cluster = sidebar_filter("Cluster", df, "_submitted_by")

    filtered = df.copy()

    if lga != "All": filtered = filtered[filtered["Q2. LGA"] == lga]
    if ward != "All": filtered = filtered[filtered["Your Ward is"] == ward]
    if community != "All": filtered = filtered[filtered["Confirm your community"] == community]
    if cluster != "All": filtered = filtered[filtered["_submitted_by"] == cluster]

    if female is not None and "_uuid" in filtered.columns:
        uuids = filtered["_uuid"].astype(str).unique()
        female = female[female["_submission__uuid"].astype(str).isin(uuids)]

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Households", safe_unique(filtered, "unique_code"))
    k2.metric("Women", safe_unique(female, "mother_id"))
    k3.metric("Wards", filtered["Your Ward is"].nunique())
    k4.metric("Settlements", filtered["Confirm your community"].nunique())

    st.markdown("---")

    if female is not None:
        metrics = calculate_pregnancy_metrics(female)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Born Alive", metrics["alive"])
        c2.metric("Born Dead", metrics["dead"])
        c3.metric("Miscarriages", metrics["miscarriage"])
        c4.metric("Total Pregnancies", metrics["total"])

    st.markdown("---")

    dup = duplicate_households(filtered)
    mismatch = pregnancy_mismatch(female) if female is not None else None

    dq = {
        "Issue": ["Duplicate Households", "Pregnancy Outcome Mismatch"],
        "Count": [len(dup), 0 if mismatch is None else len(mismatch)]
    }

    fig = px.bar(dq, x="Issue", y="Count", text="Count")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📄 Data Preview")
    st.dataframe(filtered.head(200), use_container_width=True)
