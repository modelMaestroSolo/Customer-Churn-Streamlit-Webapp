import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Customer-Churn-Dashboard", page_icon=":bar_chart:", layout="wide"
)

st.title(":bar_chart: Churn Insights: Understanding Customer Retention")
st.markdown(
    "<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True
)

cleaned_data = st.session_state["df"]
tab1, tab2 = st.tabs(["Exploratory Analysis", "KPI Metrics"])
# data_train = st.write(st.session_state["df"])

with tab1:
    pass
