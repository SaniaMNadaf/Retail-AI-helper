import streamlit as st
from datetime import datetime
from utils.session import (
    set_active_nav,
    get_user_data,
    NAV_SCANNER,
    NAV_TWIN,
    NAV_RECORDS,
)
from models.user import UserProfile
from services.export_service import generate_audit_csv

def render_quick_actions() -> None:
    """Renders modern quick-action shortcut cards with micro-interactions."""
    st.markdown(
        """
        <div style="font-weight: 700; font-size: 1rem; color: #0F172A; margin-top: 10px; margin-bottom: 12px;">
            ⚡ Quick Actions
        </div>
        """,
        unsafe_allow_html=True,
    )

    q1, q2, q3 = st.columns(3)

    with q1:
        if st.button("📸 Scan Label", use_container_width=True, help="Scan camera or upload barcode/ingredient image"):
            set_active_nav(NAV_SCANNER)

    with q2:
        if st.button("🧬 Edit Digital Twin", use_container_width=True, help="Update allergies, dietary restrictions, and age"):
            set_active_nav(NAV_TWIN)

    with q3:
        if st.button("📜 Full History", use_container_width=True, help="Browse all past scanned food and cosmetic items"):
            set_active_nav(NAV_RECORDS)
