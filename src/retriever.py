from langchain_community.vectorstores import FAISS


def create_retriever(vector_store: FAISS, k: int = 4):
    """Create a retriever from a vector store.

    Args:
        vector_store: FAISS vector store to search.
        k: Number of top chunks to retrieve.

    Returns:
        Retriever configured to fetch k most relevant chunks.
    """
    return vector_store.as_retriever(search_kwargs={"k": k})