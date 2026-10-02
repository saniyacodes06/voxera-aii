
# 🎙️ Voxera AI

### AI-Powered Video & Meeting Intelligence Assistant

> **Turn videos and meetings into intelligent, actionable insights.**

Voxera AI is an AI-powered video and meeting assistant that converts YouTube videos and uploaded recordings into structured insights.

It uses **Whisper for transcription, Mistral AI for intelligent analysis, LangChain for orchestration, Sentence Transformers for embeddings, and ChromaDB for retrieval-augmented generation (RAG).**

🎥 Video → 📝 Transcript → 🧠 AI Insights → 💬 Ask Voxera

---

## 🚀 Live Demo

👉 **[Try Voxera AI Live](https://voxera-aii-ndfkvbpe5dxjqivmrexscs.streamlit.app/)**

You can provide a public YouTube video or upload a video/audio recording and let Voxera analyze it.

---

## 📸 Screenshots

### 🏠 Voxera AI Dashboard
<img width="1470" height="956" alt="Screenshot 2026-10-02 at 11 05 44" src="https://github.com/user-attachments/assets/84d17aac-0f3f-4583-88fb-4e9e6c62f528" />
<img width="1470" height="956" alt="Screenshot 2026-10-02 at 11 31 37" src="https://github.com/user-attachments/assets/94e69a90-818e-4073-812d-2d9d024b8041" />

![Voxera AI Dashboard](![]()
)

### 🧠 AI-Generated Insights
<img width="1470" height="956" alt="Screenshot 2026-10-02 at 11 31 24" src="https://github.com/user-attachments/assets/e35757d7-db34-4db3-a46a-c7560abb9cad" />

![Voxera AI Insights]()

### 💬 Ask Voxera — RAG Assistant

<img width="1465" height="885" alt="ask" src="https://github.com/user-attachments/assets/d9368aab-ff7a-4c21-bc5c-5258d93d8f19" />

> Screenshots show the live Voxera AI interface, AI-generated insights, and transcript-based question answering.

---

# ✨ Features

### 🎥 Video & Audio Input

- Analyze public YouTube videos
- Upload video recordings
- Upload audio recordings
- Supports common video/audio formats
- Automatic audio extraction and normalization

### 📝 Automatic Transcription

Voxera uses **OpenAI Whisper** to convert speech into text.

Features include:

- Automatic speech-to-text
- Multiple language support
- Language selection
- Auto-detection option
- Audio normalization for reliable transcription

### 🧠 AI-Powered Analysis

Mistral AI analyzes the generated transcript and extracts:

- 📋 Meeting Summary
- ✅ Action Items
- 🎯 Key Decisions
- ❓ Open Questions
- 🏷️ Intelligent Title

### 💬 Ask Voxera

Users can ask questions about the analyzed video or meeting.

Ask Voxera uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant parts of the transcript before generating an answer.

This helps Voxera answer questions based on the actual recording instead of relying only on the language model's general knowledge.

### 🔐 Secure API Management

API credentials are not stored in the source code.

- Local development → `.env`
- Cloud deployment → Streamlit Secrets
- `.env` is excluded through `.gitignore`

---

# 🧠 How Voxera Works

Voxera follows an end-to-end AI pipeline:

```text
                 ┌────────────────────────┐
                 │   YouTube / Upload     │
                 └────────────┬───────────┘
                              │
                              ▼
                 ┌────────────────────────┐
                 │    Audio Processing    │
                 │    yt-dlp + FFmpeg     │
                 │   Audio Normalization  │
                 └────────────┬───────────┘
                              │
                              ▼
                 ┌────────────────────────┐
                 │       Whisper          │
                 │      Transcription     │
                 └────────────┬───────────┘
                              │
                              ▼
                       ┌────────────┐
                       │ Transcript │
                       └─────┬──────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
       ┌─────────────────┐      ┌─────────────────┐
       │   Mistral AI    │      │    ChromaDB     │
       │ Transcript      │      │ Vector Store    │
       │ Analysis        │      │ + Embeddings    │
       └────────┬────────┘      └────────┬────────┘
                │                         │
                ▼                         ▼
       ┌─────────────────┐      ┌─────────────────┐
       │ AI Insights     │      │  Ask Voxera     │
       │                 │      │      RAG        │
       │ • Summary       │      │                 │
       │ • Actions       │      │ Retrieve →      │
       │ • Decisions     │      │ Generate Answer │
       │ • Questions     │      │                 │
       └─────────────────┘      └─────────────────┘
