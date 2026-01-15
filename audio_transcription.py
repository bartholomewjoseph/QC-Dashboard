import streamlit as st
import openai

def render_audio_page():
    st.title("🎧 Audio Transcription")
    st.info("Accepted formats: WAV, MP3, M4A, AMR")

    openai_key = st.secrets.get("OPENAI_API_KEY", None)
    if not openai_key:
        st.error("OpenAI API key not found. Add it to .streamlit/secrets.toml")
        return

    client = openai

    audio_file = st.file_uploader("Upload audio file", type=["wav", "mp3", "m4a", "amr"])
    if audio_file:
        st.audio(audio_file)
        if st.button("Transcribe Audio"):
            with st.spinner("Transcribing..."):
                try:
                    transcript = client.Audio.transcriptions.create(file=audio_file, model="whisper-1")
                    st.text_area("Transcript", transcript["text"], height=300)
                except Exception as e:
                    st.error(e)
