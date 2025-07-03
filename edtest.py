import streamlit as st

about_page = st.Page(
    page="views/about_ed.py",
    title="About",
    default=True,
)

selected_page = st.Page(
    page="views/gra_sub.py",
    title="Download Items",
)

pdfs_page = st.Page(
    page="views/pdfs.py",
    title="Chat with PDFs",
)

quiz_page = st.Page(
    page="views/quiz.py",
    title="Take A Quiz"
)

analytics_page = st.Page(
    page="views/analytics.py",
    title="Student Analytics"
)
pg = st.navigation(pages=[about_page, selected_page, pdfs_page, quiz_page, analytics_page])
pg.run()
