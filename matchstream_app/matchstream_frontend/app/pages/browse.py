import streamlit as st
from utils.ui import apply_theme, init_session, require_login, require_location
from utils import api
from utils.components import profile_card_html

# -------------------------------------------------
# Page setup
# -------------------------------------------------
st.set_page_config(page_title="MatchStream - Browse", layout="centered")
init_session()
apply_theme()

require_login()
require_location()

# -------------------------------------------------
# Custom button styling
# -------------------------------------------------
st.markdown(
    """
    <style>
    .stButton > button {
        height: 78px;
        font-size: 26px;
        font-weight: 900;
        border-radius: 20px;
        border: none;
        letter-spacing: 0.5px;

        background: linear-gradient(135deg, #3b6cff, #6fa8ff);
        color: white;

        box-shadow: 0 12px 30px rgba(59,108,255,0.45);
        transition: all 0.2s ease-in-out;
    }

    /* Bigger emoji + text */
    .stButton > button span {
        font-size: 28px;
    }

    /* Hover lift */
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 38px rgba(59,108,255,0.65);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Fetch next profile
# -------------------------------------------------
data = api.discover(
    token=st.session_state.token,
    state=st.session_state.state,
    city=st.session_state.city,
)

if data.get("message"):
    st.info("💔 No more users in this area")
    st.stop()

target_id = data["user_id"]
full_name = f"{data.get('first_name','')} {data.get('last_name','')}".strip()

# -------------------------------------------------
# Header (heart + full name)
# -------------------------------------------------
st.markdown(
    f"""
    <div class="center" style="margin: 14px 0 26px 0;">
        <div style="font-size:68px; line-height:1;">💘</div>
        <div style="font-size:30px; font-weight:800; margin-top:6px;">
            {full_name}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Profile card
# -------------------------------------------------
st.markdown(profile_card_html(data, photo_size_px=350), unsafe_allow_html=True)
st.markdown("")

# -------------------------------------------------
# Action buttons
# -------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("💔    Dislike", use_container_width=True):
        api.swipe(st.session_state.token, target_id, "dislike")
        st.rerun()

with col2:
    if st.button("💖    Like", use_container_width=True):
        api.swipe(st.session_state.token, target_id, "like")
        st.rerun()
