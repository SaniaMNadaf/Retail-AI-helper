import streamlit as st
from config.settings import PAGE_CLONING, PAGE_HOME, APP_TITLE, PAGE_REGISTER
from utils.session import navigate_to, login_user, is_logged_in
from services.auth_service import authenticate_user, create_user

def render_login_page() -> None:
    """Renders Page 2: Modern SaaS split authentication card."""
    # Redirect if already logged in
    if is_logged_in():
        navigate_to(PAGE_HOME)
        return
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, main_col, _ = st.columns([1, 2, 1])

    with main_col:
        st.markdown(
            f"""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 24px; padding: 36px; box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.05); margin-bottom: 20px;">
                <div style="text-align: center; margin-bottom: 24px;">
                    <div style="font-size: 2rem; margin-bottom: 8px;">✨</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #0F172A;">Welcome to {APP_TITLE}</div>
                    <div style="font-size: 0.88rem; color: #64748B;">Sign in to access your AI Wellness Bodyguard</div>
                </div>
            """,
            unsafe_allow_html=True,
        )

        # Login form
        with st.form("login_form"):
            l_email = st.text_input("Email", placeholder="e.g. user@aurasathi.ai")
            l_pass = st.text_input("Password", type="password", placeholder="Enter your password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("Sign In →", type="primary", use_container_width=True):
                if not l_email or not l_pass:
                    st.error("❌ Please enter both email and password")
                else:
                    success, msg, user = authenticate_user(l_email, l_pass)
                    if success:
                        login_user(user.id)
                        st.toast(f"✅ {msg}", icon="✨")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

        st.markdown("<p style='text-align:center; color:#94A3B8; font-size:0.8rem; margin: 16px 0 12px 0;'>OR</p>", unsafe_allow_html=True)

        c_btn1, c_btn2 = st.columns([1, 1])
        with c_btn1:
            if st.button("🧬 Setup Digital Twin", use_container_width=True):
                navigate_to(PAGE_CLONING)

        with c_btn2:
            if st.button("🌐 Continue with Google", use_container_width=True):
                # Placeholder for Google OAuth
                st.info("Google OAuth integration coming soon!")

        st.markdown("<p style='text-align:center; color:#94A3B8; font-size:0.8rem; margin: 16px 0 12px 0;'>NEW HERE?</p>", unsafe_allow_html=True)
        
        if st.button("📝 Create Account", type="primary", use_container_width=True):
            navigate_to(PAGE_REGISTER)

        st.markdown("</div>", unsafe_allow_html=True)
