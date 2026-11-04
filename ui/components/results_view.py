import streamlit as st
import pandas as pd
from typing import Union
from models.product import ProductAnalysis
from services.audio_service import generate_voice_bytes

def render_results_view(analysis: Union[ProductAnalysis, dict]) -> None:
    """
    Renders modern, premium product evaluation results with verdict banners,
    WHO insights, interactive price comparisons, and audio readout.
    """
    if isinstance(analysis, dict):
        verdict = analysis.get("verdict", "UNKNOWN")
        prod_name = analysis.get("product_name", "Unknown Product")
        who_verdict = analysis.get("who_verdict", "No WHO data")
        safety_score = analysis.get("safety_score", 0)
        safety_check = analysis.get("safety_check", "")
        voice_script = analysis.get("voice_script", "")
        prices = analysis.get("online_prices", [])
        truth_report = analysis.get("truth_report", "")
    else:
        verdict = analysis.verdict
        prod_name = analysis.product_name
        who_verdict = analysis.who_verdict
        safety_score = analysis.safety_score
        safety_check = analysis.safety_check
        voice_script = analysis.voice_script
        prices = [p.model_dump() if hasattr(p, "model_dump") else dict(p) for p in analysis.online_prices]
        truth_report = analysis.truth_report

    st.markdown("<br>", unsafe_allow_html=True)

    # Dynamic Verdict Banner
    if "BUY" in verdict.upper():
        verdict_bg = "#ECFDF5"
        verdict_border = "#10B981"
        verdict_color = "#065F46"
        icon = "✅"
        badge_text = "VERIFIED SAFE TO BUY"
    elif "THINK" in verdict.upper():
        verdict_bg = "#FFFBEB"
        verdict_border = "#F59E0B"
        verdict_color = "#92400E"
        icon = "⚠️"
        badge_text = "THINK & CONSUME IN MODERATION"
    else:
        verdict_bg = "#FEF2F2"
        verdict_border = "#EF4444"
        verdict_color = "#991B1B"
        icon = "❌"
        badge_text = "AVOID PRODUCT (HEALTH RISK)"

    st.markdown(
        f"""
        <div style="background: {verdict_bg}; border: 1px solid {verdict_border}; border-radius: 16px; padding: 20px 24px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 2rem;">{icon}</span>
                    <div>
                        <div style="font-size: 0.78rem; font-weight: 700; color: {verdict_color}; letter-spacing: 0.05em; text-transform: uppercase;">{badge_text}</div>
                        <div style="font-size: 1.4rem; font-weight: 800; color: #0F172A;">{prod_name}</div>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.75rem; color: #64748B; font-weight: 600;">SAFETY RATING</div>
                    <div style="font-size: 1.8rem; font-weight: 800; color: {verdict_border};">{safety_score} <span style="font-size: 1rem; color: #94A3B8;">/10</span></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Two-column layout for details
    col_left, col_right = st.columns([7, 5])

    with col_left:
        # Factual Truth Report
        st.markdown(
            f"""
            <div class="saas-card">
                <div style="font-weight: 700; font-size: 0.95rem; color: #0F172A; margin-bottom: 8px;">
                    🔬 Ingredient Truth Report
                </div>
                <div style="font-size: 0.88rem; color: #334155; line-height: 1.6;">
                    {truth_report}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # WHO Standards & Guidelines Check
        st.markdown(
            f"""
            <div class="saas-card" style="border-left: 4px solid #3B82F6;">
                <div style="font-weight: 700; font-size: 0.95rem; color: #1E40AF; margin-bottom: 6px;">
                    🌐 World Health Organization (WHO) Benchmark
                </div>
                <div style="font-size: 0.86rem; color: #1E293B; line-height: 1.5;">
                    {who_verdict}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Price Comparison Table
        if prices:
            st.markdown(
                """
                <div style="font-weight: 700; font-size: 0.95rem; color: #0F172A; margin-top: 14px; margin-bottom: 8px;">
                    🛒 Live Price Comparison across Platforms
                </div>
                """,
                unsafe_allow_html=True,
            )
            prices_df = pd.DataFrame(prices)
            st.dataframe(
                prices_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "platform": st.column_config.TextColumn("E-Commerce Platform", width="medium"),
                    "price": st.column_config.TextColumn("Detected Price", width="medium"),
                },
            )

    with col_right:
        # Personalized Safety & Allergy Warnings
        st.markdown(
            f"""
            <div class="saas-card" style="border-left: 4px solid #F59E0B;">
                <div style="font-weight: 700; font-size: 0.95rem; color: #92400E; margin-bottom: 6px;">
                    ⚠️ Digital Twin Health Advisory
                </div>
                <div style="font-size: 0.86rem; color: #78350F; line-height: 1.5;">
                    {safety_check}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Audio Voice Verdict Readout
        if voice_script:
            st.markdown(
                f"""
                <div class="saas-card" style="background: #F8FAFC;">
                    <div style="font-weight: 700; font-size: 0.92rem; color: #0F172A; margin-bottom: 6px;">
                        🔊 AI Voice Summary
                    </div>
                    <div style="font-size: 0.84rem; color: #475569; font-style: italic; margin-bottom: 12px;">
                        "{voice_script}"
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            audio_bytes = generate_voice_bytes(voice_script)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3", autoplay=True)
