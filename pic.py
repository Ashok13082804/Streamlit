import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import google.generativeai as genai
from gemini_helper import configure_gemini

# Streamlit page config (must be first)
st.set_page_config(page_title="📸 Photo Filters App", layout="centered")

# Configure Gemini AI
configure_gemini()

# ===== Filter Functions =====

def apply_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def apply_sepia(img):
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    sepia = cv2.transform(img, kernel)
    return np.clip(sepia, 0, 255).astype(np.uint8)

def apply_blur(img):
    return cv2.GaussianBlur(img, (15, 15), 0)

def apply_cartoon(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray_blur, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(img, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

# ===== Gemini-based Description (optional) =====

def describe_image_with_gemini(pil_image):
    img_bytes = io.BytesIO()
    pil_image.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    model = genai.GenerativeModel('gemini-3.5-flash')
    response = model.generate_content([
        "Describe this image and suggest a cool photo filter style.",
        img_bytes.read()
    ])
    return response.text.strip()

# ===== Streamlit UI =====

st.title("📸 Photo Filters App with Gemini AI")

# Upload or take a picture
option = st.radio("Choose input source:", ["Upload Image", "Use Webcam"])

if option == "Upload Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
elif option == "Use Webcam":
    captured_image = st.camera_input("Take a picture")
    if captured_image is not None:
        st.image(captured_image)
