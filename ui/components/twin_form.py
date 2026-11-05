import streamlit as st
from config.settings import DEFAULT_PREFERENCES
from utils.session import get_user_data, update_user_data
from models.user import UserProfile
from utils.validation import sanitize_text, validate_file_upload, esc


def render_twin_form(
    form_key: str,
    submit_label: str,
    on_submit_callback=None,
    show_photo: bool = False,
    extended_options: bool = True,
) -> bool:
    """
    Renders the Digital Twin form fields.
    Returns True if form was submitted.
    """
    user = get_user_data()

    with st.form(form_key):
        st.markdown("#### 👤 Personal & Biometric Details")
        f1, f2 = st.columns(2)
        with f1:
            name = st.text_input("Full Name", value=user.get("name", "Alex Mercer"), max_chars=100)
            age = st.number_input("Age", min_value=1, max_value=120, value=int(user.get("age", 28)))
        with f2:
            height = st.text_input("Height", value=user.get("height", "178cm"), placeholder="e.g. 175cm", max_chars=20)
            weight = st.text_input("Weight", value=user.get("weight", "72kg"), placeholder="e.g. 70kg", max_chars=20)

        st.markdown("#### 🚨 Allergies & Restricted Ingredients")
        health = st.text_area(
            "Known Allergies / Medical Issues",
            value=user.get("health", "Lactose sensitivity, Low sodium diet"),
            help="Aura Sathi will issue high-priority warnings whenever an ingredient matches these criteria.",
            max_chars=500,
        )

        st.markdown("#### 🥗 Dietary Preferences & Shopping Goals")
        if extended_options:
            options = list(set(DEFAULT_PREFERENCES + ["Low Sodium", "Gluten-Free", "Vegan", "Low GI", "Keto"]))
        else:
            options = DEFAULT_PREFERENCES + ["Low Sodium", "Gluten-Free", "Vegan"]
        
        current_interests = user.get("interests", ["Fitness", "Organic"])
        interests = st.multiselect(
            "Select Preferences",
            options=options,
            default=[i for i in current_interests if i in options],
        )

        photo = None
        photo_error = None
        if show_photo:
            photo = st.file_uploader("Profile Photo (Optional)", type=["jpg", "png", "jpeg"])
            if photo:
                is_valid, msg = validate_file_upload(photo, ["image/jpeg", "image/png"], max_size_mb=5)
                if not is_valid:
                    photo_error = msg
                    st.error(f"❌ {msg}")

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button(submit_label, type="primary", use_container_width=True)

        if submitted:
            # Validate all fields
            errors = []
            
            # Validate name
            clean_name = sanitize_text(name, max_length=100)
            if not clean_name or len(clean_name) < 2:
                errors.append("Name must be at least 2 characters")
            
            # Validate age
            if not isinstance(age, int) or age < 1 or age > 120:
                errors.append("Age must be between 1 and 120")
            
            # Validate measurements
            for field_name, value in [("Height", height), ("Weight", weight)]:
                clean_value = sanitize_text(value, max_length=20)
                if clean_value and not __import__('re').match(r'^\d+(\.\d+)?(cm|kg|m|ft|in|lbs?)?$', clean_value, __import__('re').IGNORECASE):
                    errors.append(f"{field_name} format invalid. Use e.g. '178cm' or '72kg'")
            
            # Validate health
            clean_health = sanitize_text(health, max_length=500)
            
            # Validate interests
            clean_interests = []
            seen = set()
            for interest in interests:
                if isinstance(interest, str):
                    clean_interest = sanitize_text(interest, max_length=50)
                    if clean_interest and clean_interest not in seen:
                        clean_interests.append(clean_interest)
                        seen.add(clean_interest)
            clean_interests = clean_interests[:20]
            
            # Validate photo
            if photo_error:
                errors.append(photo_error)
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                update_user_data({
                    "name": clean_name,
                    "age": age,
                    "height": sanitize_text(height, max_length=20),
                    "weight": sanitize_text(weight, max_length=20),
                    "health": clean_health,
                    "interests": clean_interests,
                })
                if photo is not None:
                    st.session_state.user_data["has_photo"] = photo is not None
                
                st.toast("✅ Digital Twin updated successfully!", icon="🧬")
                
                if on_submit_callback:
                    on_submit_callback()
                else:
                    st.rerun()
                return True

    return False


def render_twin_preview_card(user: dict) -> None:
    """Renders the preview card showing current digital twin state."""
    active_interests_tags = "".join(
        f'<span style="background: #EEF2FF; color: #4F46E5; font-size: 0.78rem; font-weight: 600; padding: 4px 10px; border-radius: 20px; margin-right: 6px; display: inline-block; margin-bottom: 6px;">#{esc(tag)}</span>'
        for tag in user.get("interests", ["Fitness", "Organic"])
    )

    card_html = (
        f'<div class="twin-preview-card" style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 20px; padding: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">'
        f'<div style="display: flex; align-items: center; gap: 14px; margin-bottom: 18px;">'
        f'<div style="width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, #4F46E5, #06B6D4); display: flex; align-items: center; justify-content: center; font-size: 1.6rem; color: white; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);">🧬</div>'
        f'<div>'
        f'<div class="twin-title" style="font-size: 1.2rem; font-weight: 800; color: #0F172A;">{esc(user.get("name", "Aarav Sharma"))}</div>'
        f'<div style="font-size: 0.82rem; color: #10B981; font-weight: 600;">● Active Aura Protection</div>'
        f'</div>'
        f'</div>'
        f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">'
        f'<div class="twin-box" style="background: #F8FAFC; padding: 10px 14px; border-radius: 10px; border: 1px solid #E2E8F0;">'
        f'<div style="font-size: 0.72rem; color: #64748B; font-weight: 600;">AGE</div>'
        f'<div class="twin-val" style="font-size: 1.1rem; font-weight: 800; color: #0F172A;">{user.get("age", 28)} yrs</div>'
        f'</div>'
        f'<div class="twin-box" style="background: #F8FAFC; padding: 10px 14px; border-radius: 10px; border: 1px solid #E2E8F0;">'
        f'<div style="font-size: 0.72rem; color: #64748B; font-weight: 600;">BIOMETRICS</div>'
        f'<div class="twin-val" style="font-size: 1.1rem; font-weight: 800; color: #0F172A;">{esc(user.get("height", "178cm"))} / {esc(user.get("weight", "72kg"))}</div>'
        f'</div>'
        f'</div>'
        f'<div style="margin-bottom: 14px;">'
        f'<div style="font-size: 0.8rem; font-weight: 700; color: #92400E; margin-bottom: 4px;">⚠️ Active Allergen Interceptors</div>'
        f'<div class="twin-alert" style="font-size: 0.85rem; color: #78350F; background: #FFFBEB; border: 1px solid #FDE68A; padding: 8px 12px; border-radius: 8px;">{esc(user.get("health", "None"))}</div>'
        f'</div>'
        f'<div>'
        f'<div style="font-size: 0.8rem; font-weight: 700; color: #475569; margin-bottom: 6px;">Shopping Philosophy</div>'
        f'<div>{active_interests_tags or "<span style=\'color:#94A3B8; font-size:0.8rem;\'>None specified</span>"}</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)