import streamlit as st
import pandas as pd
import altair as alt
from typing import List
from datetime import datetime, timedelta
from collections import defaultdict
from models.scan_record import ScanRecord


def _get_trend_data(records: List[ScanRecord]) -> pd.DataFrame:
    """Generate 7-day trend data from actual scan records."""
    days_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    today = datetime.now()
    
    daily_scores = defaultdict(list)
    daily_counts = defaultdict(int)
    
    for record in records:
        record_date = None
        ts = record.timestamp.lower() if record.timestamp else ""
        if "today" in ts:
            record_date = today
        elif "yesterday" in ts:
            record_date = today - timedelta(days=1)
        elif "days ago" in ts or "day ago" in ts:
            try:
                parts = ts.split()
                days_num = int(parts[0])
                record_date = today - timedelta(days=days_num)
            except (ValueError, IndexError):
                record_date = today - timedelta(days=2)
        else:
            try:
                record_date = datetime.strptime(record.timestamp, "%Y-%m-%d %H:%M")
            except ValueError:
                try:
                    record_date = datetime.strptime(record.timestamp, "%a, %b %d, %Y")
                except ValueError:
                    record_date = today
        
        if record_date:
            days_diff = (today - record_date).days
            if 0 <= days_diff < 7:
                day_name = record_date.strftime("%a")
                daily_scores[day_name].append(record.safety_score)
                daily_counts[day_name] += 1
    
    trend_data = []
    for i, day in enumerate(days_order):
        target_date = today - timedelta(days=6-i)
        day_name = target_date.strftime("%a")
        
        scores = daily_scores.get(day_name, [])
        avg_score = sum(scores) / len(scores) if scores else 0
        count = daily_counts.get(day_name, 0)
        
        trend_data.append({
            "Day": day,
            "Safety Score": round(avg_score, 1) if avg_score > 0 else None,
            "Products Scanned": count,
        })
    
    return pd.DataFrame(trend_data)


def render_interactive_charts(records: List[ScanRecord]) -> None:
    """Renders interactive charts for scanning activity trends and verdict distribution."""
    col_chart1, col_chart2 = st.columns([7, 5])

    with col_chart1:
        st.markdown(
            """
            <div style="font-weight: 700; font-size: 1rem; color: #0F172A; margin-bottom: 4px;">
                📈 Safe Shopping & Activity Trends
            </div>
            <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 12px;">
                Safety scores and volume of scanned items over the past 7 days
            </div>
            """,
            unsafe_allow_html=True,
        )

        trend_df = _get_trend_data(records)
        
        # Filter out days with no data for line chart
        line_df = trend_df[trend_df["Safety Score"].notna()].copy()
        
        # Dual visual chart with Altair
        base = alt.Chart(trend_df).encode(x=alt.X("Day:N", sort=None, title=None))

        bar = base.mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, color="#EEF2FF", size=24).encode(
            y=alt.Y("Products Scanned:Q", title="Items Scanned", axis=alt.Axis(tickMinStep=1)),
            tooltip=["Day", "Products Scanned", "Safety Score"],
        )

        combined_chart = alt.layer(bar).resolve_scale(y="independent").properties(
            height=260,
            padding={"left": 10, "top": 10, "right": 10, "bottom": 10},
        ).configure_view(strokeWidth=0).configure_axis(
            gridColor="#F1F5F9",
            labelColor="#64748B",
            titleColor="#475569",
            labelFont="Plus Jakarta Sans, Inter, sans-serif",
            titleFont="Plus Jakarta Sans, Inter, sans-serif",
        )
        
        # Add line chart if we have score data
        if not line_df.empty:
            line_base = alt.Chart(line_df).encode(x=alt.X("Day:N", sort=None, title=None))
            line = line_base.mark_line(color="#4F46E5", strokeWidth=3, interpolate="monotone").encode(
                y=alt.Y("Safety Score:Q", title="Safety Index (out of 10)", scale=alt.Scale(domain=[0, 10])),
                tooltip=["Day", "Safety Score", "Products Scanned"],
            )
            points = line_base.mark_circle(size=60, color="#4F46E5").encode(
                y=alt.Y("Safety Score:Q"),
                tooltip=["Day", "Safety Score", "Products Scanned"],
            )
            combined_chart = alt.layer(bar, line, points).resolve_scale(y="independent").properties(
                height=260,
                padding={"left": 10, "top": 10, "right": 10, "bottom": 10},
            ).configure_view(strokeWidth=0).configure_axis(
                gridColor="#F1F5F9",
                labelColor="#64748B",
                titleColor="#475569",
                labelFont="Plus Jakarta Sans, Inter, sans-serif",
                titleFont="Plus Jakarta Sans, Inter, sans-serif",
            )

        st.altair_chart(combined_chart, use_container_width=True)

    with col_chart2:
        st.markdown(
            """
            <div style="font-weight: 700; font-size: 1rem; color: #0F172A; margin-bottom: 4px;">
                🎯 Verdict Breakdown
            </div>
            <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 12px;">
                Distribution of AI purchase recommendations
            </div>
            """,
            unsafe_allow_html=True,
        )

        buy_count = sum(1 for r in records if r.verdict == "BUY")
        think_count = sum(1 for r in records if r.verdict == "THINK")
        avoid_count = sum(1 for r in records if r.verdict == "AVOID")

        verdict_df = pd.DataFrame({
            "Verdict": ["BUY (Safe)", "THINK (Caution)", "AVOID (Hazard)"],
            "Count": [buy_count, think_count, avoid_count],
            "Color": ["#10B981", "#F59E0B", "#EF4444"],
        })

        # If no data, show placeholder
        if buy_count == 0 and think_count == 0 and avoid_count == 0:
            st.info("No scan data yet. Scan a product to see your verdict breakdown!")
            return

        donut_chart = alt.Chart(verdict_df).mark_arc(innerRadius=55, stroke="#FFFFFF", strokeWidth=2).encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(
                field="Verdict",
                type="nominal",
                scale=alt.Scale(
                    domain=["BUY (Safe)", "THINK (Caution)", "AVOID (Hazard)"],
                    range=["#10B981", "#F59E0B", "#EF4444"],
                ),
                legend=alt.Legend(
                    orient="bottom",
                    direction="horizontal",
                    title=None,
                    labelFont="Plus Jakarta Sans, Inter, sans-serif",
                ),
            ),
            tooltip=["Verdict", "Count"],
        ).properties(
            height=260,
        ).configure_view(strokeWidth=0)

        st.altair_chart(donut_chart, use_container_width=True)
