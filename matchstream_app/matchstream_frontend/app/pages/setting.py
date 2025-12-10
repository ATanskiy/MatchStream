import streamlit as st

st.title("🌍 Choose Location")

state = st.text_input("State (e.g. NY, CA, TX)")
city = st.text_input("City (e.g. New York, Phoenix)")

if st.button("Save"):
    st.session_state.state = state
    st.session_state.city = city
    st.success("Location updated!")