import streamlit as st
from utils.ui import apply_theme, init_session

st.set_page_config(page_title="MatchStream", layout="centered")
init_session()
apply_theme()

st.title("💘 MatchStream")
st.write("Find your perfect data match 🔥")

if st.session_state.token:
    st.switch_page("pages/browse.py")
else:
    st.switch_page("pages/login.py")