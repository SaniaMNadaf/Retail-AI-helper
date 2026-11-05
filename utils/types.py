from typing import TypedDict, List, Optional, Dict, Any
from models.scan_record import ScanRecord
from models.product import ProductAnalysis
from models.user import UserProfile
from datetime import datetime


class NotificationDict(TypedDict):
    id: str
    title: str
    message: str
    type: str  # "warning", "success", "info"
    time: str


DEFAULT_NOTIFICATIONS: List[NotificationDict] = [
    {
        "id": "notif-1",
        "title": "Allergen Warning Detected",
        "message": "Palm Oil & High Sodium detected in recently scanned snack.",
        "type": "warning",
        "time": "15m ago",
    },
    {
        "id": "notif-2",
        "title": "Better Price on Blinkit",
        "message": "Quaker Rolled Oats is ₹20 cheaper on Blinkit compared to retail MRP.",
        "type": "success",
        "time": "1h ago",
    },
    {
        "id": "notif-3",
        "title": "Weekly Shield Score 94%",
        "message": "You made 5 safe food choices this week! Keep it up.",
        "type": "info",
        "time": "1d ago",
    },
]


class SessionStateDict(TypedDict):
    """Type definition for Streamlit session state."""
    # Page routing
    page: str
    
    # User authentication
    user_id: Optional[str]
    user_data: Dict[str, Any]  # UserProfile fields
    
    # Scan history
    scan_history: List[ScanRecord]
    history_user_id: Optional[str]
    last_analysis: Optional[ProductAnalysis]
    
    # Navigation
    active_nav: str
    search_query: str
    
    # Notifications
    notifications: List[NotificationDict]
    show_notifications: bool


# Default values for session state
DEFAULT_SESSION_STATE: Dict[str, Any] = {
    "page": "Home",
    "user_id": None,
    "user_data": {},
    "scan_history": [],
    "history_user_id": None,
    "last_analysis": None,
    "active_nav": "Dashboard",
    "search_query": "",
    "notifications": DEFAULT_NOTIFICATIONS,
    "show_notifications": False,
}

# Navigation constants
class NavItem(str):
    DASHBOARD = "Dashboard"
    SCANNER = "AI Scanner"
    TWIN = "Digital Twin"
    RECORDS = "Scan History"
    SETTINGS = "Settings"


# Page constants
class Page(str):
    LOGO = "Logo"
    LOGIN = "Login"
    REGISTER = "Register"
    CLONING = "Cloning"
    HOME = "Home"


# Type alias for metrics dict
MetricsDict = TypedDict('MetricsDict', {
    'total_scans': int,
    'avg_safety': str,
    'alerts_avoided': int,
    'money_saved': str,
    'buy_count': int,
    'think_count': int,
    'avoid_count': int,
    'safe_percentage': int,
})