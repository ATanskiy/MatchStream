import streamlit as st
from utils.ui import apply_theme, init_session, require_login
from utils import api

st.set_page_config(page_title="MatchStream - Matches", layout="centered")
init_session()
apply_theme()

require_login()

st.title("💞 Your Matches")

items = api.matches(st.session_state.token)

if not items:
    st.info("You don't have any matches yet 💔")
    st.stop()

for m in items:
    photo = m.get("picture") or "https://via.placeholder.com/200?text=No+Photo"
    name = f"{m.get('first_name','')} {m.get('last_name','')}".strip()
    loc = ", ".join([x for x in [m.get("city",""), m.get("state","")] if x])

    st.markdown(
        f"""
        <div class="card" style="display:flex; align-items:center; gap:14px; margin-bottom:12px;">
          <img src="{photo}" style="width:76px; height:76px; border-radius:50%; object-fit:cover;">
          <div>
            <div style="font-weight:800; font-size:18px;">{name}</div>
            <div class="muted">📍 {loc}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )