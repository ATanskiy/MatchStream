import streamlit as st
import requests
from datetime import datetime

BACKEND = "http://matchstream_backend:8010"

st.set_page_config(page_title="MatchStream - Browse", layout="centered")

# -----------------------------
# Session state
# -----------------------------
if "info_view" not in st.session_state:
    st.session_state.info_view = "name"

# -----------------------------
# Require login
# -----------------------------
if "token" not in st.session_state:
    st.warning("🔐 Please log in first")
    st.page_link("pages/login.py", label="Go to Login")
    st.stop()

# -----------------------------
# Require location
# -----------------------------
if "state" not in st.session_state or "city" not in st.session_state:
    st.warning("📍 Please set your location")
    st.page_link("pages/setting.py", label="Set Location")
    st.stop()

st.title("💘 MatchStream — Browse")

# -----------------------------
# Call backend
# -----------------------------
resp = requests.get(
    f"{BACKEND}/discover",
    params={
        "token": st.session_state.token,
        "state": st.session_state.state,
        "city": st.session_state.city,
    },
)

data = resp.json()

if "message" in data:
    st.info("No more users in this area")
    st.stop()

target_id = data["user_id"]

# -----------------------------
# Helpers
# -----------------------------
def format_dob(dob_str: str) -> str:
    try:
        d = datetime.strptime(dob_str, "%Y-%m-%d")
        return d.strftime("%B %d, %Y")
    except Exception:
        return dob_str


def calculate_age(dob_str: str) -> str:
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - dob.year - (
            (today.month, today.day) < (dob.month, dob.day)
        )
        return f"{age} years old"
    except Exception:
        return "Age unknown"


def get_info_text(p, view: str) -> str:
    if view == "name":
        return f"{p['first_name']} {p['last_name']}"
    if view == "email":
        return p["email"]
    if view == "phone":
        return p["phone"]
    if view == "location":
        return f"{p['city']}, {p['state']}"
    if view == "dob":
        return format_dob(p["dob"])
    if view == "age":
        return calculate_age(p["dob"])
    return ""

# -----------------------------
# Profile picture (round + fallback)
# -----------------------------
photo_url = data.get("picture")
if not photo_url:
    photo_url = "https://via.placeholder.com/160?text=No+Photo"

st.markdown(
    f"""
    <div style="display:flex; justify-content:center; margin:15px 0;">
      <img src="{photo_url}" style="
        width:160px;
        height:160px;
        border-radius:50%;
        object-fit:cover;
        box-shadow:0 6px 20px rgba(0,0,0,0.3);
      ">
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Main info text
# -----------------------------
st.markdown(
    "<p style='text-align:center; opacity:0.6; margin-bottom:0;'>Profile info</p>",
    unsafe_allow_html=True,
)

st.markdown(
    f"<h2 style='text-align:center; margin-top:0;'>"
    f"{get_info_text(data, st.session_state.info_view)}</h2>",
    unsafe_allow_html=True,
)

# -----------------------------
# Info buttons
# -----------------------------
c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    if st.button("👤", help="Name"):
        st.session_state.info_view = "name"
        st.rerun()

with c2:
    if st.button("✉️", help="Email"):
        st.session_state.info_view = "email"
        st.rerun()

with c3:
    if st.button("📞", help="Phone"):
        st.session_state.info_view = "phone"
        st.rerun()

with c4:
    if st.button("📍", help="Location"):
        st.session_state.info_view = "location"
        st.rerun()

with c5:
    if st.button("🎂", help="Birthday"):
        st.session_state.info_view = "dob"
        st.rerun()

with c6:
    if st.button("⏳", help="Age"):
        st.session_state.info_view = "age"
        st.rerun()

st.markdown("---")

# -----------------------------
# Like / Dislike buttons
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("❌ Dislike", use_container_width=True):
        requests.post(
            f"{BACKEND}/swipe",
            params={"token": st.session_state.token},
            json={"target_id": target_id, "decision": "dislike"},
        )
        st.rerun()

with col2:
    if st.button("💗 Like", use_container_width=True):
        requests.post(
            f"{BACKEND}/swipe",
            params={"token": st.session_state.token},
            json={"target_id": target_id, "decision": "like"},
        )
        st.rerun()