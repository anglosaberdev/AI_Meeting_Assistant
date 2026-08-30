from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:

    # --------------------------------------------------------
    # Ollama
    # --------------------------------------------------------

    ollama_model: str = "qwen3:1.7b"
    ollama_base_url: str = "http://localhost:11434"

    # --------------------------------------------------------
    # Whisper
    # --------------------------------------------------------

    # Arabic + English + other languages
    whisper_model: str = "openai/whisper-small"

    # --------------------------------------------------------
    # LLM parameters
    # --------------------------------------------------------

    temperature: float = 0.3
    max_tokens: int = 512

    # --------------------------------------------------------
    # Output
    # --------------------------------------------------------

    output_file: str = "meeting_minutes_and_tasks.txt"


settings = Settings()