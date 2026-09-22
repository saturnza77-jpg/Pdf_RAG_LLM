"""PDF RAG Chatbot - Streamlit web interface."""

import os
import streamlit as st

from app import create_rag
from src.rag import ask_question


st.markdown("""
<style>

.answer-box {
    background: white;
    padding: 22px 25px;
    border-radius: 14px;
    border: 1px solid #E9D5FF;
    box-shadow: 0 4px 12px rgba(91, 33, 182, 0.08);

    font-size: 19px;
    line-height: 2;
    color: #29233D;

    direction: rtl;
    text-align: right;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #F3E8FF;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.stButton > button {
    background-color: #8A2BE2;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


st.set_page_config(
    page_title="PDF RAG Chatbot",
    page_icon=":material/article:",
)

st.title(":material/article: PDF RAG Chatbot")

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

    if st.button(":material/description: Process PDF"):
        os.makedirs("data/uploads", exist_ok=True)
        pdf_path = os.path.join("data/uploads", uploaded_file.name)

        with open(pdf_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        try:
            with st.spinner("Processing PDF..."):
                retriever, llm = create_rag(pdf_path)

            st.session_state.retriever = retriever
            st.session_state.llm = llm

            st.success(":material/check: PDF is ready!")

        except Exception as e:
            st.error(f":material/warning: Error processing PDF: {e}")

# Question section
if st.session_state.retriever is not None:
    question = st.text_input("Enter your question:")

    if st.button(":material/search: Ask"):
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

                st.subheader(":material/smart_toy: Answer")
                st.markdown(f"""
                <div class="answer-box">
                {answer}
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f":material/warning: Error answering: {e}")
else:
    st.info("Please upload and process a PDF first.")