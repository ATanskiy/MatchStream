import streamlit as st
from pytest_mock import MockerFixture

from matchstream_app.matchstream_frontend.app.utils.ui import (
    init_session,
    apply_theme,
    require_login,
    require_location,
)


def test_init_session():
    # Clear real session_state
    st.session_state.clear()

    init_session()

    assert st.session_state["token"] is None
    assert st.session_state["theme"] == "light"


def test_apply_theme_light(mocker: MockerFixture):
    st.session_state.clear()
    st.session_state["theme"] = "light"

    mock_markdown = mocker.patch.object(st, "markdown")

    apply_theme()

    mock_markdown.assert_called()
    args, kwargs = mock_markdown.call_args
    assert "style" in args[0]
    assert kwargs["unsafe_allow_html"] is True


def test_require_login_no_token(mocker: MockerFixture):
    st.session_state.clear()
    st.session_state["token"] = None

    mock_warning = mocker.patch.object(st, "warning")
    mock_switch = mocker.patch.object(st, "switch_page")

    require_login()

    mock_warning.assert_called_with("🔐 Please log in first")
    mock_switch.assert_called_with("pages/login.py")


def test_require_login_with_token(mocker: MockerFixture):
    st.session_state.clear()
    st.session_state["token"] = "fake_token"

    mock_warning = mocker.patch.object(st, "warning")
    mock_switch = mocker.patch.object(st, "switch_page")

    require_login()

    mock_warning.assert_not_called()
    mock_switch.assert_not_called()


def test_require_location_missing(mocker: MockerFixture):
    st.session_state.clear()
    st.session_state["state"] = None
    st.session_state["city"] = None

    mock_warning = mocker.patch.object(st, "warning")
    mock_switch = mocker.patch.object(st, "switch_page")

    require_location()

    mock_warning.assert_called_with("📍 Please set your location")
    mock_switch.assert_called_with("pages/setting.py")


def test_require_location_present(mocker: MockerFixture):
    st.session_state.clear()
    st.session_state["state"] = "CA"
    st.session_state["city"] = "SF"

    mock_warning = mocker.patch.object(st, "warning")
    mock_switch = mocker.patch.object(st, "switch_page")

    require_location()

    mock_warning.assert_not_called()
    mock_switch.assert_not_called()