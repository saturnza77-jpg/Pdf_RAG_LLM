"""PDF RAG Chatbot - Streamlit web interface."""

import os
import streamlit as st

from app import create_rag
from src.rag import ask_question


st.set_page_config(
    page_title="PDF RAG Chatbot",
    page_icon="📚",
)

st.title("📚 PDF RAG Chatbot")

# Initialize session state
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "llm" not in st.session_state:
    st.session_state.llm = None

# Upload PDF
uploaded_file = st.file_uploader("Choose a PDF file:", type=["pdf"])

# Process PDF
if uploaded_file is not None:
    st.write(f"Selected file: {uploaded_file.name}")

    if st.button("📄 Process PDF"):
        os.makedirs("data/uploads", exist_ok=True)
        pdf_path = os.path.join("data/uploads", uploaded_file.name)

        with open(pdf_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        try:
            with st.spinner("Processing PDF..."):
                retriever, llm = create_rag(pdf_path)

            st.session_state.retriever = retriever
            st.session_state.llm = llm

            st.success("✅ PDF is ready!")

        except Exception as e:
            st.error(f"❌ Error processing PDF: {e}")

# Question section
if st.session_state.retriever is not None:
    question = st.text_input("Enter your question:")

    if st.button("🔍 Ask"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            try:
                with st.spinner("Finding answer..."):
                    answer = ask_question(
                        question,
                        st.session_state.retriever,
                        st.session_state.llm,
                    )

                st.subheader("🤖 Answer")
                st.write(answer)

            except Exception as e:
                st.error(f"❌ Error answering: {e}")
else:
    st.info("Please upload and process a PDF first.")