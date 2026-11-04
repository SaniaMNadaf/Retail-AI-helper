import streamlit as st
from config.settings import PAGE_HOME, DEFAULT_PREFERENCES
from utils.session import get_user_data, update_user_data, navigate_to
from ui.components.twin_form import render_twin_form

def render_cloning_page() -> None:
    """Renders Page 3: Modern onboarding for creating the Digital Twin profile."""
    st.markdown("<br>", unsafe_allow_html=True)
    _, main_col, _ = st.columns([1, 3, 1])

    with main_col:
        st.markdown(
            """
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 24px; padding: 36px; box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.05); margin-bottom: 24px;">
                <div style="text-align: center; margin-bottom: 28px;">
                    <div style="font-size: 2.2rem; margin-bottom: 8px;">🧬</div>
                    <div style="font-size: 1.8rem; font-weight: 800; color: #0F172A;">Create Your Digital Twin</div>
                    <div style="font-size: 0.9rem; color: #64748B;">
                        Calibrate your personalized bodyguard rules, health restrictions, and shopping targets.
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )

        def on_submit():
            navigate_to(PAGE_HOME)

        render_twin_form(
            form_key="twin_onboarding_form",
            submit_label="✨ Generate Digital Twin & Enter Dashboard",
            on_submit_callback=on_submit,
            show_photo=True,
            extended_options=False,
        )

        st.markdown("</div>", unsafe_allow_html=True)
