from typing import Any, Dict, List, Optional
import streamlit as st
from config.settings import PAGE_LOGO, PAGE_HOME
from services.history_service import get_initial_records
from services.database_service import (
    get_user_profile,
    get_scan_history,
    update_user_profile,
    init_db,
    get_user_by_id,
)
from models.user import UserProfile
from utils.types import (
    DEFAULT_SESSION_STATE,
    DEFAULT_NOTIFICATIONS,
    NavItem,
    Page,
    SessionStateDict,
)

# Navigation constants - kept for backward compatibility
NAV_DASHBOARD = NavItem.DASHBOARD
NAV_SCANNER = NavItem.SCANNER
NAV_TWIN = NavItem.TWIN
NAV_RECORDS = NavItem.RECORDS
NAV_SETTINGS = NavItem.SETTINGS


def init_session_state() -> None:
    """Initializes default session state variables for modern SaaS dashboard."""
    # Initialize database
    init_db()
    
    # Initialize session state with defaults
    for key, default_value in DEFAULT_SESSION_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
            
    # Ensure scan_history is populated with initial records if empty
    if not st.session_state.get("scan_history"):
        st.session_state.scan_history = get_initial_records()


def load_user_session(user_id: str) -> None:
    """Load user data and scan history into session state."""
    profile = get_user_profile(user_id)
    st.session_state.user_data = profile.model_dump()
    st.session_state.user_id = user_id
    
    db_records = get_scan_history(user_id, limit=50)
    if not db_records:
        st.session_state.scan_history = get_initial_records()
    else:
        st.session_state.scan_history = db_records


def set_active_nav(nav_item: str) -> None:
    """Switches active navigation tab and triggers rerun."""
    st.session_state.active_nav = nav_item
    st.session_state.page = PAGE_HOME
    st.rerun()


def navigate_to(page: str) -> None:
    """Safely transitions between pages and triggers a rerun."""
    st.session_state.page = page
    st.rerun()


def get_user_data() -> Dict[str, Any]:
    """Returns the current user profile dictionary."""
    return st.session_state.get("user_data", {})


def get_user_id() -> Optional[str]:
    """Returns the current user ID."""
    return st.session_state.get("user_id")


def get_current_user_id() -> Optional[str]:
    """Alias used by settings and history code."""
    return st.session_state.get("user_id")


def update_user_data(new_data: Dict[str, Any]) -> None:
    """Updates user profile data in session state and database."""
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}
    st.session_state.user_data.update(new_data)
    
    # Persist to database
    user_id = st.session_state.get("user_id")
    profile = UserProfile(**st.session_state.user_data)
    update_user_profile(profile, user_id)


def login_user(user_id: str) -> None:
    """Set up session after successful login."""
    load_user_session(user_id)
    st.session_state.page = PAGE_HOME
    st.session_state.active_nav = NAV_DASHBOARD


def logout() -> None:
    """Clears user session state and returns to landing page."""
    # Reset all user-related session state
    for key in ["user_id", "user_data", "last_analysis", "scan_history"]:
        if key in st.session_state:
            del st.session_state[key]
    
    # Reset to defaults
    st.session_state.active_nav = NAV_DASHBOARD
    navigate_to(Page.LOGO)


def is_logged_in() -> bool:
    """Check if user is logged in."""
    return st.session_state.get("user_id") is not None
