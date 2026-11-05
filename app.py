import streamlit as st
from config.settings import (
    APP_TITLE,
    APP_ICON,
    PAGE_LOGO,
    PAGE_LOGIN,
    PAGE_REGISTER,
    PAGE_CLONING,
    PAGE_HOME,
)
from config.validation import check_required_config, get_validated_page, PageRoute
from ui.styles import apply_custom_styles
from utils.session import init_session_state
from utils.logging_config import setup_logging
from ui.pages import (
    render_landing_page,
    render_login_page,
    render_register_page,
    render_cloning_page,
    render_dashboard_page,
)

# Initialize logging first
setup_logging()

# 1. Validate configuration at startup
try:
    check_required_config()
except Exception as e:
    st.error(f"❌ Configuration Error: {str(e)}")
    st.stop()

# 3. Initialize Session State
init_session_state()

# 4. Load user theme setting and inject CSS theme
from services.database_service import get_user_settings
user_id = st.session_state.get("user_id")
is_dark = False
if user_id:
    user_settings = get_user_settings(user_id)
    is_dark = (getattr(user_settings, "theme", "Light Mode") == "Dark Mode")
apply_custom_styles(is_dark=is_dark)

# 5. Declarative Page Routing with Enum validation
PAGE_ROUTES: dict[PageRoute, callable] = {
    PageRoute.LOGO: render_landing_page,
    PageRoute.LOGIN: render_login_page,
    PageRoute.REGISTER: render_register_page,
    PageRoute.CLONING: render_cloning_page,
    PageRoute.HOME: render_dashboard_page,
}

current_page_str = st.session_state.get("page", PageRoute.LOGO.value)
current_page = get_validated_page(current_page_str)
page_renderer = PAGE_ROUTES.get(current_page, render_landing_page)
page_renderer()