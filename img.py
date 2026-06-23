import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import google.generativeai as genai
from gemini_helper import configure_gemini

# Streamlit UI page config must be set first
st.set_page_config(page_title="🖼️ Meme Generator", layout="centered")

# Configure Gemini AI key
configure_gemini()

# Function to generate meme text using Gemini
def generate_meme_text(prompt):
    model = genai.GenerativeModel('gemini-3.5-flash')
    response = model.generate_content(f"Generate a funny meme caption for this: {prompt}")
    return response.text.strip()

# Function to draw text on image
def create_meme(image, top_text, bottom_text):
    image = image.convert('RGB')
    draw = ImageDraw.Draw(image)
    width, height = image.size

    # Load font
    try:
        font = ImageFont.truetype("impact.ttf", size=int(height/12))
    except:
        font = ImageFont.load_default()

    # Stroke for text
    stroke_width = 2

    # Function to center text
    def draw_centered_text(text, y):
        text = text.upper()
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) / 2
        draw.text((x, y), text, fill="white", stroke_fill="black", stroke_width=stroke_width, font=font)

    # Draw top and bottom texts
    if top_text:
        draw_centered_text(top_text, 10)
    if bottom_text:
        draw_centered_text(bottom_text, height - int(height / 10))

    return image

# Streamlit UI
st.title("😂 Meme Generator with Gemini AI")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    st.subheader("Add Your Text or Let AI Help")

    prompt = st.text_input("Optional: Describe the image for AI to generate captions")
    if prompt:
        if st.button("Generate Funny Caption with Gemini"):
            ai_text = generate_meme_text(prompt)
            st.success("Generated Meme Caption:")
            st.write(ai_text)
    else:
        ai_text = ""

    top_text = st.text_input("Top Text", value=ai_text if ai_text else "")
    bottom_text = st.text_input("Bottom Text")

    if st.button("Create Meme"):
        meme = create_meme(image, top_text, bottom_text)
        st.image(meme, caption="Generated Meme", use_column_width=True)

        # Download button
        buf = io.BytesIO()
        meme.save(buf, format="PNG")
        st.download_button("📥 Download Meme", buf.getvalue(), file_name="meme.png", mime="image/png")
