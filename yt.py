import streamlit as st
import google.generativeai as genai
import re
from gemini_helper import configure_gemini

# Configure page
st.set_page_config(page_title="📊 YouTube Analytics App", layout="centered")

# Configure Gemini API Key
configure_gemini()

st.title("📊 YouTube Channel Insights with Gemini AI")
model = genai.GenerativeModel("gemini-3.5-flash")

# Helper to extract channel name/ID
def extract_channel_name(url):
    pattern = r"(?:https?://)?(?:www\.)?youtube\.com/(?:c/|channel/|@)?([\w\-]+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

# Input URL
channel_url = st.text_input("Enter a YouTube channel URL (e.g., https://youtube.com/@veritasium):")

if st.button("Analyze"):
    if not channel_url:
        st.warning("Please enter a valid YouTube channel URL.")
    else:
        channel_id_or_name = extract_channel_name(channel_url)
        if not channel_id_or_name:
            st.error("Could not extract channel name. Please check the URL.")
        else:
            with st.spinner("Generating insights using Gemini AI..."):
                prompt = f"""
You are a YouTube analyst AI.

Based on the YouTube channel `{channel_id_or_name}`, give intelligent assumptions and creative insights such as:

- Likely content focus
- Possible audience demographics
- Suggestions for better reach or engagement
- Posting frequency assumptions
- Style or tone of content (if known)

Be clear, insightful, and structured. If you don't have exact data, use general inference based on similar YouTube channels.
"""
                try:
                    response = model.generate_content(prompt)
                    st.subheader("📈 Gemini's Channel Insights")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Gemini API Error: {str(e)}")
