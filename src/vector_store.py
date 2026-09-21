from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings


def create_vector_store(
    chunks: list[str],
    embedding_model: OllamaEmbeddings,
) -> FAISS:
    """Create a FAISS vector store from text chunks.

    Args:
        chunks: List of text chunks to embed and store.
        embedding_model: Model to convert text to vectors.

    Returns:
        FAISS vector store ready for retrieval.
    """
    return FAISS.from_texts(chunks, embedding_model)