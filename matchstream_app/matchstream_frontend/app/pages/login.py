import streamlit as st
import requests

BACKEND = "http://matchstream_backend:8010"

st.title("🔐 Login or Register")

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        resp = requests.post(f"{BACKEND}/login", json={"email": email, "password": password})
        if resp.status_code == 200:
            st.session_state.token = resp.json()["token"]
            st.success("Logged in!")
            st.switch_page("main.py")
        else:
            st.error("Invalid credentials")

with tab2:
    email_r = st.text_input("Email", key="rmail")
    password_r = st.text_input("Password", type="password", key="rpass")
    first = st.text_input("First name")
    last = st.text_input("Last name")

    if st.button("Register"):
        resp = requests.post(f"{BACKEND}/register", json={
            "email": email_r,
            "password": password_r,
            "first_name": first,
            "last_name": last
        })
        if resp.status_code == 200:
            st.session_state.token = resp.json()["token"]
            st.success("Registered!")
            st.switch_page("main.py")
        else:
            st.error("Email already exists")