"""PDF RAG Chatbot - Command-line interface."""

from src.pdf_loader import load_pdf
from src.splitter import split_text
from src.embeddings import create_embedding_model
from src.vector_store import create_vector_store
from src.retriever import create_retriever
from src.llm import create_llm
from src.rag import ask_question


def create_rag(pdf_path: str):
    """Build the RAG pipeline from a PDF file.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Tuple of (retriever, llm) ready for question answering.
    """
    text = load_pdf(pdf_path)
    chunks = split_text(text)
    embedding_model = create_embedding_model()
    vector_store = create_vector_store(chunks, embedding_model)
    retriever = create_retriever(vector_store)
    llm = create_llm()
    return retriever, llm


def main():
    """Run the interactive command-line chatbot."""
    pdf_path = input("PDF path: ")

    retriever, llm = create_rag(pdf_path)

    print("\nReady! Type 'exit' to quit.\n")

    while True:
        question = input("Question: ")

        if question.lower() == "exit":
            break

        answer = ask_question(question, retriever, llm)

        print("\nAnswer:")
        print(answer)
        print()


if __name__ == "__main__":
    main()