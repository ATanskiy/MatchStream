import streamlit as st
from utils.ui import apply_theme, init_session
from utils import api

st.set_page_config(page_title="MatchStream - Login", layout="centered")
init_session()
apply_theme()

st.markdown(
    """
    <style>
    .login-title {
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 24px;
        line-height: 1.2;
    }

    .login-lock {
        display: inline-block;
        margin-right: 10px;
        cursor: pointer;
    }

    .login-lock:hover {
        animation: lock-bounce 0.6s ease;
    }

    @keyframes lock-bounce {
        0%   { transform: translateY(0); }
        30%  { transform: translateY(-10px); }
        60%  { transform: translateY(0); }
        80%  { transform: translateY(-4px); }
        100% { transform: translateY(0); }
    }

    /* ===============================
       Fix password eye icon
       =============================== */
    [data-testid="stTextInput"] svg {
        color: #f5f6f7;
        fill: currentColor;
        background: transparent !important;
        filter: none !important;
    }

    [data-testid="stTextInput"] button {
        background: transparent !important;
        border: none !important;
    }

    [data-testid="stTextInput"] button:hover svg {
        color: #112723;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="login-title">
        <span class="login-lock">🔐</span>Login or Register
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        try:
            data = api.login(email=email, password=password)
            st.session_state.token = data["token"]
            st.switch_page("pages/browse.py")
        except Exception:
            st.error("Invalid credentials")

with tab2:
    email_r = st.text_input("Email", key="rmail")
    password_r = st.text_input("Password", type="password", key="rpass")
    first = st.text_input("First name")
    last = st.text_input("Last name")

    if st.button("Register", use_container_width=True):
        try:
            data = api.register(email=email_r, password=password_r, first_name=first, last_name=last)
            st.session_state.token = data["token"]
            st.switch_page("pages/browse.py")
        except Exception:
            st.error("Email already exists")