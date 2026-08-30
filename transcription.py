import torch
from transformers import pipeline

from config import settings


class AudioTranscriber:
    """
    Converts meeting audio into text using Whisper.
    """

    def __init__(self) -> None:

        # ----------------------------------------------------
        # Select device
        # ----------------------------------------------------

        if torch.backends.mps.is_available():
            self.device = "mps"
        else:
            self.device = "cpu"

        print("=" * 60)
        print("Whisper Configuration")
        print("=" * 60)
        print(f"Device       : {self.device}")
        print(f"Whisper model: {settings.whisper_model}")
        print("=" * 60)

        # ----------------------------------------------------
        # Create Whisper pipeline
        # ----------------------------------------------------

        try:

            self._pipeline = pipeline(
                task="automatic-speech-recognition",
                model=settings.whisper_model,
                chunk_length_s=30,
                device=self.device,
            )

        except Exception as error:

            print("\nFailed to initialize Whisper.")
            print(f"Error: {error}")

            raise

    # --------------------------------------------------------
    # Transcription
    # --------------------------------------------------------

    def transcribe(self, audio_file: str) -> str:

        if not audio_file:
            raise ValueError(
                "Audio file is required."
            )

        print("\nStarting transcription...")
        print(f"Audio file: {audio_file}")

        try:

            result = self._pipeline(
                audio_file,
                batch_size=1,
            )

        except Exception as error:

            print("\nWhisper transcription failed.")
            print(f"Error: {error}")

            raise

        transcript = result.get(
            "text",
            "",
        ).strip()

        if not transcript:

            raise ValueError(
                "No speech was detected in the audio file."
            )

        print("\nTranscription completed.")
        print(f"Characters: {len(transcript)}")

        return transcript