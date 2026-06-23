# app.py
import streamlit as st
import google.generativeai as genai
from gemini_helper import configure_gemini

# Configure Streamlit page
st.set_page_config(page_title="🧮 Math Solver", layout="centered")

# Load Gemini API Key
configure_gemini()

st.title("🧮 Math Problem Solver using Gemini AI")

# Create the Gemini model
model = genai.GenerativeModel("gemini-3.5-flash")

# Input from user
solve_source = st.radio("Select Problem Solving Mode:", ["💡 Standard Solver", "📖 Use Reference Notes/Textbook (RAG)"])

problem = ""
if solve_source == "💡 Standard Solver":
    problem = st.text_input("Enter a math equation or word problem (e.g., x^2 - 4 = 0):")
else:
    uploaded_file = st.file_uploader("📂 Upload reference textbook/notes (PDF or TXT):", type=["pdf", "txt"])
    if uploaded_file:
        from rag_engine import process_and_cache_document, retrieve_context
        process_and_cache_document(uploaded_file)
        problem = st.text_input("Enter the math equation or problem to solve using context:")

can_solve = (solve_source == "💡 Standard Solver" and problem.strip() != "") or (solve_source == "📖 Use Reference Notes/Textbook (RAG)" and "rag_chunks" in st.session_state and problem.strip() != "")

if st.button("Solve"):
    if not can_solve:
        st.warning("Please enter a valid problem (and ensure a reference document is uploaded if in RAG mode).")
    else:
        with st.spinner("Solving with Gemini AI..."):
            if solve_source == "📖 Use Reference Notes/Textbook (RAG)":
                from rag_engine import retrieve_context
                context = retrieve_context(problem, top_k=4)
                prompt = f"""
You are a math teacher. Solve the following math problem step by step in detail, utilizing the reference context provided below.
If the reference text contains specific formulas, theorems, or step-by-step methods matching the problem, prioritize using them.

Reference Context:
{context}

Problem: {problem}

Make sure your explanation is clear, each step is explained properly, and references the formulas/concepts from the context when applicable.
"""
            else:
                prompt = f"""
You are a math teacher. Solve the following math problem step by step in detail.

Problem: {problem}

Make sure your explanation is clear and each step is explained properly.
"""
            try:
                response = model.generate_content(prompt)
                st.subheader("📘 Step-by-Step Solution:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {str(e)}")
