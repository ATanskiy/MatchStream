import streamlit as st
import requests

BACKEND = "http://matchstream_backend:8010"

st.set_page_config(page_title="MatchStream - Browse", layout="centered")

# require login + location
if "token" not in st.session_state or st.session_state.token is None:
    st.warning("Please login first.")
    st.switch_page("app/main.py")

if "state" not in st.session_state or "city" not in st.session_state:
    st.warning("Please set your location.")
    st.switch_page("pages/setting.py")

st.title("💘 MatchStream — Browse")

state = st.session_state.state
city  = st.session_state.city

# Load next user
resp = requests.get(
    f"{BACKEND}/discover",
    params={"state": state, "city": city, "user_id": st.session_state.token}
)

data = resp.json()

if "message" in data:
    st.info("No more users in this area. Try changing your location!")
    st.stop()

target_id = data["id"]

# ---- CARD UI ----
st.markdown("""
<style>
.user-card {
    background-color: #f9f9fc;
    border-radius: 15px;
    padding: 25px;
    text-align: center;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
}
.big-button {
    font-size: 28px;
    padding: 10px 25px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='user-card'>", unsafe_allow_html=True)

st.subheader(f"{data['first_name']} {data['last_name']}")
st.write(f"📍 {data['city']}, {data['state']}")

st.markdown("</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1,1])

with col1:
    if st.button("❌ Dislike", use_container_width=True, type="secondary"):
        requests.post(
            f"{BACKEND}/swipe",
            params={"user_id": st.session_state.token},
            json={"target_id": target_id, "decision": "dislike"}
        )
        st.rerun()

with col2:
    if st.button("💗 Like", use_container_width=True, type="primary"):
        requests.post(
            f"{BACKEND}/swipe",
            params={"user_id": st.session_state.token},
            json={"target_id": target_id, "decision": "like"}
        )
        st.rerun()