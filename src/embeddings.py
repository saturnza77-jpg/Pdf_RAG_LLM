from langchain_ollama import OllamaEmbeddings


def create_embedding_model(model: str = "qwen3-embedding:0.6b") -> OllamaEmbeddings:
    """Create an embedding model for converting text to vectors.

    Args:
        model: Name of the Ollama embedding model to use.

    Returns:
        Configured OllamaEmbeddings instance.
    """
    return OllamaEmbeddings(model=model)