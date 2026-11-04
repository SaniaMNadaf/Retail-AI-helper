import streamlit as st
from datetime import datetime
from utils.session import get_user_data, NAV_SCANNER, set_active_nav
from services.history_service import compute_dashboard_metrics
from ui.components import (
    render_top_nav,
    render_stat_cards,
    render_interactive_charts,
    render_quick_actions,
    render_progress_section,
    render_records_table,
    render_safety_alert_banner,
)

def render_dashboard_overview() -> None:
    """Renders the main modern SaaS dashboard view with KPI cards, charts, alerts, and records."""
    user = get_user_data()
    user_name = user.get("name", "Aarav Sharma")
    records = st.session_state.get("scan_history", [])
    metrics = compute_dashboard_metrics(records)

    # 1. Top Navigation Bar
    render_top_nav()

    # 2. Welcome & Context Header
    today_str = datetime.now().strftime("%A, %B %d, %Y")
    welcome_html = (
        f'<div class="welcome-banner">'
        f'<div>'
        f'<div style="font-size: 0.85rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">{today_str}</div>'
        f'<div style="font-size: 1.75rem; font-weight: 800; margin: 4px 0 6px 0;">Welcome back, {user_name}! 👋</div>'
        f'<div style="font-size: 0.92rem; opacity: 0.95; max-width: 600px; line-height: 1.5;">'
        f'Your AI Shopping Bodyguard has monitored <strong>{metrics.get("total_scans", 0)} items</strong> with an average health score of <strong>{metrics.get("avg_safety", "0.0")}/10</strong>.'
        f'</div>'
        f'</div>'
        f'<div style="display: flex; gap: 10px; align-items: center;">'
        f'<div style="background: rgba(255, 255, 255, 0.18); backdrop-filter: blur(8px); padding: 10px 16px; border-radius: 12px; text-align: center; border: 1px solid rgba(255, 255, 255, 0.25);">'
        f'<div style="font-size: 0.72rem; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em;">Shield Rating</div>'
        f'<div style="font-size: 1.4rem; font-weight: 800;">{metrics.get("safe_percentage", 85)}% Safe</div>'
        f'</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(welcome_html, unsafe_allow_html=True)

    # 3. High-Priority Safety Alert Banner
    render_safety_alert_banner(records)

    # 4. Key Performance Statistic Cards (4 Columns)
    render_stat_cards(metrics)

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. Interactive Charts & Analytics (Trends + Verdict Donut)
    render_interactive_charts(records)

    # 6. Quick Action Buttons
    render_quick_actions()

    # 7. Health Goals & Progress Indicators
    render_progress_section(metrics)

    # 8. Recent Activity / Transactions Table (Limit to 5 on main dashboard)
    render_records_table(records, limit=5, show_filters=False)

    # View All Link Button
    if len(records) > 5:
        c_spacer, c_btn, _ = st.columns([4, 2, 4])
        with c_btn:
            from utils.session import NAV_RECORDS
            if st.button("View Full Scan History →", use_container_width=True):
                set_active_nav(NAV_RECORDS)
