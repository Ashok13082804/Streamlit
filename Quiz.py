import streamlit as st
import google.generativeai as genai
from gemini_helper import configure_gemini

# Streamlit page config
st.set_page_config(page_title="🧠 AI Quiz Game with Gemini", layout="centered")

# Configure Gemini API key
configure_gemini()
st.title("🧠 AI Quiz Game with Gemini")
st.write("Generate interactive quizzes using Google Gemini AI based on any topic!")

from rag_engine import process_and_cache_document, retrieve_context

# User input mode selection
quiz_source = st.radio("Select Quiz Source:", ["💡 Generate by Topic", "📄 Generate from Document (RAG)"])

topic = ""
context = ""

if quiz_source == "💡 Generate by Topic":
    topic = st.text_input("📚 Enter a topic for the quiz (e.g., Python, Space, History):")
else:
    uploaded_file = st.file_uploader("📂 Upload a document (PDF or TXT):", type=["pdf", "txt"])
    if uploaded_file:
        process_and_cache_document(uploaded_file)
        topic = st.text_input("🎯 Specific focus/sub-topic inside the document (optional):")

num_questions = st.slider("🔢 Number of questions", 1, 10, 5)

# Generate quiz button
can_generate = (quiz_source == "💡 Generate by Topic" and topic) or (quiz_source == "📄 Generate from Document (RAG)" and "rag_chunks" in st.session_state)

if st.button("🚀 Generate Quiz") and can_generate:
    with st.spinner("Generating quiz using Gemini..."):
        if quiz_source == "📄 Generate from Document (RAG)":
            search_query = topic if topic else "main concepts, definitions, and key topics"
            context = retrieve_context(search_query, top_k=5)
            
            prompt = f"""
            Generate {num_questions} multiple-choice questions based strictly on the provided context below.
            Do not make up facts; use only what is in the context.
            
            Context:
            {context}

            Each question must include:
            - The question starting with 'Q:'
            - Four options labeled A, B, C, D
            - Correct answer labeled as 'Answer: <option letter>'

            Example:
            Q: What is the capital of France?
            A. Berlin
            B. Madrid
            C. Paris
            D. Rome
            Answer: C
            """
        else:
            # Prompt for Gemini
            prompt = f"""
            Generate {num_questions} multiple-choice questions on the topic: {topic}.
            Each question must include:
            - The question starting with 'Q:'
            - Four options labeled A, B, C, D
            - Correct answer labeled as 'Answer: <option letter>'

            Example:
            Q: What is the capital of France?
            A. Berlin
            B. Madrid
            C. Paris
            D. Rome
            Answer: C
            """

        try:
            model = genai.GenerativeModel("gemini-3.5-flash")
            response = model.generate_content(prompt)
            quiz_raw = response.text.strip()
            st.session_state.quiz_text = quiz_raw
            st.session_state.quiz_data = []
            st.session_state.user_answers = []
            st.session_state.correct_answers = []

            questions = quiz_raw.split("Q:")[1:]

            for q in questions:
                q_parts = q.strip().split("Answer:")
                if len(q_parts) != 2:
                    continue
                q_text = q_parts[0].strip()
                answer = q_parts[1].strip()[0]
                lines = q_text.split("\n")
                question = lines[0]
                options = lines[1:5]
                option_dict = {opt[0]: opt[3:].strip() for opt in options}
                st.session_state.quiz_data.append((question, option_dict, answer))
                st.session_state.user_answers.append(None)
                st.session_state.correct_answers.append(answer)

        except Exception as e:
            st.error(f"Error generating quiz: {e}")

# Display quiz questions
if "quiz_data" in st.session_state and st.session_state.quiz_data:
    st.header("📝 Take the Quiz")
    for idx, (question, options, correct) in enumerate(st.session_state.quiz_data):
        st.subheader(f"Q{idx + 1}: {question}")
        selected = st.radio(
            "Select an answer:",
            options.keys(),
            format_func=lambda x: f"{x}. {options[x]}",
            key=f"q_{idx}"
        )
        st.session_state.user_answers[idx] = selected

    # Submit button
    if st.button("✅ Submit Answers"):
        st.header("📊 Results")
        score = 0
        for idx, (user_ans, correct_ans) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers)):
            is_correct = user_ans == correct_ans
            result = "✅ Correct" if is_correct else f"❌ Wrong (Correct: {correct_ans})"
            st.markdown(f"**Q{idx + 1}:** {result}")
            if is_correct:
                score += 1
        st.success(f"🎉 Your score: {score} / {len(st.session_state.correct_answers)}")
