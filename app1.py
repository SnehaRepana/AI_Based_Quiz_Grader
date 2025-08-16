import streamlit as st
import time

QUIZZES = {
    "Python": [
        {"question": "What is the output of: print(type([]))?",
         "options": ["<class 'list'>", "<class 'dict'>", "<class 'tuple'>", "<class 'set'>"],
         "answer": "<class 'list'>"},
        {"question": "Which keyword is used to define a function in Python?",
         "options": ["function", "def", "define", "fun"],
         "answer": "def"},
        {"question": "What is the output of 3 * '7'?",
         "options": ["21", "777", "'777'", "Error"],
         "answer": "777"},
        {"question": "What does the 'len' function do?",
         "options": ["Returns the length", "Calculates memory", "Counts numbers", "Lists files"],
         "answer": "Returns the length"},
        {"question": "Which data type is immutable?",
         "options": ["list", "dict", "set", "tuple"],
         "answer": "tuple"},
        {"question": "What is a correct syntax to import a module?",
         "options": ["import math", "load math", "require math", "include math"],
         "answer": "import math"},
        {"question": "What is the result of 4 // 2?",
         "options": ["2", "2.0", "2.5", "Error"],
         "answer": "2"},
        {"question": "Which one is a Python boolean value?",
         "options": ["true", "True", "TRUE", "truth"],
         "answer": "True"},
        {"question": "What is used to handle exceptions?",
         "options": ["try/except", "if/else", "for/while", "import/error"],
         "answer": "try/except"},
        {"question": "Which of the following is used to define a block of code in Python?",
         "options": ["{}", "begin/end", "indentation", "[]"],
         "answer": "indentation"},
    ],
    "Machine Learning": [
        {"question": "Which of these is a supervised learning algorithm?",
         "options": ["K-Means", "Linear Regression", "DBSCAN", "Apriori"],
         "answer": "Linear Regression"},
        {"question": "What is overfitting?",
         "options": ["Good performance on all data", "Poor performance on test data", "Data leakage", "Clean data"],
         "answer": "Poor performance on test data"},
        {"question": "Which metric is used for classification?",
         "options": ["MSE", "Accuracy", "R²", "RMSE"],
         "answer": "Accuracy"},
        {"question": "Which ML algorithm is used for clustering?",
         "options": ["KNN", "K-Means", "SVM", "Linear Regression"],
         "answer": "K-Means"},
        {"question": "Which library is used for ML in Python?",
         "options": ["NumPy", "TensorFlow", "Flask", "Django"],
         "answer": "TensorFlow"},
        {"question": "What is the purpose of a train-test split?",
         "options": ["To save memory", "To tune hyperparameters", "To evaluate model generalization", "To shuffle data"],
         "answer": "To evaluate model generalization"},
        {"question": "What is a feature in ML?",
         "options": ["Model output", "Model name", "Input variable", "Training data"],
         "answer": "Input variable"},
        {"question": "Which technique helps prevent overfitting?",
         "options": ["Regularization", "Batching", "Normalization", "Concatenation"],
         "answer": "Regularization"},
        {"question": "What is gradient descent used for?",
         "options": ["Prediction", "Error measurement", "Optimization", "Data normalization"],
         "answer": "Optimization"},
        {"question": "What type of ML is used in recommender systems?",
         "options": ["Unsupervised", "Supervised", "Reinforcement", "Collaborative"],
         "answer": "Collaborative"},
    ],
    "Java": [
        {"question": "Which of these is not a Java primitive type?",
         "options": ["int", "float", "String", "char"],
         "answer": "String"},
        {"question": "What does JVM stand for?",
         "options": ["Java Variable Machine", "Java Virtual Machine", "Java Verified Machine", "Joint Virtual Module"],
         "answer": "Java Virtual Machine"},
        {"question": "Which keyword is used to inherit a class?",
         "options": ["implements", "inherits", "extends", "instanceof"],
         "answer": "extends"},
        {"question": "Which method is the entry point for a Java program?",
         "options": ["start()", "init()", "main()", "run()"],
         "answer": "main()"},
        {"question": "Which of the following is not an access modifier?",
         "options": ["private", "public", "protected", "static"],
         "answer": "static"},
        {"question": "What is the default value of a boolean in Java?",
         "options": ["true", "false", "0", "null"],
         "answer": "false"},
        {"question": "Which loop is used when the number of iterations is known?",
         "options": ["while", "do-while", "for", "switch"],
         "answer": "for"},
        {"question": "What is used to handle exceptions?",
         "options": ["try-catch", "throw-catch", "assert", "scan"],
         "answer": "try-catch"},
        {"question": "Which of the following is used to create objects?",
         "options": ["new", "class", "static", "void"],
         "answer": "new"},
        {"question": "What is method overloading?",
         "options": ["Same method name, different parameters", "Different names", "Multiple classes", "Abstract method"],
         "answer": "Same method name, different parameters"},
    ]
}

