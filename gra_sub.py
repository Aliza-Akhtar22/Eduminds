import streamlit as st
import psycopg2

# --- Database Connection ---
def get_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="Quiz_Generation",
        user="postgres",
        password="aliza123"
    )

# --- UI Layout ---
col1, col2 = st.columns([1, 5])

with col1:
    st.image("purpose.png", width=100)

with col2:
    st.title("Download Items")

# Static mapping of subjects and topics
subject_topics = {
    "Science": [
        "Chemical Reactions and Equations", "Acids, Bases and Salts", "Metals and Non-metals",
        "Carbon and its Compounds", "Life Processes", "Control and Coordination",
        "How do Organisms Reproduce?", "Heredity", "Light – Reflection and Refraction",
        "The Human Eye and the Colourful World", "Electricity", "Magnetic Effects of Electric Current",
        "Our Environment"
    ],
    "Mathematics": [
        "Real Numbers", "Polynomials", "Pair of Linear Equations in Two Variables", "Quadratic Equations",
        "Arithmetic Progressions", "Triangles", "Coordinate Geometry", "Introduction to Trigonometry",
        "Some Applications of Trigonometry", "Circles", "Areas Related to Circles", "Surface Areas and Volumes",
        "Statistics", "Probability"
    ],
    "English": [
        "A Letter to God", "Nelson Mandela: Long Walk to Freedom",
        "Two Stories about Flying", "From the Diary of Anne Frank", "Glimpses of India",
        "Mijbil the Otter", "Madam Rides the Bus", "The Sermon at Benares",
        "The Proposal"
    ],
    "History": [
        "The Rise of Nationalism in Europe", "Nationalism in India",
        "The Making of a Global World", "The Age of Industrialisation",
        "Print Culture and The Modern World"
    ],
    "Geography": [
        "Resources and Development", "Forest and Wildlife Resources",
        "Water Resources", "Agriculture", "Minerals and Energy Resources",
        "Manufacturing Industries", "Lifelines of National Economy"
    ],
    "Politics": [
        "Power Sharing", "Federalism", "Gender Religion and Caste", "Political Parties", "Outcomes of Democracy"
    ]
}

# --- Grade Selection ---
st.header("Grade Selection")
grade = st.selectbox("Select a Grade", ["Grade 10"])

if grade:
    st.header("Subject Selection")
    subject = st.selectbox("Select a Subject", list(subject_topics.keys()))

    if subject:
        st.header("Select a Topic")
        topic = st.selectbox("Select a Topic", subject_topics[subject])

        if topic:
            st.write(f"Selected Topic: {topic}")

            try:
                conn = get_connection()
                cursor = conn.cursor()

                # Step 1: Get subject_id
                cursor.execute("SELECT subject_id FROM class_sub WHERE subject_name = %s AND class = 10", (subject,))
                result = cursor.fetchone()
                if result:
                    subject_id = result[0]

                    # Step 2: Get chapter_id
                    cursor.execute("SELECT chapter_id FROM chap_sub WHERE chapter_name = %s AND subject_id = %s", (topic, subject_id))
                    chapter_result = cursor.fetchone()
                    if chapter_result:
                        chapter_id = chapter_result[0]

                        # Step 3: Get PDF URL
                        cursor.execute("SELECT pdf_url FROM chap_pdfs WHERE subject_id = %s AND chapter_id = %s", (subject_id, chapter_id))
                        pdf_result = cursor.fetchone()
                        if pdf_result:
                            pdf_url = pdf_result[0]
                            st.markdown(f"### 📄 [Download PDF for '{topic}']({pdf_url})", unsafe_allow_html=True)
                        else:
                            st.warning("❌ PDF not found for this topic.")
                    else:
                        st.warning("❌ Chapter not found in database.")
                else:
                    st.warning("❌ Subject not found in database.")

                cursor.close()
                conn.close()

            except Exception as e:
                st.error(f"⚠️ Database error: {e}")
