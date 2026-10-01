cat > README.md <<'EOF'
# 🎙️ Voxera AI

### AI-Powered Video & Meeting Intelligence Assistant

Voxera AI transforms YouTube videos and uploaded recordings into structured, actionable insights using AI.

🎥 **Analyze videos** → 📝 **Transcribe** → 🧠 **Generate insights** → 💬 **Ask questions with RAG**

## 🚀 Live Demo

https://voxera-aii-ndfkvbpe5dxjqivmrexcscs.streamlit.app/

## ✨ Features

- 🎥 Analyze public YouTube videos
- 📁 Upload video/audio recordings
- 📝 Automatic speech-to-text transcription using Whisper
- 🧠 AI-generated summaries
- ✅ Action item extraction
- 🎯 Key decision extraction
- ❓ Open question detection
- 💬 Ask Voxera conversational RAG assistant
- 🔎 Transcript-based semantic retrieval
- 🌐 Live Streamlit deployment
- 🔐 Secure API key management using Streamlit Secrets

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │   YouTube / Upload  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Audio Processing  │
                    │   yt-dlp / FFmpeg   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Whisper        │
                    │    Transcription    │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
          ┌──────────────────┐   ┌──────────────────┐
          │   Voxera AI      │   │  Vector Store    │
          │ Mistral Analysis │   │   ChromaDB       │
          └────────┬─────────┘   └────────┬─────────┘
                   │                      │
                   ▼                      ▼
          ┌──────────────────┐   ┌──────────────────┐
          │ Summary          │   │   Ask Voxera     │
          │ Action Items     │   │      RAG         │
          │ Decisions        │   │   Q&A Assistant  │
          │ Questions        │   └──────────────────┘
          └──────────────────┘
