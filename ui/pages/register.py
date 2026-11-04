import streamlit as st
from config.settings import PAGE_LOGIN, PAGE_HOME, APP_TITLE
from utils.session import navigate_to, login_user
from services.auth_service import create_user

def render_register_page() -> None:
    """Renders the registration page for new users."""
    # Redirect if already logged in
    from utils.session import is_logged_in
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
                    <div style="font-size: 1.6rem; font-weight: 800; color: #0F172A;">Create Your Account</div>
                    <div style="font-size: 0.88rem; color: #64748B;">Join Aura Sathi and start scanning smarter</div>
                </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("register_form"):
            st.markdown("#### 📧 Account Details")
            f1, f2 = st.columns(2)
            with f1:
                email = st.text_input("Email", placeholder="e.g. user@aurasathi.ai")
            with f2:
                name = st.text_input("Full Name (Optional)", placeholder="e.g. Alex Mercer")
            
            st.markdown("#### 🔐 Password")
            p1, p2 = st.columns(2)
            with p1:
                password = st.text_input("Password", type="password", placeholder="Min 8 chars, upper, lower, number, symbol")
            with p2:
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
            
            st.markdown("""
            <div style="font-size: 0.75rem; color: #64748B; margin: 12px 0;">
                Password must contain: 8+ characters, uppercase, lowercase, number, and special character
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            submitted = st.form_submit_button("✨ Create Account", type="primary", use_container_width=True)
            
            if submitted:
                errors = []
                if not email or "@" not in email:
                    errors.append("Valid email is required")
                if password != confirm_password:
                    errors.append("Passwords do not match")
                if len(password) < 8:
                    errors.append("Password must be at least 8 characters")
                
                if errors:
                    for error in errors:
                        st.error(f"❌ {error}")
                else:
                    success, msg, user = create_user(email, password, name)
                    if success:
                        login_user(user.id)
                        st.toast(f"✅ {msg}", icon="🎉")
                        navigate_to(PAGE_HOME)
                    else:
                        st.error(f"❌ {msg}")

        st.markdown("<p style='text-align:center; color:#94A3B8; font-size:0.8rem; margin: 16px 0 12px 0;'>ALREADY HAVE AN ACCOUNT?</p>", unsafe_allow_html=True)
        
        if st.button("🔑 Sign In Instead", use_container_width=True):
            navigate_to(PAGE_LOGIN)

        st.markdown("</div>", unsafe_allow_html=True)