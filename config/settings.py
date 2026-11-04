import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

# App branding and configuration
APP_TITLE = "Aura Sathi"
APP_ICON = "✨"
APP_SUBTITLE = "Your AI Wellness Bodyguard"

# Gemini Model Configuration
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"

# Page Identifiers
PAGE_LOGO = "Logo"
PAGE_LOGIN = "Login"
PAGE_REGISTER = "Register"
PAGE_CLONING = "Cloning"
PAGE_HOME = "Home"

# Preference options for Digital Twin
DEFAULT_PREFERENCES = ["Fitness", "Budget", "Organic", "Tech"]
