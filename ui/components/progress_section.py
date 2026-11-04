import streamlit as st
from typing import Dict, Any

def render_progress_section(metrics: Dict[str, Any]) -> None:
    """Renders progress indicators and health goal trackers using native container borders."""
    st.markdown(
        """
        <div style="font-weight: 700; font-size: 1rem; color: #0F172A; margin-top: 14px; margin-bottom: 12px;">
            🎯 Health Goals & Shield Coverage
        </div>
        """,
        unsafe_allow_html=True,
    )

    safe_pct = metrics.get("safe_percentage", 82)
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-weight: 600; font-size: 0.88rem; color: #0F172A;">Weekly Safe Shopping Target</span>
                    <span style="font-weight: 700; font-size: 0.88rem; color: #10B981;">{safe_pct}%</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.progress(safe_pct / 100)
            st.caption("Goal: 80% or higher clean pantry rating")

    with col2:
        with st.container(border=True):
            st.markdown(
                """
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-weight: 600; font-size: 0.88rem; color: #0F172A;">Allergen Filter Coverage</span>
                    <span style="font-weight: 700; font-size: 0.88rem; color: #4F46E5;">100% Active</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.progress(1.0)
            st.caption("Lactose & Sodium sensitivity rules enforced")

    with col3:
        with st.container(border=True):
            st.markdown(
                """
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-weight: 600; font-size: 0.88rem; color: #0F172A;">WHO Added-Sugar Compliance</span>
                    <span style="font-weight: 700; font-size: 0.88rem; color: #F59E0B;">76% Compliant</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.progress(0.76)
            st.caption("Items scanned under <25g/day free-sugar limit")
