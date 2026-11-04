import streamlit as st
from ui.components.sidebar import render_sidebar
from ui.pages.dashboard_view import render_dashboard_overview
from ui.pages.scanner_view import render_scanner_view
from ui.pages.twin_view import render_twin_view
from ui.pages.records_view import render_records_view
from ui.pages.settings_view import render_settings_view
from utils.session import (
    NAV_DASHBOARD,
    NAV_SCANNER,
    NAV_TWIN,
    NAV_RECORDS,
    NAV_SETTINGS,
)

def render_dashboard_page() -> None:
    """Renders the main authenticated dashboard shell with persistent sidebar and active view routing."""
    # 1. Left Sidebar Navigation
    render_sidebar()

    # 2. View Router based on sidebar selection
    active_nav = st.session_state.get("active_nav", NAV_DASHBOARD)

    if active_nav == NAV_DASHBOARD:
        render_dashboard_overview()
    elif active_nav == NAV_SCANNER:
        render_scanner_view()
    elif active_nav == NAV_TWIN:
        render_twin_view()
    elif active_nav == NAV_RECORDS:
        render_records_view()
    elif active_nav == NAV_SETTINGS:
        render_settings_view()
    else:
        render_dashboard_overview()
