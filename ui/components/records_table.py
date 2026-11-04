import streamlit as st
import pandas as pd
from typing import List
from models.scan_record import ScanRecord

def render_records_table(records: List[ScanRecord], limit: int = None, show_filters: bool = True) -> None:
    """Renders a modern, filterable table of scanned items with badges and export capabilities."""
    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 18px; margin-bottom: 12px;">
            <div>
                <span style="font-weight: 700; font-size: 1.05rem; color: #0F172A;">📋 Recent Activity & Scanned Items</span>
                <span style="font-size: 0.8rem; color: #64748B; margin-left: 8px;">Real-time feed of AI product evaluations</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    filtered_records = records

    if show_filters:
        f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
        with f_col1:
            global_q = st.session_state.get("search_query", "")
            table_q = st.text_input(
                "Filter items",
                value=global_q,
                placeholder="Filter by product name, ingredient, or brand...",
                label_visibility="collapsed",
                key="table_search_filter",
            )
        with f_col2:
            verdict_filter = st.selectbox(
                "Verdict Filter",
                options=["All Verdicts", "BUY (Safe)", "THINK (Caution)", "AVOID (Hazard)"],
                label_visibility="collapsed",
            )
        with f_col3:
            category_filter = st.selectbox(
                "Category Filter",
                options=["All Categories", "Dairy & Eggs", "Beverages", "Cereals & Grains", "Snacks & Confectionery", "Breakfast & Spreads"],
                label_visibility="collapsed",
            )

        if table_q:
            filtered_records = [
                r for r in filtered_records
                if table_q.lower() in r.product_name.lower() or any(table_q.lower() in f.lower() for f in r.flagged_ingredients)
            ]

        if verdict_filter != "All Verdicts":
            code = "BUY" if "BUY" in verdict_filter else ("THINK" if "THINK" in verdict_filter else "AVOID")
            filtered_records = [r for r in filtered_records if r.verdict == code]

        if category_filter != "All Categories":
            filtered_records = [r for r in filtered_records if r.category == category_filter]

    if limit and limit > 0:
        filtered_records = filtered_records[:limit]

    # Handle Empty State
    if not filtered_records:
        st.markdown(
            """
            <div style="background: #FFFFFF; border: 1px dashed #CBD5E1; border-radius: 14px; padding: 36px; text-align: center; margin: 12px 0;">
                <div style="font-size: 2rem; margin-bottom: 8px;">🔍</div>
                <div style="font-weight: 700; color: #0F172A; font-size: 1rem;">No matching product scans found</div>
                <div style="font-size: 0.85rem; color: #64748B; margin-top: 4px;">Try clearing search filters or scan a new product label.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Prepare DataFrame for clean display
    table_rows = []
    for r in filtered_records:
        badge_emoji = "✅" if r.verdict == "BUY" else ("⚠️" if r.verdict == "THINK" else "❌")
        table_rows.append({
            "Verdict": f"{badge_emoji} {r.verdict}",
            "Product": r.product_name,
            "Category": r.category,
            "Safety Score": f"{r.safety_score} / 10",
            "Best Price": r.price,
            "Flagged Risks": ", ".join(r.flagged_ingredients) if r.flagged_ingredients else "None (Clean)",
            "Date/Time": r.timestamp,
        })

    df = pd.DataFrame(table_rows)

    # Display clean table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Verdict": st.column_config.TextColumn("AI Verdict", width="small"),
            "Product": st.column_config.TextColumn("Product Name", width="large"),
            "Category": st.column_config.TextColumn("Category", width="medium"),
            "Safety Score": st.column_config.TextColumn("Safety", width="small"),
            "Best Price": st.column_config.TextColumn("Live Price", width="medium"),
            "Flagged Risks": st.column_config.TextColumn("Allergen / Risk Flags", width="medium"),
            "Date/Time": st.column_config.TextColumn("Timestamp", width="small"),
        },
    )
