import streamlit as st
import psycopg2
import random

# Database connection
def get_connection():
    return psycopg2.connect(
        dbname="Quiz_Generation",
        user="postgres",
        password="aliza123",
        host="localhost",
        port="5432"
    )

def fetch_subjects():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT subject_id, subject_name FROM class_sub")
    subjects = cur.fetchall()
    conn.close()
    return subjects

def fetch_chapters(subject_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT chapter_id, chapter_name FROM chap_sub WHERE subject_id = %s", (subject_id,))
    chapters = cur.fetchall()
    conn.close()
    return chapters

def fetch_questions(chapter_ids):
    conn = get_connection()
    cur = conn.cursor()
    format_strings = ','.join(['%s'] * len(chapter_ids))
    query = f"""
        SELECT cp.chapter_id, qa.question_id, qa.question, qa.option_1, qa.option_2, qa.option_3, qa.option_4,
               qa.option_1_exp, qa.option_2_exp, qa.option_3_exp, qa.option_4_exp, qa.correct_option
        FROM ques_ans qa
        JOIN chap_pdfs cp ON qa.pdf_id = cp.pdf_id
        WHERE cp.chapter_id IN ({format_strings})
    """
    cur.execute(query, tuple(chapter_ids))
    questions = cur.fetchall()
    conn.close()
    return questions

# UI
col1, col2 = st.columns([1, 5]) 
with col1:
    st.image("quiz.png", width=140)  
with col2:
    st.title("EduMinds AI – Quiz Generator")

# Subject selection
subjects = fetch_subjects()
subject_names = {name: sid for sid, name in subjects}
subject = st.selectbox("Select Subject", list(subject_names.keys()))

if subject:
    subject_id = subject_names[subject]
    chapters = fetch_chapters(subject_id)
    chapter_dict = {name: cid for cid, name in chapters}
    selected_chapters = st.multiselect("Select at least 3 Chapters", list(chapter_dict.keys()))

    if len(selected_chapters) >= 3:
        if st.button("Start Quiz"):
            chapter_ids = [chapter_dict[chap] for chap in selected_chapters]
            all_questions = fetch_questions(chapter_ids)
            random.shuffle(all_questions)

            st.session_state.questions = all_questions
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.chapter_scores = {cid: {"correct": 0, "total": 0} for cid in chapter_ids}
            st.session_state.quiz_done = False
            st.session_state.chapter_names = {cid: name for name, cid in chapter_dict.items()}
            st.session_state.selected_subject = subject

if "questions" in st.session_state and not st.session_state.quiz_done:
    questions = st.session_state.questions
    q_index = st.session_state.q_index

    if q_index < len(questions):
        q = questions[q_index]
        chapter_id = q[0]
        question_text = q[2]
        options = q[3:7]

        st.subheader(f"Q{q_index + 1}: {question_text}")
        selected = st.radio("Choose an option:", options, key=f"q{q_index}")

        if st.button("Submit Answer", key=f"submit{q_index}"):
            correct_option = q[11]
            st.session_state.chapter_scores[chapter_id]["total"] += 1

            if options.index(selected) + 1 == correct_option:
                st.success("Correct!")
                st.session_state.score += 1
                st.session_state.chapter_scores[chapter_id]["correct"] += 1
            else:
                st.error("Wrong Answer!")
                explanation = q[6 + correct_option]
                st.info(f"Correct Answer: {options[correct_option - 1]}")
                st.write(f"Explanation: {explanation}")

            st.session_state.q_index += 1
            if st.session_state.q_index >= len(questions):
                st.session_state.quiz_done = True
                # Save latest quiz results
                st.session_state.quiz_results = {
                    "subject": st.session_state.selected_subject,
                    "chapters": st.session_state.chapter_scores,
                    "chapter_names": st.session_state.chapter_names
                }
                st.experimental_rerun()

# Final Score
if "quiz_done" in st.session_state and st.session_state.quiz_done:
    st.success(f"Quiz Completed! Your Score: {st.session_state.score} / {len(st.session_state.questions)}")
    if st.button("Take Again"):
        for key in ["questions", "q_index", "score", "quiz_done", "chapter_scores", "quiz_results"]:
            st.session_state.pop(key, None)
        st.experimental_rerun()
