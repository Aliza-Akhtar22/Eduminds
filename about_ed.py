import streamlit as st
import json
from streamlit_lottie import st_lottie

# Function to load Lottie animation
def load_lottie(path: str):
    with open(path, "r") as f:
        return json.load(f)

# Layout for image and title
col1, col2 = st.columns([1, 5])

with col1:
    st.image("education.png", width=140)

with col2:
    st.title("About EduMinds AI")

# Project description
st.write("""
EduMinds AI is a major project aimed at enhancing student learning through AI by generating questions, quizzes, and providing answers to queries from study materials.
The platform will also generate detailed student analytics reports based on quiz performance. This project is being developed as part of a university initiative, 
with a focus on integrating subject-specific learning experiences and leveraging LLMs.
""")

lottie_animation = load_lottie("about.json")  # Make sure this JSON is transparent
st_lottie(lottie_animation, height=200)  # Not too big
# Load and display the Lottie animation
st.write("""
EduMinds AI is an AI-powered EdTech platform designed to enhance the digital learning experience for students and educators. 
The platform integrates intelligent features that streamline content access, learning engagement, and performance tracking.
""")
st.write(""
"")

st.subheader("Download Items")

lottie_animation = load_lottie("pdf.json")  # Make sure this JSON is transparent
st_lottie(lottie_animation, height=200)

st.write("""
To support seamless learning, students can conveniently browse and download study materials by selecting their respective grade, choosing a subject of interest, and then picking a specific topic. 
This structured approach ensures quick access to relevant content tailored to their academic level.
""")
st.write(""
"")

st.subheader("Chat With Multiple PDFs")

lottie_animation = load_lottie("chat.json")  # Make sure this JSON is transparent
st_lottie(lottie_animation, height=200)

st.write("""
Students can interactively engage with their study materials using the 'Chat with Multiple PDFs' feature, which allows them to upload multiple PDF documents and ask questions directly related to the content. 
This enables a personalized and efficient learning experience, as the system responds with context-aware answers based on the uploaded materials.
""")
st.write(""
"")

st.subheader("Quiz Generation")

lottie_animation = load_lottie("quiz.json")  # Make sure this JSON is transparent
st_lottie(lottie_animation, height=200)

st.write("""
The platform enables dynamic quiz generation based on selected subjects and topics, allowing students to test their understanding through automatically created multiple-choice questions. 
Each quiz is uniquely tailored to the chapters chosen by the student, and immediate feedback with explanations is provided for every question. 
This helps reinforce learning, identify areas for improvement, and track academic progress effectively.
""")
st.write(""
"")

st.subheader("Student Analytics")

lottie_animation = load_lottie("analytics.json")  # Make sure this JSON is transparent
st_lottie(lottie_animation, height=200)

st.write("""
EduMinds AI provides insightful student analytics through a clear and interactive line graph, which visually represents the student's performance across different chapters or topics within a quiz. 
This allows students to easily track their strengths and identify areas where improvement is needed. 
By analyzing trends over time, learners can make informed decisions about their study focus and monitor their academic growth effectively.
""")

