import os
import streamlit as st
import google.generativeai as genai

def configure_gemini():
    """
    Configures the Gemini API Key.
    Checks environment variables first, then falls back to secrets.toml.
    """
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            pass

    if not api_key:
        # Default fallback key
        api_key = os.getenv("GEMINI_API_KEY")

    genai.configure(api_key=api_key)
