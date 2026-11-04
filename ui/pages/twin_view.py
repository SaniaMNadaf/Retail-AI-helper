import streamlit as st
from ui.components import render_top_nav
from ui.components.twin_form import render_twin_form, render_twin_preview_card
from utils.session import get_user_data

def render_twin_view() -> None:
    """Renders the Digital Twin & Health Profile management screen."""
    render_top_nav()

    header_html = (
        '<div style="margin-bottom: 20px;">'
        '<div style="font-size: 1.5rem; font-weight: 800; color: #0F172A;">🧬 Digital Twin Health Profile</div>'
        '<div style="font-size: 0.88rem; color: #64748B;">'
        'Aura Sathi compares every ingredient against your personalized profile to protect your health and dietary preferences.'
        '</div>'
        '</div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)

    user = get_user_data()

    col_form, col_preview = st.columns([7, 5], gap="large")

    with col_form:
        render_twin_form(
            form_key="edit_twin_form",
            submit_label="💾 Save Digital Twin Updates",
            extended_options=True,
        )

    with col_preview:
        st.markdown("#### ✨ Active Aura Twin Card")
        render_twin_preview_card(user)
