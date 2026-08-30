# 🎙️ AI Meeting Assistant

An AI-powered meeting assistant that converts **audio recordings into structured meeting minutes and action items** using **Whisper, Ollama, LangChain, and Gradio**.

The application supports **audio upload or microphone recording**, automatically transcribes the meeting, normalizes financial terminology, and generates concise meeting minutes with decisions and tasks.

---

## 🚀 Features

* 🎤 Upload or record meeting audio
* 📝 Automatic speech-to-text transcription using **OpenAI Whisper**
* 🌍 Supports Arabic, English, and other languages supported by Whisper
* 💰 Financial terminology normalization
* 🤖 Local LLM processing using **Ollama**
* 🦜🔗 LangChain prompt and processing pipelines
* 📋 Generates structured meeting minutes
* ✅ Extracts decisions and action items
* 📥 Download results as a `.txt` file
* 🖥️ Simple interactive **Gradio** interface
* 🍎 Supports Apple Silicon acceleration through **MPS** when available
* 🔒 Runs locally without requiring a cloud LLM API

---

## 🏗️ Architecture

```text
              🎙️ Audio / Microphone
                       │
                       ▼
              ┌─────────────────┐
              │     Whisper     │
              │ Speech-to-Text  │
              └────────┬────────┘
                       │
                       ▼
                  Transcript
                       │
                       ▼
          ┌────────────────────────┐
          │ Terminology Normalizer │
          │       Ollama LLM       │
          └────────────┬───────────┘
                       │
                       ▼
           Normalized Transcript
                       │
                       ▼
          ┌────────────────────────┐
          │   Meeting Assistant    │
          │       Ollama LLM       │
          └────────────┬───────────┘
                       │
                       ▼
             Meeting Minutes
                       │
              ┌────────┴────────┐
              ▼                 ▼
       Gradio Output       TXT File
```

---

## 🧠 Processing Pipeline

The application follows three main stages:

### 1. Audio Transcription

The recorded meeting is processed by the Whisper model:

```text
Audio → Whisper → Transcript
```

The default model is:

```text
openai/whisper-small
```

---

### 2. Terminology Normalization

The transcript is passed to a local Ollama LLM to correct financial terminology and acronyms.

For example:

```text
HSA → Health Savings Account (HSA)
ROA → Return on Assets (ROA)
401k → 401(k) retirement savings plan
```

The original meaning, names, and numbers are preserved.

```text
Transcript
    ↓
Financial Terminology Normalization
    ↓
Corrected Transcript
```

---

### 3. Meeting Minutes Generation

The normalized transcript is passed to the LLM again to generate:

* Key Discussion Points
* Decisions
* Tasks
* Task owners when available
* Deadlines when available

If an owner or deadline is not mentioned:

```text
Not specified
```

---

## 🛠️ Tech Stack

| Technology                | Purpose                   |
| ------------------------- | ------------------------- |
| Python                    | Application development   |
| Gradio                    | Web interface             |
| Hugging Face Transformers | Whisper integration       |
| OpenAI Whisper            | Speech-to-text            |
| PyTorch                   | Model execution           |
| Ollama                    | Local LLM inference       |
| Qwen3                     | Meeting intelligence      |
| LangChain                 | LLM pipelines and prompts |
| Pathlib                   | File handling             |

---

## 📁 Project Structure

```text
ai-meeting-assistant/
│
├── app.py
├── config.py
├── llm.py
├── meeting.py
├── transcription.py
├── prompts.py
├── requirements.txt
├── README.md
│
└── meeting_minutes_and_tasks.txt
```

### `app.py`

Main Gradio application.

Responsible for:

* Audio input
* Processing workflow
* Progress updates
* Displaying meeting minutes
* Downloading the generated TXT file

### `config.py`

Contains application configuration:

```python
ollama_model = "qwen3:1.7b"
ollama_base_url = "http://localhost:11434"
whisper_model = "openai/whisper-small"
temperature = 0.3
max_tokens = 512
```

### `llm.py`

Creates and configures the local Ollama model using LangChain.

