import streamlit as st
from utils.session import (
    get_user_data,
    logout,
    NAV_DASHBOARD,
    NAV_SCANNER,
    NAV_TWIN,
    NAV_RECORDS,
    NAV_SETTINGS,
)
from config.settings import APP_TITLE, APP_SUBTITLE
from ui.components.logo import render_logo
from utils.validation import esc

def render_sidebar() -> None:
    """Renders the modern left sidebar navigation with branding, active nav items, and profile card."""
    user = get_user_data()
    user_name = user.get("name", "Aarav Sharma")
    age = user.get("age", 25)
    health = user.get("health", "None")
    active_nav = st.session_state.get("active_nav", NAV_DASHBOARD)

    with st.sidebar:
        # App Branding Header
        logo_html = render_logo(44)
        brand_html = (
            f'<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">'
            f'{logo_html}'
            f'<div>'
            f'<div style="font-weight: 800; font-size: 1.25rem; color: #0F172A; letter-spacing: -0.02em;">{APP_TITLE}</div>'
            f'<div style="font-size: 0.75rem; color: #64748B; font-weight: 500;">{APP_SUBTITLE}</div>'
            f'</div>'
            f'</div>'
        )
        st.markdown(brand_html, unsafe_allow_html=True)

        st.caption("MAIN NAVIGATION")

        # Navigation Buttons with active indicator
        nav_items = [
            ("📊 Dashboard", NAV_DASHBOARD),
            ("📸 AI Scanner", NAV_SCANNER),
            ("🧬 Digital Twin", NAV_TWIN),
            ("📜 Scan History", NAV_RECORDS),
            ("⚙️ Settings", NAV_SETTINGS),
        ]

        for label, nav_key in nav_items:
            is_active = (active_nav == nav_key)
            button_type = "primary" if is_active else "secondary"
            if st.button(label, key=f"nav_{nav_key}", use_container_width=True, type=button_type):
                st.session_state.active_nav = nav_key
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("AURA SYNC STATUS")

        # Digital Twin Profile Widget
        widget_html = (
            f'<div class="sidebar-widget" style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px; padding: 14px; margin-bottom: 20px;">'
            f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">'
            f'<span style="font-weight: 700; font-size: 0.85rem; color: #0F172A;">{esc(user_name)} ({esc(age)}y)</span>'
            f'<span style="background: #ECFDF5; color: #059669; font-size: 0.7rem; font-weight: 700; padding: 2px 6px; border-radius: 4px;">ACTIVE</span>'
            f'</div>'
            f'<div style="font-size: 0.78rem; color: #64748B; margin-bottom: 8px;">'
            f'<strong>Allergies:</strong> {esc(health[:35])}{"..." if len(health) > 35 else ""}'
            f'</div>'
            f'<div style="background: #E2E8F0; border-radius: 4px; height: 6px; overflow: hidden;">'
            f'<div style="background: #10B981; width: 94%; height: 100%;"></div>'
            f'</div>'
            f'<div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #64748B; margin-top: 4px;">'
            f'<span>Aura Protection</span>'
            f'<span style="font-weight: 600; color: #059669;">94%</span>'
            f'</div>'
            f'</div>'
        )
        st.markdown(widget_html, unsafe_allow_html=True)

        # Logout button
        if st.button("🚪 Logout / Switch Twin", use_container_width=True):
            logout()
