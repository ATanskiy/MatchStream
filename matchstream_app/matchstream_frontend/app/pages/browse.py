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
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;900&display=swap');
    
    /* === BASE STREAMLIT BUTTON === */
    div.stButton > button {
        width: 100%;
        height: 86px;

        font-family: 'Poppins', sans-serif !important;
        font-size: 24px !important;
        font-weight: 600 !important;

        border-radius: 22px !important;
        border: none !important;

        display: flex;
        align-items: center;
        justify-content: center;
        gap: 14px;

        letter-spacing: 0.5px;
        cursor: pointer;

        background: linear-gradient(135deg, #3b6cff, #6fa8ff);
        color: white !important;

        box-shadow: 0 12px 30px rgba(59,108,255,0.45);
        transition: all 0.2s ease-in-out;
    }

    /* === TARGET ALL TEXT INSIDE BUTTON === */
    div.stButton > button p {
        font-family: 'Poppins', sans-serif !important;
        font-size: 24px !important;
        font-weight: 600 !important;
        line-height: 1.2 !important;
        margin: 0 !important;
    }

    /* === TARGET NESTED SPANS (EMOJI + TEXT) === */
    div.stButton > button span,
    div.stButton > button span > span {
        font-family: 'Poppins', sans-serif !important;
        font-size: 24px !important;
        font-weight: 600 !important;
        line-height: 1.2 !important;
    }

    /* === HOVER === */
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 38px rgba(59,108,255,0.65);
    }
    
    /* === HEART ANIMATION === */
    .heart-icon {
        display: inline-block;
        cursor: pointer;
        transition: transform 0.3s ease, filter 0.3s ease;
    }
    
    .heart-icon:hover {
        transform: scale(1.3);
        filter: drop-shadow(0 0 20px rgba(255, 105, 180, 0.8));
        animation: heartbeat 0.6s ease-in-out;
    }
    
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        25% { transform: scale(1.3); }
        50% { transform: scale(1.15); }
        75% { transform: scale(1.3); }
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
    st.markdown("<div style='height: 160px;'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="text-align:center;font-family:Poppins,sans-serif;">
            <div style="font-size:28px;font-weight:800;color:#ff6b9d;margin-bottom:16px;">
                💔 No more users in this area
            </div>
            <div style="font-size:18px;color:#ff6b9d;opacity:0.85;">
                Try expanding your search area or check back later!
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.stop()

target_id = data["user_id"]

# -------------------------------------------------
# Handle action from query params
# -------------------------------------------------
params = st.query_params
action = params.get("action")

if action in ("like", "dislike"):
    api.swipe(st.session_state.token, target_id, action)

    # clear URL params so refresh doesn't repeat action
    st.query_params.clear()

    st.rerun()

full_name = f"{data.get('first_name','')} {data.get('last_name','')}".strip()

# -------------------------------------------------
# Header (heart + full name)
# -------------------------------------------------
st.markdown(
    f"""
    <div class="center" style="margin: 14px 0 26px 0;">
        <div class="heart-icon" style="font-size:88px; line-height:1;">💘</div>
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
    if st.button("💔  Dislike", use_container_width=True, key="dislike"):
        st.query_params["action"] = "dislike"
        st.rerun()

with col2:
    if st.button("💖  Like", use_container_width=True, key="like"):
        st.query_params["action"] = "like"
        st.rerun()