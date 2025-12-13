import streamlit as st
from utils.states import US_STATES

st.title("📍 Set your location")

state_name = st.selectbox(
    "State",
    options=list(US_STATES.values())
)

# reverse lookup
state_id = next(k for k, v in US_STATES.items() if v == state_name)

city = st.text_input("City")

if st.button("Save location"):
    st.session_state.state = state_id      # 👈 NY
    st.session_state.city = city.strip()   # 👈 New York
    st.success("Location saved!")