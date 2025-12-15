import streamlit as st
from utils.ui import apply_theme, init_session, require_login, require_location
from utils import api
from utils.components import profile_card_html

st.set_page_config(page_title="MatchStream - Browse", layout="centered")
init_session()
apply_theme()

require_login()
require_location()

st.title("💘 MatchStream — Browse")

# filters (expects backend /filters)
filters = {}
with st.expander("Filters", expanded=False):
    try:
        opts = api.filter_options(st.session_state.token)
        age_min, age_max = opts.get("age_range", [18, 80])
        genders = opts.get("genders", [])
        filters["min_age"] = st.slider("Min age", min_value=age_min, max_value=age_max, value=age_min)
        filters["max_age"] = st.slider("Max age", min_value=age_min, max_value=age_max, value=age_max)
        if genders:
            filters["gender"] = st.multiselect("Gender", options=genders)
    except Exception:
        st.info("Filters endpoint not available yet.")

data = api.discover(
    token=st.session_state.token,
    state=st.session_state.state,
    city=st.session_state.city,
    filters=filters,
)

if data.get("message"):
    st.info("No more users in this area")
    st.stop()

target_id = data["user_id"]

st.markdown(profile_card_html(data, photo_size_px=280), unsafe_allow_html=True)
st.markdown("")

col1, col2 = st.columns(2)
with col1:
    if st.button("❌ Dislike", use_container_width=True):
        api.swipe(st.session_state.token, target_id, "dislike")
        st.rerun()

with col2:
    if st.button("💗 Like", use_container_width=True):
        api.swipe(st.session_state.token, target_id, "like")
        st.rerun()