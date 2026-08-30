from langchain_ollama import ChatOllama

from config import settings


def create_llm() -> ChatOllama:
    """
    Create and configure the local Ollama model.
    """

    print("=" * 60)
    print("Ollama Configuration")
    print("=" * 60)
    print(f"Model    : {settings.ollama_model}")
    print(f"Base URL : {settings.ollama_base_url}")
    print("=" * 60)

    llm = ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
        temperature=settings.temperature,
        num_predict=settings.max_tokens,
    )

    return llm