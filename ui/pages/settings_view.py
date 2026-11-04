import streamlit as st
from ui.components import render_top_nav
from config.settings import DEFAULT_GEMINI_MODEL, API_KEY
from services.history_service import get_initial_records
from services.database_service import get_user_settings, update_user_settings

def render_settings_view() -> None:
    """Renders the settings and system configuration view."""
    render_top_nav()

    # Load settings from database
    settings = get_user_settings()
    
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #0F172A;">⚙️ Application Settings</div>
            <div style="font-size: 0.88rem; color: #64748B;">
                Manage your AI model configurations, alert sensitivity, and shopping preferences.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            """
            <div class="saas-card">
                <div style="font-weight: 700; font-size: 1rem; color: #0F172A; margin-bottom: 12px;">
                    🎨 Appearance & Theme
                </div>
            """,
            unsafe_allow_html=True,
        )

        theme_options = ["Light Mode", "Dark Mode", "System Default"]
        current_theme = getattr(settings, "theme", "Light Mode")
        theme_index = theme_options.index(current_theme) if current_theme in theme_options else 0
        new_theme = st.radio("Select Application Theme", options=theme_options, index=theme_index, horizontal=True)
        if new_theme != current_theme:
            update_user_settings({"theme": new_theme})
            st.toast(f"✅ Theme updated to {new_theme}", icon="🎨")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="saas-card">
                <div style="font-weight: 700; font-size: 1rem; color: #0F172A; margin-bottom: 12px;">
                    🛒 E-Commerce & Currency
                </div>
            """,
            unsafe_allow_html=True,
        )
        currency_options = ["₹ INR (India)", "$ USD", "€ EUR", "£ GBP"]
        currency_index = currency_options.index(settings.currency) if settings.currency in currency_options else 0
        new_currency = st.selectbox("Default Currency", currency_options, index=currency_index)
        if new_currency != settings.currency:
            update_user_settings({"currency": new_currency})
            st.toast("✅ Currency updated", icon="💰")

        platform_options = ["Blinkit", "Amazon India", "Swiggy Instamart", "Zepto", "BigBasket"]
        new_platforms = st.multiselect(
            "Priority Shopping Platforms",
            platform_options,
            default=settings.priority_platforms,
        )
        if set(new_platforms) != set(settings.priority_platforms):
            update_user_settings({"priority_platforms": new_platforms})
            st.toast("✅ Platforms updated", icon="🛒")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            """
            <div class="saas-card">
                <div style="font-weight: 700; font-size: 1rem; color: #0F172A; margin-bottom: 12px;">
                    🚨 Audio & Alert Sensitivity
                </div>
            """,
            unsafe_allow_html=True,
        )
        new_auto_play = st.toggle("Auto-play voice verdict on scan", value=settings.auto_play_voice)
        if new_auto_play != settings.auto_play_voice:
            update_user_settings({"auto_play_voice": new_auto_play})
            st.toast("✅ Audio setting updated", icon="🔊")

        new_push_notif = st.toggle("Push high-priority allergen notifications", value=settings.push_notifications)
        if new_push_notif != settings.push_notifications:
            update_user_settings({"push_notifications": new_push_notif})
            st.toast("✅ Notification setting updated", icon="🔔")

        new_threshold = st.slider("Minimum Safe Score Threshold", min_value=1, max_value=10, value=settings.safe_score_threshold, help="Products below this score receive THINK or AVOID warnings.")
        if new_threshold != settings.safe_score_threshold:
            update_user_settings({"safe_score_threshold": new_threshold})
            st.toast("✅ Threshold updated", icon="✨")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="saas-card">
                <div style="font-weight: 700; font-size: 1rem; color: #0F172A; margin-bottom: 12px;">
                    🧹 Data Management
                </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption("Reset your session history or restore default test scans.")
        if st.button("Reset Scan History to Sample Data"):
            st.session_state.scan_history = get_initial_records()
            st.session_state.last_analysis = None
            st.toast("✅ Scan history reset to sample records.", icon="🔄")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
