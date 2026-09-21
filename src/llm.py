from langchain_ollama import ChatOllama


def create_llm(model: str = "gemma3:12b", temperature: float = 0.0) -> ChatOllama:
    """Create a language model for generating answers.

    Args:
        model: Name of the Ollama chat model to use.
        temperature: Randomness of responses (0 = deterministic).

    Returns:
        Configured ChatOllama instance.
    """
    return ChatOllama(model=model, temperature=temperature)