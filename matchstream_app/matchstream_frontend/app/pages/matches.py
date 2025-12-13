import streamlit as st
import requests

BACKEND = "http://matchstream_backend:8010"

st.set_page_config(page_title="MatchStream - Matches", layout="centered")

st.title("💞 Your Matches")

# -----------------------------
# Require login
# -----------------------------
if "token" not in st.session_state:
    st.warning("🔐 Please log in first")
    st.page_link("pages/login.py", label="Go to Login")
    st.stop()

# -----------------------------
# Call backend
# -----------------------------
resp = requests.get(
    f"{BACKEND}/matches",
    params={"token": st.session_state.token},
)

matches = resp.json()

if not matches:
    st.info("You don't have any matches yet 💔")
    st.stop()

# -----------------------------
# Render matches
# -----------------------------
for m in matches:
    st.markdown(
        f"""
        <div style="
            display:flex;
            align-items:center;
            gap:15px;
            background:#f9f9fc;
            padding:15px;
            border-radius:12px;
            margin-bottom:12px;
        ">
            <img src="{m['picture']}" style="
                width:70px;
                height:70px;
                border-radius:50%;
                object-fit:cover;
            ">
            <div>
                <b>{m['first_name']} {m['last_name']}</b><br>
                <span style="opacity:0.7;">📍 {m['city']}, {m['state']}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )