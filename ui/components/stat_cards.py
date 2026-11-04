import streamlit as st
from typing import Dict, Any

def render_stat_cards(metrics: Dict[str, Any]) -> None:
    """Renders 4 key performance statistic cards with trends and modern SaaS card styling."""
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        html_c1 = (
            f'<div class="stat-card">'
            f'<div class="stat-card-header">'
            f'<span class="stat-card-title">Products Scanned</span>'
            f'<div class="stat-card-icon" style="background: #EEF2FF; color: #4F46E5;">🏷️</div>'
            f'</div>'
            f'<div class="stat-card-value">{metrics.get("total_scans", 0)}</div>'
            f'<div class="stat-card-footer">'
            f'<span class="stat-badge-positive">↑ +14%</span>&nbsp;'
            f'<span style="color: #64748B;">vs last week</span>'
            f'</div>'
            f'</div>'
        )
        st.markdown(html_c1, unsafe_allow_html=True)

    with c2:
        avg_score = metrics.get('avg_safety', '0.0')
        html_c2 = (
            f'<div class="stat-card">'
            f'<div class="stat-card-header">'
            f'<span class="stat-card-title">Safety Index</span>'
            f'<div class="stat-card-icon" style="background: #ECFDF5; color: #059669;">✨</div>'
            f'</div>'
            f'<div class="stat-card-value">{avg_score} <span style="font-size: 1rem; color: #94A3B8; font-weight: 500;">/10</span></div>'
            f'<div class="stat-card-footer">'
            f'<span class="stat-badge-positive">↑ +0.6 pts</span>&nbsp;'
            f'<span style="color: #64748B;">WHO standards</span>'
            f'</div>'
            f'</div>'
        )
        st.markdown(html_c2, unsafe_allow_html=True)

    with c3:
        alerts = metrics.get('alerts_avoided', 0)
        html_c3 = (
            f'<div class="stat-card">'
            f'<div class="stat-card-header">'
            f'<span class="stat-card-title">Allergen Hazards Avoided</span>'
            f'<div class="stat-card-icon" style="background: #FEF3C7; color: #D97706;">⚠️</div>'
            f'</div>'
            f'<div class="stat-card-value">{alerts}</div>'
            f'<div class="stat-card-footer">'
            f'<span class="stat-badge-positive">100% Aura</span>&nbsp;'
            f'<span style="color: #64748B;">risks intercepted</span>'
            f'</div>'
            f'</div>'
        )
        st.markdown(html_c3, unsafe_allow_html=True)

    with c4:
        savings = metrics.get('money_saved', '₹0')
        html_c4 = (
            f'<div class="stat-card">'
            f'<div class="stat-card-header">'
            f'<span class="stat-card-title">Est. Price Savings</span>'
            f'<div class="stat-card-icon" style="background: #F3E8FF; color: #9333EA;">💰</div>'
            f'</div>'
            f'<div class="stat-card-value">{savings}</div>'
            f'<div class="stat-card-footer">'
            f'<span class="stat-badge-neutral">Blinkit & Amazon</span>&nbsp;'
            f'<span style="color: #64748B;">live arbitrage</span>'
            f'</div>'
            f'</div>'
        )
        st.markdown(html_c4, unsafe_allow_html=True)
