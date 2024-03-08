import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


def login():
    with open("./config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["preauthorized"],
    )
    authenticator.login(location="main")
    if st.session_state["authentication_status"]:
        authenticator.logout(location="sidebar", key="logout")
        st.write(f'Welcome *{st.session_state["name"]}*')

    elif st.session_state["authentication_status"] is False:
        st.error("Username/password is incorrect")

    else:
        st.warning("Please enter your username and password")
