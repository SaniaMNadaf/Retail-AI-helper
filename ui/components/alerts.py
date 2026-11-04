import streamlit as st
from typing import List
from models.scan_record import ScanRecord


def render_safety_alert_banner(records: List[ScanRecord] = None) -> None:
    """Renders a prominent, high-priority safety alert card on the dashboard if risks exist."""
    if records is None:
        records = st.session_state.get("scan_history", [])
    
    # Find recent AVOID verdicts and flagged ingredients
    recent_avoid = [r for r in records[:5] if r.verdict == "AVOID"]
    all_flagged = []
    for r in records[:10]:
        all_flagged.extend(r.flagged_ingredients)
    
    # Get unique flagged ingredients
    unique_flagged = list(dict.fromkeys(all_flagged))[:3]
    
    if not recent_avoid and not unique_flagged:
        return  # No alerts to show
    
    if recent_avoid:
        product_names = [r.product_name for r in recent_avoid[:2]]
        products_str = " and ".join([f'<span style="color: #1D4ED8 !important; font-weight: bold;">{name}</span>' for name in product_names])
        message = f"Recently evaluated {products_str} received AVOID verdict. Your digital twin advises against these."
    else:
        ingredients_str = ", ".join([f'<span style="color: #1D4ED8 !important; font-weight: bold;">{ing}</span>' for ing in unique_flagged])
        message = f"Recent scans flagged {ingredients_str}. Your digital twin advises caution with these ingredients."

    st.markdown(
        f"""
        <div style="background: #FFFFFF !important; border: 1px solid #BFDBFE !important; border-left: 5px solid #2563EB !important; border-radius: 12px; padding: 16px 20px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 16px rgba(0,0,0,0.15) !important;">
            <div style="display: flex; gap: 14px; align-items: center;">
                <div style="font-size: 1.5rem;">⚠️</div>
                <div>
                    <div style="font-weight: 700; font-size: 0.92rem; color: #1E40AF !important;">Active Allergy Guard Triggered</div>
                    <div style="font-size: 0.82rem; color: #1E3A8A !important; margin-top: 2px;">
                        {message}
                    </div>
                </div>
            </div>
            <div>
                <span style="background: #DBEAFE !important; color: #1E40AF !important; font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 6px; border: 1px solid #BFDBFE !important;">
                    HIGH PRIORITY
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