### `meeting.py`

Contains the `MeetingAssistant` class.

Responsible for:

```text
Transcript
    ↓
Terminology Normalization
    ↓
Meeting Minutes
```

### `transcription.py`

Contains the `AudioTranscriber` class and uses Hugging Face Transformers to run Whisper.

### `prompts.py`

Contains the prompts used for:

* Financial terminology normalization
* Meeting minutes generation

---

## ⚙️ Requirements

Recommended environment:

```text
Python 3.11+
Ollama
PyTorch
```

The application can use Apple Silicon **MPS** acceleration when available.

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-meeting-assistant.git

cd ai-meeting-assistant
```

### 2. Create a virtual environment

```bash
python3.11 -m venv .venv
```

Activate it:

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🤖 Install Ollama

Install Ollama and make sure the Ollama server is running.

Then download the Qwen model:

```bash
ollama pull qwen3:1.7b
```

Verify that the model is available:

```bash
ollama list
```

The application expects Ollama to run at:

```text
http://localhost:11434
```

---

## ▶️ Run the Application

Start the Gradio application:

```bash
python app.py
```

The application will run on:

```text
http://127.0.0.1:5000
```

Open the address in your browser.

---

## 🎤 How to Use

1. Open the Gradio application.
2. Upload a meeting recording **or record audio using your microphone**.
3. Click **Start Processing**.
4. Whisper transcribes the audio.
5. The transcript is normalized for financial terminology.
6. Ollama generates structured meeting minutes.
7. Review the generated output.
8. Download the `.txt` meeting summary.

---

## 📄 Example Output

```text
Key Discussion Points

- Reviewed the quarterly financial performance.
- Discussed the company's ROA.
- Reviewed employee HSA contributions.

Decisions

- The team agreed to review the financial report again next week.

Tasks

- Prepare the updated financial report.
  Owner: Not specified
  Deadline: Not specified
```

---

## 🔧 Configuration

You can modify the application settings in `config.py`.

```python
@dataclass(frozen=True)
class Settings:

    ollama_model: str = "qwen3:1.7b"

    ollama_base_url: str = "http://localhost:11434"

    whisper_model: str = "openai/whisper-small"

    temperature: float = 0.3

    max_tokens: int = 512

    output_file: str = "meeting_minutes_and_tasks.txt"
```

### Change the Ollama model

```python
ollama_model: str = "your-model"
```

### Change the Whisper model

```python
whisper_model: str = "openai/whisper-small"
```

---

## 🔐 Local AI Architecture

One of the main goals of this project is to keep the AI processing local.

```text
Meeting Audio
     ↓
Local Whisper
     ↓
Local Transcript
     ↓
Local Ollama
     ↓
Meeting Minutes
```

No external LLM API is required for the meeting analysis.

---

## 🎯 Use Cases

This project can be useful for:

* Business meetings
* Financial meetings
* Team discussions
* Project meetings
* Client calls
* Research meetings
* Interviews
* Internal meeting documentation

---

## 🚧 Future Improvements

Possible future enhancements:

* [ ] Export to PDF
* [ ] Export to DOCX
* [ ] Speaker diarization
* [ ] Automatic speaker identification
* [ ] Timestamped transcripts
* [ ] JSON output
* [ ] Database storage
* [ ] Searchable meeting history
* [ ] Multiple meeting languages
* [ ] Email meeting summaries
* [ ] Calendar integration
* [ ] RAG-based meeting history
* [ ] Automatic follow-up task tracking

---

## 📚 Key Concepts

This project demonstrates practical implementation of:

* Generative AI
* Local LLMs
* Speech-to-Text
* Prompt Engineering
* LangChain
* Ollama
* Transformers
* Meeting Intelligence
* AI-powered Information Extraction
* Natural Language Processing

---

## 👨‍💻 Author

**Anglo Saber**

Applied NLP Researcher | Generative AI | LLMs | RAG | iOS Development

---

## ⭐ Project

If you find this project useful, consider giving it a ⭐ on GitHub.
