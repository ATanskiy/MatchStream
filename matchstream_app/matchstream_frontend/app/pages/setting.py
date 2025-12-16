import streamlit as st
from utils.ui import apply_theme, init_session, require_login
from utils.api import get_filters

st.set_page_config(page_title="MatchStream - Settings", layout="centered")
init_session()
apply_theme()
require_login()

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
        60%  { transform: translateY(0) rotate(6deg); }
        100% { transform: translateY(0) rotate(0deg); }
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
        <span class="login-lock">⚙️</span>Settings
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Load filters ONCE
# -----------------------------
if "filters" not in st.session_state:
    st.session_state.filters = get_filters(st.session_state.token)

filters = st.session_state.filters

states = filters["states"]
cities_by_state = filters["cities"]
genders = filters["genders"]
age_range = filters["age"]

# -----------------------------
# Theme
# -----------------------------
theme = st.selectbox(
    "Theme",
    options=["light", "dark"],
    index=0 if st.session_state.theme == "light" else 1,
)

# -----------------------------
# Location (FROM DB)
# -----------------------------
state = st.selectbox(
    "State",
    options=states,
    index=states.index(st.session_state.state)
    if st.session_state.get("state") in states
    else 0,
)

cities = cities_by_state.get(state, [])

city = st.selectbox(
    "City",
    options=cities,
    index=cities.index(st.session_state.city)
    if st.session_state.get("city") in cities
    else 0,
)

# -----------------------------
# Gender
# -----------------------------
gender = st.selectbox(
    "Gender",
    options=genders,
    index=genders.index(st.session_state.gender)
    if st.session_state.get("gender") in genders
    else 0,
)

# -----------------------------
# Age range (single slider)
# -----------------------------
min_age, max_age = st.slider(
    "Age range",
    min_value=age_range["min"],
    max_value=age_range["max"],
    value=(
        st.session_state.get("min_age", age_range["min"]),
        st.session_state.get("max_age", age_range["max"]),
    ),
)

# -----------------------------
# Save + Redirect
# -----------------------------
if st.button("Save settings", use_container_width=True, type="primary"):
    st.session_state.theme = theme
    st.session_state.state = state
    st.session_state.city = city
    st.session_state.gender = gender
    st.session_state.min_age = min_age
    st.session_state.max_age = max_age

    st.switch_page("pages/browse.py")
