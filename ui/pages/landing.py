import streamlit as st
from config.settings import PAGE_LOGIN, PAGE_HOME, APP_TITLE, APP_SUBTITLE
from utils.session import navigate_to
from ui.components.logo import render_logo

def render_landing_page() -> None:
    """Renders Page 1: Modern, clean SaaS landing hero screen."""
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:
        logo_html = render_logo(80)
        st.markdown(
            f"""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 24px; padding: 48px 36px; text-align: center; box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.05);">
                <div style="display: flex; justify-content: center; margin-bottom: 20px;">
                    {logo_html}
                </div>
                <div style="font-size: 2.2rem; font-weight: 800; color: #0F172A; letter-spacing: -0.02em; margin-bottom: 8px;">
                    {APP_TITLE}
                </div>
                <div style="font-size: 1.05rem; color: #64748B; font-weight: 500; margin-bottom: 24px;">
                    {APP_SUBTITLE}
                </div>
                <div style="display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; margin-bottom: 32px;">
                    <span style="background: #F1F5F9; color: #475569; font-size: 0.8rem; font-weight: 600; padding: 5px 12px; border-radius: 20px;">🌐 WHO Guidelines</span>
                    <span style="background: #ECFDF5; color: #059669; font-size: 0.8rem; font-weight: 600; padding: 5px 12px; border-radius: 20px;">🧬 Allergy Twin Shield</span>
                    <span style="background: #EEF2FF; color: #4F46E5; font-size: 0.8rem; font-weight: 600; padding: 5px 12px; border-radius: 20px;">💰 Live Price Comparison</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        btn1, btn2 = st.columns([1, 1])
        with btn1:
            if st.button("🚀 Get Started →", type="primary", use_container_width=True):
                navigate_to(PAGE_LOGIN)
        with btn2:
            if st.button("📊 Open Dashboard Directly", use_container_width=True):
                navigate_to(PAGE_HOME)
