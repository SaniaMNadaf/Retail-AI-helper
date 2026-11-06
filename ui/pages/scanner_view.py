import streamlit as st
from ui.components import render_top_nav, render_results_view
from services.ai_service import analyze_product_image, apply_score_threshold
from services.history_service import add_scan_to_history
from services.database_service import get_user_settings
from utils.session import get_user_data, get_current_user_id
from config.settings import APP_TITLE
from utils.validation import validate_file_upload

def render_scanner_view() -> None:
    """Renders the AI Scanner view with camera capture, image upload, and live evaluation."""
    render_top_nav()

    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #0F172A;">📸 AI Scanner</div>
            <div style="font-size: 0.88rem; color: #64748B;">
                Point your camera or upload a package label to cross-reference ingredients with WHO guidelines and your health allergies.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(["📸 Camera Scanner", "📁 Upload Image / Label"])

    img_file = None
    upload_error = None
    with tab1:
        cam = st.camera_input("Scan Product Packaging / Ingredients")
        if cam:
            img_file = cam

    with tab2:
        up = st.file_uploader("Upload Product Picture", type=["jpg", "png", "jpeg"], help="Support formats: JPG, PNG, WEBP")
        if up:
            is_valid, msg = validate_file_upload(up, ["image/jpeg", "image/png", "image/webp"], max_size_mb=10)
            if not is_valid:
                upload_error = msg
                st.error(f"❌ {msg}")
            else:
                img_file = up

    st.caption("💡 Tip: Ensure the ingredients list and nutritional facts table are clearly visible and well lit.")

    if upload_error:
        st.warning("⚠️ Please fix the upload error above before analyzing.")

    if st.button("🚀 ANALYZE THE PRODUCT", type="primary", use_container_width=True):
        if not img_file:
            st.warning("⚠️ Please capture or upload a product photo first.")
        elif upload_error:
            st.warning("⚠️ Please fix the upload error above before analyzing.")
        else:
            with st.spinner("🤖 Aura Sathi is reading ingredients, checking WHO guidelines, and fetching prices..."):
                try:
                    img_bytes = img_file.getvalue()
                    mime_type = getattr(img_file, "type", "image/jpeg") or "image/jpeg"
                    user_data = get_user_data()
                    user_id = get_current_user_id()
                    settings = get_user_settings(user_id) if user_id else None
                    priority_platforms = getattr(settings, "priority_platforms", None) if settings else None

                    analysis = analyze_product_image(
                        image_bytes=img_bytes,
                        mime_type=mime_type,
                        user_data=user_data,
                        priority_platforms=priority_platforms,
                    )

                    # Apply score threshold setting
                    threshold = getattr(settings, "safe_score_threshold", 1) if settings else 1
                    analysis = apply_score_threshold(analysis, threshold)

                    # Automatically register into history
                    add_scan_to_history(analysis)
                    st.session_state.last_analysis = analysis
                    st.toast(f"✅ Product evaluated: {analysis.product_name} ({analysis.verdict})", icon="✨")
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")

    # Display active analysis results if available
    if st.session_state.get("last_analysis"):
        render_results_view(st.session_state.last_analysis)
