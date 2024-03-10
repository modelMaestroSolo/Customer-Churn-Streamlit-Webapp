import streamlit as st
import numpy as np
import pandas as pd
from typing import List, Tuple
import os
from utils import login


# function to set up page configuration
def set_page_config():
    st.set_page_config(
        page_title="Prediction History!",
        page_icon="🕰️",
        layout="wide",
    )


# function to display title in a streamlit container
def display_title_container():
    with st.container(border=True):
        st.markdown(""" ### 🕰️ Prediction History """)
        st.write("This page shows all the predictions made so far!")

    st.markdown(
        "<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True
    )


def display_history():
    try:
        data = pd.read_csv("./data/history.csv")
        st.dataframe(data)
    except FileNotFoundError:
        st.info("No predictions have been made yet!")


def main():
    display_title_container()
    display_history()


if __name__ == "__main__":
    set_page_config()
    login(main=main)
