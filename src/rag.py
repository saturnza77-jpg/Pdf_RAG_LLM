from langchain_core.retrievers import BaseRetriever
from langchain_ollama import ChatOllama


def ask_question(
    question: str,
    retriever: BaseRetriever,
    llm: ChatOllama,
) -> str:
    """Answer a question using retrieved context from a PDF.

    Args:
        question: The user's question.
        retriever: Retriever to fetch relevant chunks from the vector store.
        llm: Language model to generate the answer.

    Returns:
        The generated answer as a string.
    """
    docs = retriever.invoke(question)

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""You are a question-answering assistant.

Use only the information in the context below to answer the question.
Do not use outside knowledge.

If the answer cannot be found in the context, say:
"من نتونستم جواب را پیدا کنم لطفا دوباره امتحان کنید."

Answer in the same language as the question:
- If the question is in English, answer in English.
- اگر سؤال به فارسی است، پاسخ را به فارسی بده.

Context:
{context}

Question:
{question}

Answer:
"""
    response = llm.invoke(prompt)
    return response.content