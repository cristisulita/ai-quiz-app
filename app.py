import streamlit as st
import json
from ocr_utils import read_image, read_pdf, read_docx, read_txt
from ai_quiz import generate_quiz

st.title("AI Quiz Generator (Cloud Version)")

# --- Session state ---
if "quiz" not in st.session_state:
    st.session_state.quiz = []
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False
if "user_answer" not in st.session_state:
    st.session_state.user_answer = None
if "score" not in st.session_state:
    st.session_state.score = 0
if "raw_json" not in st.session_state:
    st.session_state.raw_json = ""

# --- File upload ---
uploaded_file = st.file_uploader(
    "Upload file",
    type=["pdf", "png", "jpg", "jpeg", "txt", "docx"]
)

num_questions = st.slider("Number of questions", 1, 10, 5)
num_options = st.slider("Options per question", 2, 4, 4)

text = ""
if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type in ["png", "jpg", "jpeg"]:
        text = read_image(uploaded_file)
    elif file_type == "pdf":
        text = read_pdf(uploaded_file)
    elif file_type == "docx":
        text = read_docx(uploaded_file)
    elif file_type == "txt":
        text = read_txt(uploaded_file)

    st.text_area("Extracted Text", text, height=200)

    if st.button("Generate Quiz"):
        with st.spinner("Generating quiz..."):
            quiz = generate_quiz(text, num_questions, num_options)

            if quiz:
                st.session_state.quiz = quiz
                st.session_state.current_q = 0
                st.session_state.score = 0
                st.session_state.show_answer = False
                st.session_state.raw_json = json.dumps(quiz, indent=2)
                st.success("Quiz generated!")
            else:
                st.error("Failed to generate quiz.")

# --- Show JSON ---
if st.session_state.raw_json:
    st.subheader("AI JSON Output")
    st.text_area("Raw JSON", st.session_state.raw_json, height=300)

# --- Interactive quiz ---
if st.session_state.quiz:
    q_index = st.session_state.current_q
    q = st.session_state.quiz[q_index]

    st.subheader(f"Question {q_index + 1}/{len(st.session_state.quiz)}")
    st.write(q["question"])

    # Unique key per question
    selected = st.radio(
        "Choose an answer",
        q["options"],
        key=f"q_{q_index}"
    )

    # CHECK ANSWER
    if not st.session_state.show_answer:
        if st.button("Check Answer"):
            st.session_state.show_answer = True
            st.session_state.user_answer = selected

            if selected == q["answer"]:
                st.session_state.score += 1

            st.rerun()  # force clean update

    # SHOW RESULT
    if st.session_state.show_answer:
        if st.session_state.user_answer == q["answer"]:
            st.success("Correct ✅")
        else:
            st.error(f"Wrong ❌. Correct answer: {q['answer']}")

        # NEXT QUESTION
        if st.button("Next Question"):
            st.session_state.current_q += 1
            st.session_state.show_answer = False
            st.session_state.user_answer = None
            st.rerun()  # force clean transition

    # FINAL SCORE
    if st.session_state.current_q >= len(st.session_state.quiz):
        st.success(f"Final score: {st.session_state.score}/{len(st.session_state.quiz)}")