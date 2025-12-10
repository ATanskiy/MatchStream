import streamlit as st

st.set_page_config(page_title="MatchStream", layout="centered")

st.title("💘 MatchStream")
st.write("Find your perfect data match 🔥")

if "token" not in st.session_state:
    st.session_state.token = None

if st.session_state.token:
    st.success("Logged in!")
    st.page_link("pages/browse.py", label="Browse Profiles")
    st.page_link("pages/setting.py", label="Settings")
else:
    st.page_link("pages/login.py", label="Login / Register")