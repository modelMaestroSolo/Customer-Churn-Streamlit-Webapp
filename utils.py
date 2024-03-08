import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from typing import Callable


def login(main: callable):
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
        st.sidebar.header(f'Welcome *{st.session_state["name"]}*!')
        main()

    elif st.session_state["authentication_status"] is False:
        st.error("Oops! Username/password is incorrect")

    else:
        st.warning("Please enter your username and password")
