import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from pydub import AudioSegment
import tempfile

from gemini_helper import configure_gemini

# Setup
st.set_page_config(page_title="🌍 Language Tutor", layout="centered")

# Load Gemini API key
configure_gemini()
st.title("🌍 Language Tutor – AI Translation & Quiz")
model = genai.GenerativeModel("gemini-3.5-flash")

# Function to transcribe audio
def transcribe_audio(file):
    audio = AudioSegment.from_file(file)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        audio.export(tmpfile.name, format="wav")
        recognizer = sr.Recognizer()
        with sr.AudioFile(tmpfile.name) as source:
            audio_data = recognizer.record(source)
            try:
                return recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                return "Could not understand audio"
            except sr.RequestError:
                return "Speech recognition service unavailable"

# Function to get translation
def translate_text(text, target_lang="English"):
    prompt = f"Translate the following into {target_lang}:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text

# Function to generate quiz
def generate_quiz(text):
    prompt = f"""
    Based on this content, generate 3 multiple-choice quiz questions.
    Format: Q + 4 options (A–D) + Answer key.

    Content:
    {text}
    """
    response = model.generate_content(prompt)
    return response.text

# Upload section
file_type = st.radio("Choose input type:", ["Text", "Audio", "Document (RAG)"])

user_input = None

if file_type == "Text":
    user_input = st.text_area("Enter or paste the text you'd like to translate and quiz on:")
elif file_type == "Audio":
    uploaded_file = st.file_uploader("Upload an audio file (mp3, wav, etc.)", type=["mp3", "wav", "m4a"])
    if uploaded_file is not None:
        with st.spinner("Transcribing..."):
            user_input = transcribe_audio(uploaded_file)
            st.success("Transcription completed!")
            st.text_area("Transcribed Text:", value=user_input, height=150)
elif file_type == "Document (RAG)":
    uploaded_file = st.file_uploader("📂 Upload a document (PDF or TXT):", type=["pdf", "txt"])
    if uploaded_file:
        from rag_engine import process_and_cache_document, retrieve_context
        process_and_cache_document(uploaded_file)
        search_query = st.text_input("🎯 Enter a specific section or topic from the document to translate and quiz on:")
        if search_query:
            with st.spinner("Retrieving relevant context from document..."):
                user_input = retrieve_context(search_query, top_k=4)
                st.success("Context retrieved from document!")
                st.text_area("Retrieved Context:", value=user_input, height=150)

# Target language
target_lang = st.selectbox("Select language for translation:", ["English", "Spanish", "French", "German", "Hindi", "Tamil", "Chinese"])

# Process
if user_input and st.button("Generate Translation & Quiz"):
    with st.spinner("Translating..."):
        translation = translate_text(user_input, target_lang)

    with st.spinner("Generating Quiz..."):
        quiz = generate_quiz(user_input)

    st.subheader("✅ Translated Text:")
    st.write(translation)

    st.subheader("🧠 Quiz:")
    st.write(quiz)
