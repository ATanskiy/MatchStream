import streamlit as st
from utils.ui import apply_theme, init_session, require_login
from utils import api

# -------------------------------------------------
# Page setup
# -------------------------------------------------
st.set_page_config(page_title="MatchStream - Matches", layout="centered")
init_session()
apply_theme()
require_login()

# -------------------------------------------------
# Styles (USE STREAMLIT CSS VARIABLES)
# -------------------------------------------------
st.markdown(
    """
    <style>
    /* ===============================
       Title
       =============================== */
    .page-title {
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 24px;
        line-height: 1.2;
        color: var(--text-color);
    }

    .page-icon {
        display: inline-block;
        margin-right: 10px;
        cursor: pointer;
    }

    .page-icon:hover {
        animation: heart-bounce 0.6s ease;
    }

    @keyframes heart-bounce {
        0%   { transform: translateY(0) rotate(0deg); }
        30%  { transform: translateY(-10px) rotate(-8deg); }
        60%  { transform: translateY(0) rotate(10deg); }
        100% { transform: translateY(0) rotate(0deg); }
    }

    /* ===============================
       Empty state (THE CORRECT WAY)
       =============================== */
    .empty-state {
        padding: 16px;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        margin-top: 10px;

        /* THIS is the fix */
        background: var(--secondary-background-color);
        color: var(--text-color);
    }

    /* ===============================
       Match cards
       =============================== */
    .match-card {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 12px;
    }

    .match-name {
        font-weight: 800;
        font-size: 18px;
        color: var(--text-color);
    }

    .match-location {
        opacity: 0.7;
        font-size: 14px;
        color: var(--text-color);
    }

    .empty-icon {
      font-size: 48px;
      line-height: 1;
      margin-bottom: 6px;
  }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Title
# -------------------------------------------------
st.markdown(
    """
    <div class="page-title">
        <span class="page-icon">💞</span>Your Matches
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Data
# -------------------------------------------------
items = api.matches(st.session_state.token)

# -------------------------------------------------
# Empty state
# -------------------------------------------------
if not items:
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-icon">💔</div>
            <div>You don't have any matches yet</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# -------------------------------------------------
# Matches list
# -------------------------------------------------
for m in items:
    photo = m.get("picture") or "https://via.placeholder.com/200?text=No+Photo"
    name = f"{m.get('first_name','')} {m.get('last_name','')}".strip()
    loc = ", ".join([x for x in [m.get("city",""), m.get("state","")] if x])

    st.markdown(
        f"""
        <div class="match-card">
            <img src="{photo}"
                 style="width:76px; height:76px; border-radius:50%; object-fit:cover;">
            <div>
                <div class="match-name">{name}</div>
                <div class="match-location">📍 {loc}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )