import streamlit as st

MODERN_SAAS_CSS = """
<style>
/* --- GOOGLE FONTS IMPORT (Inter & Plus Jakarta Sans) --- */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #F8FAFC !important;
    color: #0F172A !important;
}

/* Ensure proper clearance so Streamlit header does not cover the custom top navbar */
header[data-testid="stHeader"] {
    background-color: transparent !important;
    z-index: 10 !important;
    height: 3.5rem !important;
}

.block-container {
    padding-top: 4.75rem !important;
    padding-bottom: 3rem !important;
    max-width: 1400px !important;
}

/* --- SIDEBAR STYLING --- */
[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #E2E8F0 !important;
    box-shadow: 2px 0 12px rgba(15, 23, 42, 0.02) !important;
}

[data-testid="stSidebar"] .block-container {
    padding-top: 4.75rem !important;
}

/* --- TOP NAVBAR WRAPPER & SEARCH BAR --- */
div[data-testid="stTextInput"] input {
    height: 42px !important;
    border-radius: 10px !important;
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    font-size: 0.9rem !important;
    padding: 0 14px !important;
    color: #0F172A !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #4F46E5 !important;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15) !important;
}

/* --- MODERN CARD SYSTEM --- */
.saas-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03), 0 6px 16px -2px rgba(15, 23, 42, 0.03);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    margin-bottom: 16px;
}

.saas-card:hover {
    box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.06);
    border-color: #CBD5E1;
}

/* --- STAT CARDS --- */
.stat-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03), 0 4px 12px rgba(15, 23, 42, 0.02);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    transition: all 0.2s ease;
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px -4px rgba(79, 70, 229, 0.08);
    border-color: #C7D2FE;
}

.stat-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}

.stat-card-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.stat-card-icon {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
}

.stat-card-value {
    font-size: 1.85rem;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.2;
    margin-bottom: 8px;
}

.stat-card-footer {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.82rem;
    font-weight: 500;
}

.stat-badge-positive {
    background-color: #ECFDF5;
    color: #059669;
    padding: 2px 8px;
    border-radius: 6px;
    font-weight: 600;
}

.stat-badge-neutral {
    background-color: #F1F5F9;
    color: #475569;
    padding: 2px 8px;
    border-radius: 6px;
    font-weight: 600;
}

/* --- BADGES --- */
.badge-buy {
    background-color: #ECFDF5;
    color: #059669;
    border: 1px solid #A7F3D0;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.badge-think {
    background-color: #FFFBEB;
    color: #D97706;
    border: 1px solid #FDE68A;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.badge-avoid {
    background-color: #FEF2F2;
    color: #DC2626;
    border: 1px solid #FECACA;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

/* --- WELCOME BANNER --- */
.welcome-banner {
    background: linear-gradient(135deg, #4F46E5 0%, #3730A3 100%);
    border-radius: 20px;
    padding: 28px 32px;
    color: #FFFFFF;
    margin-bottom: 24px;
    box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.25);
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    overflow: hidden;
}

.welcome-banner::after {
    content: '';
    position: absolute;
    right: -20px;
    bottom: -40px;
    width: 220px;
    height: 220px;
    background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0) 70%);
    border-radius: 50%;
    pointer-events: none;
}

/* --- STREAMLIT BUTTON OVERRIDES --- */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    padding: 8px 18px !important;
    height: 42px !important;
    border: 1px solid #E2E8F0 !important;
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
}

.stButton > button:hover {
    border-color: #CBD5E1 !important;
    background-color: #F8FAFC !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.07) !important;
}

/* Popover button height alignment */
button[data-testid="stBaseButton-secondary"] {
    height: 42px !important;
}

/* Primary buttons */
.stButton > button[kind="primary"],
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3) !important;
}

.stButton > button[kind="primary"]:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    background: linear-gradient(135deg, #4338CA 0%, #3730A3 100%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4) !important;
}

/* Dataframe styling */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid #E2E8F0 !important;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background-color: #4F46E5 !important;
    border-radius: 8px !important;
}

/* Alert Box Styling */
.stAlert {
    border-radius: 12px !important;
    border-width: 1px !important;
}

/* Safety Alert Banner Light Mode */
.safety-alert-banner {
    background: #FFFBEB !important;
    border: 1px solid #FDE68A !important;
    border-left: 5px solid #F59E0B !important;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #92400E !important;
}
.safety-alert-banner .safety-alert-title {
    font-weight: 700;
    font-size: 0.92rem;
    color: #92400E !important;
}
.safety-alert-banner .safety-alert-text {
    font-size: 0.82rem;
    color: #B45309 !important;
    margin-top: 2px;
}
.safety-alert-banner .safety-alert-text span {
    color: #451A03 !important;
    font-weight: bold;
}
.safety-alert-banner .safety-alert-badge {
    background: #FEF3C7 !important;
    color: #92400E !important;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 6px;
    border: 1px solid #FCD34D !important;
}
</style>
"""

DARK_SAAS_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #0F172A !important;
    color: #F8FAFC !important;
}

header[data-testid="stHeader"] {
    background-color: transparent !important;
    z-index: 10 !important;
    height: 3.5rem !important;
}

.block-container {
    padding-top: 4.75rem !important;
    padding-bottom: 3rem !important;
    max-width: 1400px !important;
}

