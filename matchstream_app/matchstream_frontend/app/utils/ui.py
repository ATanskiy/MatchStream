import streamlit as st

LIGHT_CSS = """
<style>
:root {
  --bg: #ffffff;
  --text: #111111;
  --card: #f6f7fb;
  --muted: #6b7280;
  --border: #d1d5db;
}

/* ===== App background ===== */
html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
  color: var(--text) !important;
}

/* ===== Header ===== */
header {
  background: transparent !important;
}

/* ===== Sidebar ===== */
[data-testid="stSidebar"] {
  background: #f3f4f6 !important;
}

[data-testid="stSidebarNav"] a,
[data-testid="stSidebarNav"] span {
  color: #111111 !important;
  font-weight: 500;
}

[data-testid="stSidebarNav"] a:hover {
  background-color: #e5e7eb !important;
}

/* ===== Labels ===== */
label {
  color: #111111 !important;
  font-weight: 500;
}

/* ===== Tabs ===== */
[data-testid="stTabs"] button {
  color: #111111 !important;
  font-weight: 600;
  background: transparent !important;
}

[data-testid="stTabs"] button[aria-selected="true"] {
  border-bottom: 2px solid #111111 !important;
}

/* ===== INPUT FIELDS ===== */
input, textarea {
  background-color: #ffffff !important;
  color: #111111 !important;
  border: 1.5px solid #d1d5db !important;
  border-radius: 8px !important;
}

input:focus, textarea:focus {
  border-color: #111111 !important;
  box-shadow: none !important;
}

/* ===== Password visibility button ===== */
button[data-testid="stPasswordVisibilityToggle"] {
  background: transparent !important;
  border: none !important;
}

button[data-testid="stPasswordVisibilityToggle"]:hover {
  background: #e5e7eb !important;
}

/* ===== PRIMARY BUTTON ===== */
button[kind="primary"] {
  background-color: #ffffff !important;
  color: #111111 !important;
  border: 2px solid #111111 !important;
  border-radius: 10px !important;
  font-weight: 600;
  box-shadow: none !important;
}

button[kind="primary"]:hover {
  background-color: #f3f4f6 !important;
}

/* ===== Alerts (no aggressive pink) ===== */
[data-testid="stAlert"] {
  background: #f9fafb !important;
  color: #111111 !important;
  border-left: 4px solid #9ca3af !important;
  border-radius: 10px !important;
}

/* ===== Layout ===== */
.block-container {
  padding-top: 2rem;
}

/* ===== Cards ===== */
.card {
  background: var(--card);
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 14px 16px;
}

.muted {
  color: var(--muted);
}

.center {
  text-align: center;
}
</style>
"""


DARK_CSS = """
<style>
:root {
  --bg:#0b0f19;
  --text:#e5e7eb;
  --card:#121a2a;
  --muted:#9ca3af;
  --border:#1f2937;
}

/* App background + text */
html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
  color: var(--text) !important;
}

/* Header */
header { background: transparent !important; }

/* Sidebar */
[data-testid="stSidebar"] {
  background: var(--bg) !important;
}

/* Input labels */
label {
  color: #e5e7eb !important;
  font-weight: 500;
}

/* Tabs text */
[data-testid="stTabs"] button {
  color: #e5e7eb !important;
  font-weight: 600;
}

/* Active tab underline */
[data-testid="stTabs"] button[aria-selected="true"] {
  border-bottom: 2px solid #e5e7eb !important;
}

/* Layout */
.block-container { padding-top: 2rem; }

.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 14px 16px;
}

.muted { color: var(--muted); }
.center { text-align:center; }
</style>
"""

def init_session() -> None:
    if "token" not in st.session_state:
        st.session_state.token = None
    if "theme" not in st.session_state:
        st.session_state.theme = "light"

def apply_theme() -> None:
    init_session()
    st.markdown(
        LIGHT_CSS if st.session_state.theme == "light" else DARK_CSS,
        unsafe_allow_html=True,
    )

def require_login() -> None:
    if not st.session_state.get("token"):
        st.warning("🔐 Please log in first")
        st.switch_page("pages/login.py")

def require_location() -> None:
    if not st.session_state.get("state") or not st.session_state.get("city"):
        st.warning("📍 Please set your location")
        st.switch_page("pages/setting.py")