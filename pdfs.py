import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
#import asyncio
import warnings
from htmlTemplates import css, bot_template, user_template
#from langchain_huggingface import HuggingFaceEndpoint


warnings.filterwarnings("ignore", category=DeprecationWarning)

# Function to extract text from PDFs
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to split the extracted text into chunks
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create a vectorstore using FAISS
def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

# Function to get a conversational retrieval chain
def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            col1, col2 = st.columns([1, 9])
            with col1:
                st.image("icons8-student-64.png", width=50)
            with col2:
                st.write(f"<div class='message'>{message.content}</div>", unsafe_allow_html=True)
        else:
            # Bot message
            col1, col2 = st.columns([1, 9])
            with col1:
                st.image("icons8-chatbot-64.png", width=50)
            with col2:
                st.write(f"<div class='message'>{message.content}</div>", unsafe_allow_html=True)
            st.write('<br>', unsafe_allow_html=True)

# Main function to run the Streamlit app

load_dotenv()
col1, col2 = st.columns([1, 5])  

    # In the first column, display the image
with col1:
    st.image("question.png", width=140)  

    # In the second column, display the title
with col2:
    st.title("Chat With Multiple PDFs")
st.write(css, unsafe_allow_html=True)
    
    
if "conversation" not in st.session_state:
        st.session_state.conversation = None
if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

user_question = st.text_input("Ask a question about your documents:")
    
    # Handle user input
if user_question:
        handle_userinput(user_question)

    # File uploader in sidebar for PDFs
with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # Extract text from the uploaded PDFs
                raw_text = get_pdf_text(pdf_docs)

                # Split the text into chunks
                text_chunks = get_text_chunks(raw_text)

                # Create a vectorstore using FAISS
                vectorstore = get_vectorstore(text_chunks)

                # Initialize the conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)