TIMER_SECONDS = 30

def main():
    st.title("📝 AI Based Quiz Grader")

    subject = st.sidebar.selectbox("Choose Subject", list(QUIZZES.keys()))

    # Initialize session state variables
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "answers" not in st.session_state or len(st.session_state.answers) != len(QUIZZES[subject]):
        st.session_state.answers = [None] * len(QUIZZES[subject])
    if "timer" not in st.session_state:
        st.session_state.timer = TIMER_SECONDS
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "last_time" not in st.session_state:
        st.session_state.last_time = time.time()

    questions = QUIZZES[subject]
    total_questions = len(questions)

    def next_question():
        if st.session_state.current_question < total_questions - 1:
            st.session_state.current_question += 1
            st.session_state.timer = TIMER_SECONDS
            st.session_state.last_time = time.time()
        else:
            st.session_state.quiz_submitted = True

    def prev_question():
        if st.session_state.current_question > 0:
            st.session_state.current_question -= 1
            st.session_state.timer = TIMER_SECONDS
            st.session_state.last_time = time.time()

    # Display question number and timer
    st.write(f"### Question {st.session_state.current_question + 1} of {total_questions}")

    timer_placeholder = st.empty()
    question = questions[st.session_state.current_question]

    # Add dummy option to simulate no selection
    options = ["-- Select an answer --"] + question["options"]
    current_answer = st.session_state.answers[st.session_state.current_question]
    if current_answer is None:
        current_answer_index = 0
    else:
        try:
            current_answer_index = question["options"].index(current_answer) + 1
        except ValueError:
            current_answer_index = 0

    st.write(question["question"])

    selected = st.radio(
        "Select an answer:",
        options,
        index=current_answer_index,
        key=f"radio_{st.session_state.current_question}"
    )

    if selected == "-- Select an answer --":
        st.session_state.answers[st.session_state.current_question] = None
    else:
        st.session_state.answers[st.session_state.current_question] = selected

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("Previous", disabled=(st.session_state.current_question == 0)):
            prev_question()

    with col3:
        if st.button("Next", disabled=(st.session_state.current_question == total_questions - 1)):
            next_question()

    if st.session_state.current_question == total_questions - 1:
        if st.button("Submit Quiz"):
            st.session_state.quiz_submitted = True

    # Timer countdown logic (manual navigation)
    if not st.session_state.quiz_submitted:
        now = time.time()
        elapsed = now - st.session_state.last_time

        if elapsed >= 1:
            st.session_state.timer -= 1
            st.session_state.last_time = now

        if st.session_state.timer <= 0:
            st.warning("⏰ Time's up! Please click 'Next' to continue.")
        else:
            timer_placeholder.markdown(f"⏳ Time left: **{st.session_state.timer} seconds**")

        # No automatic rerun, so no sleep or rerun here.

    # Show results after submission
    if st.session_state.quiz_submitted:
        score = 0
        st.header("📊 Results")
        show_answers = st.checkbox("Show Correct Answers", value=True)

        for i, q in enumerate(questions):
            user_ans = st.session_state.answers[i]
            correct = (user_ans == q["answer"])
            if correct:
                score += 1
            st.markdown(f"**Q{i+1}: {q['question']}**")
            st.markdown(f"- Your answer: :blue[{user_ans if user_ans else 'No answer'}] {'✅' if correct else '❌'}")
            if show_answers and not correct:
                st.markdown(f"- Correct answer: :green[{q['answer']}]")

        st.success(f"🎯 Your final score: {score} / {total_questions}")

        if st.button("Restart Quiz"):
            st.session_state.current_question = 0
            st.session_state.answers = [None] * total_questions
            st.session_state.timer = TIMER_SECONDS
            st.session_state.quiz_submitted = False
            st.session_state.last_time = time.time()

if __name__ == "__main__":
    main()