[data-testid="stSidebar"] {
    background-color: #1E293B !important;
    border-right: 1px solid #334155 !important;
}

[data-testid="stSidebar"] div, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p {
    color: #F8FAFC !important;
}

[data-testid="stSidebar"] button {
    background-color: #334155 !important;
    color: #F8FAFC !important;
    border: 1px solid #475569 !important;
}

[data-testid="stSidebar"] button p {
    color: #F8FAFC !important;
}

[data-testid="stSidebar"] button[kind="primary"] {
    background: linear-gradient(135deg, #4F46E5, #3730A3) !important;
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] button[kind="primary"] p {
    color: #FFFFFF !important;
}

.sidebar-widget {
    background: #334155 !important;
    border: 1px solid #475569 !important;
    color: #F8FAFC !important;
}

.sidebar-widget span, .sidebar-widget strong {
    color: #F8FAFC !important;
}

div[data-testid="stTextInput"] input {
    height: 42px !important;
    border-radius: 10px !important;
    background-color: #1E293B !important;
    border: 1px solid #475569 !important;
    color: #F8FAFC !important;
}

.saas-card, .stat-card {
    background: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 16px;
    padding: 22px;
    color: #F8FAFC !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

.saas-card *, .stat-card * {
    color: #F8FAFC !important;
}

.saas-card div[style*="color: #64748B"], .saas-card div[style*="color: #475569"], .saas-card div[style*="color: #334155"], .saas-card span[style*="color: #64748B"] {
    color: #94A3B8 !important;
}

.stat-card-icon {
    width: 40px !important;
    height: 40px !important;
    border-radius: 12px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 1.25rem !important;
    background: #334155 !important;
    color: #38BDF8 !important;
    flex-shrink: 0 !important;
}

.stat-card-footer span {
    color: #94A3B8 !important;
}

.stat-badge-positive {
    background: rgba(16, 185, 129, 0.2) !important;
    color: #34D399 !important;
}

.stat-badge-neutral {
    background: rgba(59, 130, 246, 0.2) !important;
    color: #60A5FA !important;
}

.welcome-banner {
    background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%) !important;
    color: #FFFFFF !important;
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 24px;
}

/* --- STREAMLIT WIDGETS DARK MODE OVERRIDES --- */
div[data-baseweb="select"] > div, div[data-baseweb="base-input"] > input, div[data-baseweb="input"], textarea {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    border-color: #475569 !important;
}

[data-baseweb="tag"] {
    background-color: #334155 !important;
    color: #38BDF8 !important;
}

[data-baseweb="tag"] span {
    color: #38BDF8 !important;
}

[data-testid="stPopover"] button {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    border: 1px solid #475569 !important;
}

.stButton > button {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    border: 1px solid #475569 !important;
}

.stButton > button p, .stButton > button span {
    color: #F8FAFC !important;
}

.stButton > button[kind="primary"], div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
}

.stButton > button[kind="primary"] p, div[data-testid="stFormSubmitButton"] > button p {
    color: #FFFFFF !important;
}

/* Tabs */
[data-testid="stTabs"] button {
    color: #94A3B8 !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #38BDF8 !important;
    border-bottom-color: #38BDF8 !important;
}

.stMarkdown :not(.safety-alert-banner) p, .stMarkdown :not(.safety-alert-banner) span, .stMarkdown :not(.safety-alert-banner) label, .stMarkdown :not(.safety-alert-banner) div {
    color: #F8FAFC !important;
}

div[data-testid="stTextInput"] input {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    border: 1px solid #475569 !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #94A3B8 !important;
}

input, textarea, select {
    color: #F8FAFC !important;
}

/* Twin Preview Card Dark Mode */
.twin-preview-card {
    background: #1E293B !important;
    border: 1px solid #334155 !important;
    color: #F8FAFC !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4) !important;
}
.twin-preview-card .twin-title, .twin-preview-card .twin-val {
    color: #F8FAFC !important;
}
.twin-preview-card .twin-box {
    background: #334155 !important;
    border: 1px solid #475569 !important;
    color: #F8FAFC !important;
}
.twin-preview-card .twin-alert {
    background: rgba(245, 158, 11, 0.15) !important;
    border: 1px solid rgba(245, 158, 11, 0.4) !important;
    color: #FBBF24 !important;
}

/* Safety Alert Banner Clean White Box with Blue Text */
.safety-alert-banner {
    background: #FFFFFF !important;
    border: 1px solid #BFDBFE !important;
    border-left: 5px solid #2563EB !important;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #1E40AF !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3) !important;
}
.safety-alert-banner *, .safety-alert-banner div, .safety-alert-banner span, .safety-alert-banner strong {
    color: #1E40AF !important;
}
.safety-alert-banner .safety-alert-badge {
    background: #DBEAFE !important;
    color: #1D4ED8 !important;
    border: 1px solid #93C5FD !important;
}
</style>
"""

def apply_custom_styles(is_dark: bool = False) -> None:
    """Injects the modern SaaS theme CSS into the Streamlit application (Light or Dark)."""
    if is_dark:
        st.markdown(DARK_SAAS_CSS, unsafe_allow_html=True)
    else:
        st.markdown(MODERN_SAAS_CSS, unsafe_allow_html=True)
