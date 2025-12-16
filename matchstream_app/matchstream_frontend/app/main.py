import streamlit as st
from utils.ui import apply_theme, init_session

st.set_page_config(page_title="MatchStream", layout="centered")
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
        0%   { transform: translateY(0) rotate(0deg); }
        30%  { transform: translateY(-10px) rotate(-8deg); }
        60%  { transform: translateY(0) rotate(14deg); }
        100% { transform: translateY(0) rotate(-5deg); }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="login-title">
        <span class="login-lock">💘</span>MatchStream
    </div>
    """,
    unsafe_allow_html=True,
)

st.html("""
<div class="card" style="margin-top:20px;">
    <h3>What is MatchStream?</h3>

    <div style="margin-top:8px; line-height:1.6;">
        MatchStream is a real-time matchmaking application focused on fast user discovery,
        clean user experience, and modern backend architecture.
    </div>

    <div style="margin-top:10px; line-height:1.6;">
        The project explores how location-aware matching, session-based interaction,
        and real-time flows can be designed and implemented in a scalable, product-oriented way.
    </div>
</div>

<div class="card" style="margin-top:16px; padding:18px 30px;">
    <h3>How it was built</h3>
    <ul>
        <li>Custom-styled Streamlit frontend focused on usability and clarity</li>
        <li>Python backend exposing REST APIs for core application logic</li>
        <li>Session-based authentication and state management</li>
        <li>Location-based user discovery and filtering logic</li>
        <li>Data engineering pipelines built with Spark</li>
        <li>Lakehouse-style data modeling using Spark and dbt</li>
        <li>Analytical reporting and dashboards powered by Power BI</li>
    </ul>
</div>

<div class="card" style="margin-top:16px;">
    <h3>About the creator</h3>
    <div style="margin-top:8px; line-height:1.6;">
        Built by a data engineer focused on full-stack ownership,
        product thinking, and building end-to-end systems that connect
        data, backend logic, and user experience.
    </div>
</div>
""")


st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("🔐 Login", use_container_width=True):
        st.switch_page("pages/login.py")

with col2:
    if st.session_state.token:
        if st.button("💖 Start Browsing", use_container_width=True):
            st.switch_page("pages/browse.py")