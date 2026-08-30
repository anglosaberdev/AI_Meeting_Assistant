from pathlib import Path
import gradio as gr

from config import settings
from meeting import MeetingAssistant
from transcription import AudioTranscriber


# ============================================================
# Application Components
# ============================================================

print("\nInitializing application...")

transcriber = AudioTranscriber()
meeting_assistant = MeetingAssistant()

print("\nApplication initialized successfully.")


# ============================================================
# Application Workflow
# ============================================================

def process_meeting(audio_file: str, progress=gr.Progress()):
    """
    Complete meeting processing workflow:

        Audio / Microphone
          ↓
        Whisper (Transcription)
          ↓
        Transcript
          ↓
        Terminology normalization
          ↓
        Ollama (Meeting Intelligence)
          ↓
        Meeting Minutes + Tasks
          ↓
        TXT File Output
    """

    if not audio_file:
        raise gr.Error("Please upload or record an audio file first.")

    try:
        # ----------------------------------------------------
        # Step 1: Transcription
        # ----------------------------------------------------
        progress(0.2, desc="Transcribing audio with Whisper...")

        transcript = transcriber.transcribe(audio_file)

        print("\nTranscript:")
        print("-" * 60)
        print(transcript[:1000])

        # ----------------------------------------------------
        # Step 2: Meeting Intelligence
        # ----------------------------------------------------
        progress(0.6, desc="Generating minutes & tasks with Ollama...")

        result = meeting_assistant.process(transcript)

        # ----------------------------------------------------
        # Step 3: Save Output
        # ----------------------------------------------------
        progress(0.9, desc="Saving output file...")

        output_path = Path(settings.output_file)

        output_path.write_text(
            result,
            encoding="utf-8",
        )

        print(f"\nOutput saved to: {output_path}")

        progress(1.0, desc="Processing complete!")

        # ----------------------------------------------------
        # Return to Gradio
        # ----------------------------------------------------
        return result, str(output_path)

    except Exception as error:
        print("\nERROR")
        print("=" * 60)
        print(error)
        print("=" * 60)

        raise gr.Error(f"Processing failed: {error}")


# ============================================================
# Gradio UI Layout & Theme
# ============================================================

theme = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="blue",
).set(
    button_primary_background_fill="*primary_500",
    button_primary_background_fill_hover="*primary_600",
)

with gr.Blocks(theme=theme, title="AI Meeting Assistant") as interface:

    # Header Banner
    with gr.Row():
        gr.Markdown(
            """
            # 🎙️ AI Meeting Assistant
            Upload meeting audio ➡️ Automatic Transcription (Whisper) ➡️ Structured Minutes & Action Items (Ollama)
            ---
            """
        )

    # Main Workflow Layout (2 Columns)
    with gr.Row():

        # Column 1: Audio Input & Control
        with gr.Column(scale=1):
            gr.Markdown("### 1️⃣ Input Audio")

            audio_input = gr.Audio(
                sources=["upload", "microphone"],
                type="filepath",
                label="Upload or Record Audio File (MP3, WAV, M4A...)",
            )

            submit_btn = gr.Button(
                "🚀 Start Processing",
                variant="primary",
                size="lg",
            )

            gr.Markdown(
                """
                > **Note:** Processing time depends on the length of the recording and your system's hardware specs.
                """
            )

        # Column 2: Generated Results & Downloads
        with gr.Column(scale=2):
            gr.Markdown("### 2️⃣ Generated Output")

            output_text = gr.Textbox(
                label="Meeting Minutes & Action Items",
                placeholder="The structured summary, meeting notes, and action items will appear here...",
                lines=18,
                interactive=False,
            )

            download_file = gr.File(
                label="📥 Download Summary File (.txt)",
            )

    # Event Wiring
    submit_btn.click(
        fn=process_meeting,
        inputs=[audio_input],
        outputs=[output_text, download_file],
    )


# ============================================================
# Run Application
# ============================================================

if __name__ == "__main__":

    print("\nStarting Gradio server...")

    interface.launch(
        server_name="127.0.0.1",
        server_port=5000,
    )