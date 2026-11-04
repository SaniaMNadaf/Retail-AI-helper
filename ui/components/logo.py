import streamlit as st

def render_logo(size: int = 44) -> str:
    """Returns HTML for the official Aura Sathi logo matching the brand identity (Letter A with glowing star on deep navy gradient)."""
    return f"""
    <div style="width: {size}px; height: {size}px; border-radius: 14px; background: linear-gradient(135deg, #0B0F19 0%, #1E1B4B 50%, #312E81 100%); display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 16px rgba(30, 27, 75, 0.4); position: relative; overflow: hidden; border: 1px solid rgba(56, 189, 248, 0.3);">
        <svg width="{size}" height="{size}" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Glow background effect -->
            <circle cx="75" cy="35" r="20" fill="#22D3EE" opacity="0.3" filter="blur(8px)"/>
            <!-- Letter A shape with gradient -->
            <path d="M50 20L25 75H38L45 58H55L62 75H75L50 20Z" fill="url(#paint0_linear)" />
            <path d="M47 48L53 48L50 35L47 48Z" fill="white" opacity="0.9"/>
            <!-- Swoosh arc -->
            <path d="M22 68C32 78 60 75 78 38" stroke="url(#paint1_linear)" stroke-width="6" stroke-linecap="round"/>
            <!-- 4-pointed glowing star -->
            <path d="M78 28C78 38 72 41 72 41C72 41 78 44 78 54C78 44 84 41 84 41C84 41 78 38 78 28Z" fill="#22D3EE"/>
            <circle cx="78" cy="41" r="3" fill="white"/>
            <defs>
                <linearGradient id="paint0_linear" x1="25" y1="20" x2="75" y2="75" gradientUnits="userSpaceOnUse">
                    <stop stop-color="#A78BFA"/>
                    <stop offset="0.5" stop-color="#38BDF8"/>
                    <stop offset="1" stop-color="#06B6D4"/>
                </linearGradient>
                <linearGradient id="paint1_linear" x1="22" y1="68" x2="78" y2="38" gradientUnits="userSpaceOnUse">
                    <stop stop-color="#818CF8" stop-opacity="0.2"/>
                    <stop offset="0.7" stop-color="#38BDF8"/>
                    <stop offset="1" stop-color="#22D3EE"/>
                </linearGradient>
            </defs>
        </svg>
    </div>
    """
