import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Customer-Churn-Dashboard", page_icon=":bar_chart:", layout="wide"
)

st.title(":bar_chart: Churn Insights: Understanding Customer Retention")
st.markdown(
    "<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True
)
