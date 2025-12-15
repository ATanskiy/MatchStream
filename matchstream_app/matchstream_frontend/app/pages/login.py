import streamlit as st
from utils.ui import apply_theme, init_session
from utils import api

st.set_page_config(page_title="MatchStream - Login", layout="centered")
init_session()
apply_theme()

st.title("🔐 Login or Register")

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        try:
            data = api.login(email=email, password=password)
            st.session_state.token = data["token"]
            st.switch_page("pages/browse.py")
        except Exception:
            st.error("Invalid credentials")

with tab2:
    email_r = st.text_input("Email", key="rmail")
    password_r = st.text_input("Password", type="password", key="rpass")
    first = st.text_input("First name")
    last = st.text_input("Last name")

    if st.button("Register", use_container_width=True):
        try:
            data = api.register(email=email_r, password=password_r, first_name=first, last_name=last)
            st.session_state.token = data["token"]
            st.switch_page("pages/browse.py")
        except Exception:
            st.error("Email already exists")