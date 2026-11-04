import io
import logging
from typing import Optional
from gtts import gTTS
import streamlit as st

logger = logging.getLogger("aura_sathi.audio")

def generate_voice_bytes(text: str) -> Optional[bytes]:
    """
    Generate MP3 voice bytes from text using Google Text-to-Speech (gTTS).
    """
    if not text or not text.strip():
        return None
    try:
        tts = gTTS(text=text.strip(), lang="en")
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp.getvalue()
    except Exception as e:
        logger.warning(f"gTTS generation failed: {e}")
        return None
