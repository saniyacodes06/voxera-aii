import os
import streamlit as st

from dotenv import load_dotenv

from core.pipeline import process_and_transcribe
from core.analyzer import analyze_transcript
from core.rag_engine import build_rag_chain, ask_question


load_dotenv(override=True)


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Voxera AI",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "result" not in st.session_state:
    st.session_state.result = None

if "transcript" not in st.session_state:
    st.session_state.transcript = None

if "audio_path" not in st.session_state:
    st.session_state.audio_path = None

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 50% 0%,
                rgba(99, 102, 241, 0.12),
                transparent 35%
            ),
            #080b14;
        color: #f8fafc;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 3rem;
        padding-bottom: 5rem;
    }

    .voxera-logo {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
    }

    .voxera-logo span {
        color: #8b5cf6;
    }

    .voxera-tagline {
        text-align: center;
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 3rem;
    }

    .source-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .card-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }

    .card-description {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;
        padding: 0.7rem 1rem;
        font-weight: 700;
        font-size: 1rem;
        background: linear-gradient(
            135deg,
            #7c3aed,
            #4f46e5
        );
        color: white;
    }

    .stButton > button:hover {
        border: none;
        transform: translateY(-1px);
    }

    div[data-testid="stPopover"] {
        position: fixed;
        right: 30px;
        bottom: 25px;
        z-index: 999;
    }

    div[data-testid="stPopover"] > button {
        border-radius: 50px;
        padding: 0.75rem 1.2rem;
        background: #7c3aed;
        color: white;
        border: none;
        font-weight: 700;
        box-shadow: 0 8px 30px rgba(124, 58, 237, 0.35);
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="voxera-logo">Voxera<span> AI</span></div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="voxera-tagline">'
    'Turn videos and meetings into intelligent insights.'
    '</div>',
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SOURCE INPUT
# --------------------------------------------------

left, right = st.columns(2, gap="large")


with left:

    st.markdown(
        """
        <div class="source-card">
            <div class="card-title">🔗 YouTube Video</div>
            <div class="card-description">
                Paste a YouTube video URL and let Voxera analyze it.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    youtube_url = st.text_input(
        "YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed",
    )


with right:

    st.markdown(
        """
        <div class="source-card">
            <div class="card-title">📁 Upload Recording</div>
            <div class="card-description">
                Upload a video or audio file from your device.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload",
        type=[
            "mp4",
            "mkv",
            "mov",
            "webm",
            "mp3",
            "wav",
            "m4a",
        ],
        label_visibility="collapsed",
    )


# --------------------------------------------------
# LANGUAGE
# --------------------------------------------------

st.markdown("###")

language_option = st.selectbox(
    "Transcript language",
    [
        "Auto Detect",
        "English",
        "Hindi / Hinglish",
    ],
)


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

st.markdown("###")

analyze = st.button(
    "✨ Analyze with Voxera"
)


if analyze:

    if not youtube_url and not uploaded_file:

        st.warning(
            "Please paste a YouTube URL or upload a recording first."
        )

    elif youtube_url and uploaded_file:

        st.warning(
            "Please use either YouTube or file upload, not both."
        )

    else:

        try:

            # ------------------------------------------
            # PREPARE SOURCE
            # ------------------------------------------

            if youtube_url:

                source = youtube_url.strip()

            else:

                os.makedirs("downloads", exist_ok=True)

                file_path = os.path.join(
                    "downloads",
                    uploaded_file.name
                )

                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                source = file_path


            # ------------------------------------------
            # LANGUAGE
            # ------------------------------------------

            if language_option == "English":
                whisper_language = "en"

            elif language_option == "Hindi / Hinglish":
                whisper_language = "hi"

            else:
                whisper_language = None


            # ------------------------------------------
            # STEP 1 — TRANSCRIPTION
            # ------------------------------------------

            with st.status(
                "🎙️ Voxera is processing your recording...",
                expanded=True
            ) as status:

                st.write("🎧 Extracting audio...")

                audio_path, transcript = process_and_transcribe(
                    source,
                    language=whisper_language
                )

                st.session_state.transcript = transcript

                st.write("📝 Transcription complete.")

                st.write("🔎 Preparing Ask Voxera...")

                st.session_state.rag_chain = build_rag_chain(
                    transcript
                )

                # --------------------------------------
                # STEP 2 — AI ANALYSIS
                # --------------------------------------

                st.write("🧠 Generating AI insights...")

                result = analyze_transcript(
                    transcript
                )

                st.session_state.result = result

                status.update(
                    label="✅ Voxera analysis complete!",
                    state="complete",
                    expanded=False
                )


            st.success(
                "Your recording has been successfully analyzed."
            )


        except Exception as e:

            st.session_state.result = None

            error_message = str(e).lower()

            if (
                "sign in to confirm" in error_message
                or "not a bot" in error_message
                or "cookies" in error_message
                or "http error 403" in error_message
            ):

                st.error(
                    "⚠️ YouTube couldn't process this video."
                )

                st.info(
                    "YouTube is blocking this video from being "
                    "downloaded from the current environment.\n\n"
                    "Please download the video/audio and use "
                    "**Upload Recording** instead."
                )

            else:

                st.error(
                    f"❌ Processing failed: {e}"
                )


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

if st.session_state.result:

    result = st.session_state.result

    st.markdown("---")

    st.markdown(
        f"# 🎯 {result['title']}"
    )

    st.caption(
        "AI-generated insights from your recording"
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📋 Summary",
            "✅ Action Items",
            "🎯 Decisions",
            "❓ Questions",
        ]
    )

    with tab1:

        st.markdown("### Meeting Summary")
        st.markdown(result["summary"])


    with tab2:

        st.markdown("### Action Items")
        st.markdown(result["action_items"])


    with tab3:

        st.markdown("### Key Decisions")
        st.markdown(result["decisions"])


    with tab4:

        st.markdown("### Open Questions")
        st.markdown(result["questions"])


# --------------------------------------------------
# ASK VOXERA
# --------------------------------------------------

with st.popover("💬 Ask Voxera"):

    st.markdown("### 💬 Ask Voxera")

    if st.session_state.rag_chain:

        st.caption(
            "Ask anything about your analyzed recording."
        )

        question = st.text_input(
            "Your question",
            placeholder="What were the key decisions?",
            key="voxera_question",
        )

        if st.button(
            "Ask Voxera",
            key="ask_voxera"
        ):

            if question.strip():

                with st.spinner("Voxera is thinking..."):

                    answer = ask_question(
                        st.session_state.rag_chain,
                        question
                    )

                st.markdown("### 🤖 Voxera")
                st.write(answer)

            else:

                st.warning(
                    "Please enter a question."
                )

    else:

        st.info(
            "Analyze a recording first to activate Ask Voxera."
        )