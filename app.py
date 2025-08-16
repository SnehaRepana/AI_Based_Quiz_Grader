import streamlit as st
from huggingface_hub import InferenceClient
import re

# --- Configuration ---
HF_TOKEN = "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"  # Replace with your actual Hugging Face token
MODEL = "mistralai/Mistral-7B-Instruct-v0.1"

# Setup InferenceClient (no deprecation warning)
client = InferenceClient(model=MODEL, token=HF_TOKEN)

# --- Streamlit UI Setup ---
st.set_page_config(page_title="AI Quiz Grader", layout="wide")
st.title("🧠 AI Quiz Grader")
st.markdown("Generate MCQs using Hugging Face's Mistral-7B model and evaluate answers.")

# --- Initialize session state ---
if "questions" not in st.session_state:
    st.session_state.questions = None
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "show_score" not in st.session_state:
    st.session_state.show_score = False
if "score" not in st.session_state:
    st.session_state.score = 0

# --- Function to generate MCQs ---
def generate_mcqs(topic):
    prompt = f"""
Generate 5 multiple choice questions on the topic '{topic}'.
Each question must have 5 options (A to E) and indicate the correct answer.
Format:

Q1. What is the question?
A. Option A
B. Option B
C. Option C
D. Option D
E. Option E
Answer: C

Return only the questions, options, and answers in the above format.
"""
    try:
        output = client.text_generation(prompt=prompt, max_new_tokens=1024, temperature=0.7)
        return output
    except Exception as e:
        return f"❌ Error generating questions: {str(e)}"

# --- Function to parse the generated output ---
def parse_questions(text):
    questions = []
    parts = re.split(r"Q\d+\.", text)
    for part in parts:
        if not part.strip():
            continue
        try:
            lines = part.strip().split("\n")
            question = lines[0].strip()
            options = {}
            for line in lines[1:6]:
                if len(line) >= 3 and line[1] == '.':
                    options[line[0]] = line[3:].strip()
            answer_line = next((l for l in lines if l.strip().startswith("Answer:")), "")
            answer = answer_line.split(":")[-1].strip()
            if question and len(options) == 5 and answer:
                questions.append({
                    "question": question,
                    "options": options,
                    "answer": answer
                })
        except Exception:
            continue
    return questions

# --- Function to calculate score ---
def submit_quiz():
    score = 0
    for i, q_data in enumerate(st.session_state.questions):
        user_answer = st.session_state.answers.get(i)
        if user_answer == q_data["answer"]:
            score += 1
    st.session_state.score = score
    st.session_state.show_score = True

# --- Main UI ---
topic = st.text_input("Enter a topic (e.g., Python, History, Biology)")

if st.button("Generate Quiz") and topic:
    st.session_state.questions = None
    st.session_state.answers = {}
    st.session_state.show_score = False
    with st.spinner("Generating quiz..."):
        raw_text = generate_mcqs(topic)
        if raw_text.startswith("❌"):
            st.error(raw_text)
        else:
            parsed_questions = parse_questions(raw_text)
            if not parsed_questions:
                st.warning("⚠️ No valid questions found. Try again with a different topic.")
            else:
                st.session_state.questions = parsed_questions
                st.success(f"✅ Generated {len(parsed_questions)} questions!")

# --- Quiz Display ---
if st.session_state.questions:
    st.subheader("Quiz")

    for i, q_data in enumerate(st.session_state.questions):
        st.markdown(f"**Q{i+1}. {q_data['question']}**")
        selected = st.radio(
            "Choose your answer:",
            options=list(q_data['options'].keys()),
            key=f"q_{i}",
            index=None
        )
        st.session_state.answers[i] = selected
        st.markdown("---")

    if st.button("Submit Quiz"):
        submit_quiz()
        st.success("✅ Quiz submitted!")

# --- Result Display ---
if st.session_state.show_score:
    st.subheader("Your Results")
    st.info(f"🎯 Your Score: **{st.session_state.score} / {len(st.session_state.questions)}**")

    if st.button("Show Correct Answers"):
        for i, q_data in enumerate(st.session_state.questions):
            st.markdown(f"**Q{i+1}. {q_data['question']}**")
            for key, val in q_data["options"].items():
                if key == q_data["answer"]:
                    st.success(f"✅ {key}. {val}")
                else:
                    st.markdown(f"{key}. {val}")
            st.markdown("---")
