import streamlit as st
from ui.components import render_top_nav, render_records_table
from services.history_service import compute_dashboard_metrics

def render_records_view() -> None:
    """Renders the full scan history and records log."""
    render_top_nav()

    records = st.session_state.get("scan_history", [])
    metrics = compute_dashboard_metrics(records)

    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #0F172A;">📜 Full Scan History & Records</div>
            <div style="font-size: 0.88rem; color: #64748B;">
                Complete record of {metrics.get('total_scans', 0)} evaluated products with WHO benchmark compliance and price arbitrage.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Mini summary cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Archive", f"{metrics.get('total_scans', 0)} items")
    with m2:
        st.metric("BUY Approved", f"{metrics.get('buy_count', 0)} items")
    with m3:
        st.metric("THINK (Caution)", f"{metrics.get('think_count', 0)} items")
    with m4:
        st.metric("AVOID (Hazard)", f"{metrics.get('avoid_count', 0)} items")

    st.markdown("<br>", unsafe_allow_html=True)
    render_records_table(records, show_filters=True)
