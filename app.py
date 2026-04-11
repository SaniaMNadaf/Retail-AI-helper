import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
import json
import re
from gtts import gTTS
import io
from dotenv import load_dotenv

# 1. INITIAL CONFIGURATION & SAFETY CHECK
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not found. Please check your .env file.")
    st.stop()

genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Aura Sathi", page_icon="🛡️", layout="wide")

# --- GLOBAL STYLING ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        color: white;
    }
    .stTextInput input {
        border-radius: 10px !important;
        padding: 12px !important;
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #334155 !important;
    }
    .stButton button {
        background: linear-gradient(90deg, #3b82f6, #2563eb) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        height: 45px;
        border: none !important;
    }
    .login-sidebar {
        background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        min-height: 350px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    </style>
""", unsafe_allow_html=True)

# --- UTILITY: TEXT TO SPEECH ---
def get_voice_bytes(text):
    try:
        if not text: return None
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp.getvalue()
    except Exception: return None

# State Management
if 'page' not in st.session_state: st.session_state.page = "Logo"
if 'user_data' not in st.session_state: st.session_state.user_data = {}

# --- PAGE 1: LOGO ---
if st.session_state.page == "Logo":
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.image("https://img.icons8.com/fluency/240/shield.png", width=180) 
        st.title("🛡️ Aura Sathi")
        st.subheader("Your AI Shopping Bodyguard")
        if st.button("Get Started →", use_container_width=True):
            st.session_state.page = "Login"
            st.rerun()

# --- PAGE 2: LOGIN ---
elif st.session_state.page == "Login":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, main_col, _ = st.columns([1, 2, 1])
    with main_col:
        col1, col2 = st.columns([1, 1], gap="medium")
        with col1:
            st.markdown("""<div class="login-sidebar"><h2>🛡️ Aura Sathi</h2><h1>Welcome Back</h1><p>Your AI-powered shopping safety assistant.</p></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("### Login")
            l_email = st.text_input("Email / Username", placeholder="e.g. user@aura.com")
            l_pass = st.text_input("Password", type="password")
            if st.button("LOGIN", use_container_width=True):
                st.session_state.user_data['name'] = l_email.split('@')[0] if l_email else "User"
                st.session_state.page = "Cloning"
                st.rerun()
            st.markdown("<p style='text-align:center; opacity:0.5;'>OR</p>", unsafe_allow_html=True)
            if st.button("🌐 Continue with Google", use_container_width=True):
                st.session_state.user_data['name'] = "Google User"
                st.session_state.page = "Cloning"
                st.rerun()

# --- PAGE 3: CLONING ---
elif st.session_state.page == "Cloning":
    st.title("🧬 Create Your Digital Twin")
    with st.form("twin_form"):
        f1, f2 = st.columns(2)
        with f1:
            name = st.text_input("Full Name", value=st.session_state.user_data.get('name', ''))
            age = st.number_input("Age", min_value=1, max_value=100, value=25)
            height = st.text_input("Height", placeholder="e.g. 175cm")
            weight = st.text_input("Weight", placeholder="e.g. 70kg")
        with f2:
            health = st.text_area("Allergies / Health Issues", value="None")
            interests = st.multiselect("Preferences", ["Fitness", "Budget", "Organic", "Tech"])
            photo = st.file_uploader("Profile Photo", type=["jpg", "png"])
        if st.form_submit_button("Generate Digital Twin ✨"):
            st.session_state.user_data.update({"name": name, "age": age, "height": height, "weight": weight, "health": health, "interests": interests})
            st.session_state.page = "Home"
            st.rerun()

# --- PAGE 4: HOME ---
elif st.session_state.page == "Home":
    with st.sidebar:
        st.header(f"👤 {st.session_state.user_data.get('name')}")
        st.info(f"Age: {st.session_state.user_data.get('age')} | Shield Active")
        if st.button("Logout", use_container_width=True): 
            st.session_state.page = "Logo"
            st.rerun()

    st.title("📱 Aura Sathi Dashboard")
    tab1, tab2 = st.tabs(["📸 Camera", "📁 Upload"])
    img_file = None
    with tab1:
        cam = st.camera_input("Scan Label")
        if cam: img_file = cam
    with tab2:
        up = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
        if up: img_file = up

    if st.button("🚀 ANALYZE PRODUCT", use_container_width=True):
        if not img_file:
            st.warning("Please upload or capture an image first.")
        else:
            with st.spinner("Analyzing..."):
                try:
                    img_bytes = img_file.getvalue()
                    model = genai.GenerativeModel("gemini-3-flash-preview")
                    u = st.session_state.user_data
                    
                    prompt = f"""
                    You are a strict JSON API. Analyze the product.
                    User: {u.get('age')}yr, Allergies: {u.get('health')}, Interests: {u.get('interests')}.
                    Return ONLY valid JSON:
                    {{
                      "product_name": "string",
                      "truth_report": "short analysis",
                      "who_verdict": "standards check",
                      "online_prices": [{{"platform": "Amazon", "price": "₹"}}, {{"platform": "Blinkit", "price": "₹"}}],
                      "safety_check": "risk warning",
                      "voice_script": "one sentence verdict",
                      "verdict": "BUY or THINK or AVOID",
                      "safety_score": 8
                    }}
                    """
                    response = model.generate_content([prompt, {"mime_type": img_file.type, "data": img_bytes}])
                    
                    try: raw_text = response.candidates[0].content.parts[0].text
                    except: raw_text = response.text
                    
                    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
                    if not match: raise ValueError("JSON not found")
                    
                    raw_json = match.group().replace(",}", "}").replace(",]", "]")
                    res = json.loads(raw_json)
                    
                    st.divider()
                    
                    # --- DYNAMIC VERDICT DISPLAY ---
                    verdict = res.get('verdict', 'UNKNOWN')
                    prod_name = res.get('product_name', 'Unknown Product')
                    
                    if "BUY" in verdict:
                        st.success(f"✅ {verdict} - {prod_name}")
                    elif "THINK" in verdict:
                        st.warning(f"⚠️ {verdict} - {prod_name}")
                    else:
                        st.error(f"❌ {verdict} - {prod_name}")

                    col_l, col_r = st.columns([2, 1])
                    with col_l:
                        st.info(f"**WHO Insight:** {res.get('who_verdict')}")
                        st.dataframe(pd.DataFrame(res.get("online_prices", [])), use_container_width=True)
                    with col_r:
                        st.metric("Safety Score", f"{res.get('safety_score')}/10")
                        st.warning(res.get("safety_check"))
                        audio = get_voice_bytes(res.get("voice_script", ""))
                        if audio: st.audio(audio, format="audio/mp3", autoplay=True)
                except Exception as e:
                    st.error(f"Error: {str(e)}")