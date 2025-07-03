import streamlit as st
import matplotlib.pyplot as plt

# Display Title
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assessment.png", width=120)
with col2:
    st.title("EduMinds AI – Analytical Report")

# Check if quiz results exist
if "quiz_results" not in st.session_state:
    st.warning("No quiz data found. Please take a quiz first.")
else:
    data = st.session_state.quiz_results
    subject = data["subject"]
    chapter_scores = data["chapters"]
    chapter_names = data["chapter_names"]

    st.subheader(f"Subject: {subject}")
    
    chapters = []
    accuracy = []

    for chap_id, scores in chapter_scores.items():
        total = scores["total"]
        correct = scores["correct"]
        acc = (correct / total) * 100 if total > 0 else 0
        chapters.append(chapter_names.get(chap_id, f"Chapter {chap_id}"))
        accuracy.append(acc)


    col3, col4 = st.columns([5, 3])
    
    with col3:
        fig, ax = plt.subplots()
        fig.patch.set_alpha(0)  # Transparent figure background
        ax.patch.set_alpha(0)   # Transparent axes background

# Plot line
        ax.plot(chapters, accuracy, marker='o', linestyle='-', color='#00C49F', label='Accuracy %')

# Titles and labels with white color for dark mode visibility
        ax.set_title("Chapter-wise Performance", color='white')
        ax.set_xlabel("Chapters", color='white')
        ax.set_ylabel("Accuracy (%)", color='white')
        ax.set_ylim(0, 110)
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')
        ax.grid(False)
        legend = ax.legend()
        for text in legend.get_texts():
            text.set_color("black")  # Or white if you prefer
        st.pyplot(fig)

    with col4:
        total_questions = sum(score["total"] for score in chapter_scores.values())
        obtained_score = sum(score["correct"] for score in chapter_scores.values())

        donut_labels = ["Correct", "Incorrect"]
        donut_values = [obtained_score, total_questions - obtained_score]
        colors = ["#00C49F", "#FF8042"]  # Green for correct, Orange for incorrect

        fig2, ax2 = plt.subplots()
        fig2.patch.set_alpha(0)
        ax2.pie(donut_values, labels=donut_labels, colors=colors, startangle=90, 
                wedgeprops=dict(width=0.4), autopct='%1.1f%%', textprops={'color': "white"})
        ax2.set_title("Overall Score Distribution", color='white')
    
        st.pyplot(fig2)
