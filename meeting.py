from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from llm import create_llm
from prompts import TERMINOLOGY_PROMPT, MEETING_MINUTES_PROMPT


class MeetingAssistant:
    """
    Process a meeting transcript:

    Transcript
        ↓
    Terminology normalization
        ↓
    Meeting minutes
    """

    def __init__(self) -> None:

        self.llm = create_llm()
        self.output_parser = StrOutputParser()

        # Terminology chain
        terminology_prompt = ChatPromptTemplate.from_template(
            TERMINOLOGY_PROMPT
        )

        self.terminology_chain = (
            terminology_prompt
            | self.llm
            | self.output_parser
        )

        # Meeting minutes chain
        minutes_prompt = ChatPromptTemplate.from_template(
            MEETING_MINUTES_PROMPT
        )

        self.minutes_chain = (
            minutes_prompt
            | self.llm
            | self.output_parser
        )

    def normalize_terminology(self, transcript: str) -> str:

        if not transcript.strip():
            raise ValueError("Transcript is empty.")

        print("Normalizing terminology...")

        try:
            result = self.terminology_chain.invoke(
                {"transcript": transcript}
            )

            result = str(result).strip()

            return result if result else transcript.strip()

        except Exception as error:
            print(f"Terminology error: {error}")
            return transcript.strip()

    def generate_minutes(self, transcript: str) -> str:

        if not transcript.strip():
            raise ValueError("Transcript is empty.")

        print("Generating meeting minutes...")

        result = self.minutes_chain.invoke(
            {"context": transcript}
        )

        result = str(result).strip()

        if not result:
            raise ValueError("Meeting minutes are empty.")

        return result

    def process(self, transcript: str) -> str:

        if not transcript or not transcript.strip():
            raise ValueError("Transcript is empty.")

        print("\nProcessing meeting...")

        # Step 1: Normalize terminology
        normalized_transcript = self.normalize_terminology(
            transcript
        )

        # Step 2: Generate minutes
        minutes = self.generate_minutes(
            normalized_transcript
        )

        print("Processing completed.")

        return minutes
