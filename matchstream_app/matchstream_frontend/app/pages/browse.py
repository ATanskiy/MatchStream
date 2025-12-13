import streamlit as st
import requests

BACKEND = "http://matchstream_backend:8010"

st.set_page_config(page_title="MatchStream - Browse", layout="centered")

# 1️⃣ Require login
if "token" not in st.session_state:
    st.warning("🔐 Please log in first")
    st.page_link("pages/login.py", label="Go to Login")
    st.stop()

# 2️⃣ Require location
if "state" not in st.session_state or "city" not in st.session_state:
    st.warning("📍 Please set your location")
    st.page_link("pages/setting.py", label="Set Location")
    st.stop()

st.title("💘 MatchStream — Browse")

# 3️⃣ Call backend
resp = requests.get(
    f"{BACKEND}/discover",
    params={
        "token": st.session_state.token,
        "state": st.session_state.state,  # e.g. NY
        "city": st.session_state.city,    # e.g. New York
    }
)

data = resp.json()

# 4️⃣ No users
if "message" in data:
    st.info("No more users in this area")
    st.stop()

# 5️⃣ Extract target
target_id = data["user_id"]

# 6️⃣ UI
st.subheader(f"{data['first_name']} {data['last_name']}")
st.write(f"📍 {data['city']}, {data['state']}")

col1, col2 = st.columns(2)

with col1:
    if st.button("❌ Dislike", use_container_width=True):
        requests.post(
            f"{BACKEND}/swipe",
            params={"token": st.session_state.token},
            json={
                "target_id": target_id,
                "decision": "dislike",
            },
        )
        st.rerun()

with col2:
    if st.button("💗 Like", use_container_width=True):
        requests.post(
            f"{BACKEND}/swipe",
            params={"token": st.session_state.token},
            json={
                "target_id": target_id,
                "decision": "like",
            },
        )
        st.rerun()