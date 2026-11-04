import streamlit as st
from utils.session import (
    get_user_data,
    set_active_nav,
    NAV_SCANNER,
)

def render_top_nav() -> None:
    """Renders the top navigation bar with search, notification popover, avatar, and quick action."""
    user = get_user_data()
    user_name = user.get("name", "Aarav Sharma")
    notifications = st.session_state.get("notifications", [])
    unread_count = len(notifications)

    with st.container(border=True):
        col_search, col_actions, col_profile = st.columns([5, 3, 2], vertical_alignment="center")

        with col_search:
            search_val = st.text_input(
                "Search",
                placeholder="🔍 Search scanned foods, ingredients, or brand names...",
                label_visibility="collapsed",
                key="global_search_input",
            )
            if search_val != st.session_state.get("search_query", ""):
                st.session_state.search_query = search_val

        with col_actions:
            btn_c1, btn_c2 = st.columns([1, 1], vertical_alignment="center")
            with btn_c1:
                with st.popover(f"🔔 Alerts ({unread_count})", use_container_width=True):
                    st.markdown("### 🔔 Recent Notifications")
                    for notif in notifications:
                        icon = "⚠️" if notif["type"] == "warning" else ("✅" if notif["type"] == "success" else "ℹ️")
                        notif_html = (
                            f'<div style="padding: 10px; border-radius: 8px; margin-bottom: 8px; background: #F8FAFC; border: 1px solid #E2E8F0;">'
                            f'<div style="font-weight: 600; font-size: 0.88rem; color: #0F172A;">{icon} {notif["title"]}</div>'
                            f'<div style="font-size: 0.8rem; color: #64748B; margin-top: 2px;">{notif["message"]}</div>'
                            f'<div style="font-size: 0.72rem; color: #94A3B8; margin-top: 4px;">{notif["time"]}</div>'
                            f'</div>'
                        )
                        st.markdown(notif_html, unsafe_allow_html=True)
            with btn_c2:
                if st.button("⚡ Quick Scan", type="primary", use_container_width=True):
                    set_active_nav(NAV_SCANNER)

        with col_profile:
            avatar_col1, avatar_col2 = st.columns([1, 3], vertical_alignment="center")
            with avatar_col1:
                avatar_html = (
                    '<div style="width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #4F46E5, #06B6D4); '
                    'display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 1rem; '
                    'box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3);">👤</div>'
                )
                st.markdown(avatar_html, unsafe_allow_html=True)
            with avatar_col2:
                profile_html = (
                    '<div style="line-height: 1.2;">'
                    f'<div style="font-weight: 700; font-size: 0.88rem; color: #0F172A;">{user_name}</div>'
                    '<div style="font-size: 0.75rem; color: #10B981; font-weight: 600;">● Aura Active</div>'
                    '</div>'
                )
                st.markdown(profile_html, unsafe_allow_html=True)
