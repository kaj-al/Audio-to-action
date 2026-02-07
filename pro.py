import streamlit as st 
from pydub import AudioSegment
import whisper
import os
from datetime import datetime
from streamlit_mic_recorder import mic_recorder

st.title("AUDIO TO ACTION")
st.write("Record your voice note and convert it into actions.")
st.subheader("RECORD VOICE")
model = whisper.load_model("base")
if "history" not in st.session_state:
    st.session_state.history = []
audio = mic_recorder(start_prompt="Start recording",stop_prompt="Stop recording",just_once=True)
if audio:
    with open("temp_audio.webm","wb") as f:
        f.write(audio["bytes"])
        sound = AudioSegment.from_file("temp_audio.webm")
        sound.export("temp_audio.wav",format="wav")

        result = model.transcribe("temp_audio.wav")
        st.subheader("recognised text")
        st.write(result["text"])

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.history.append(f"{timestamp} - {result["text"]}")
    with open("transcription.txt","a",encoding="utf-8") as f:
        f.write(f"{timestamp} - {result["text"]}\n")
    st.subheader("Voice notes history")
    for text in reversed(st.session_state.history):
        st.write(text)

    def intent(text):
        text = text.lower()
        if "remind" in text or "reminder" in text:
            return "Reminder"
        elif "buy" in text or "purchase" in text:
            return "Task"
        elif "open" in text or "search" in text:
            return "Open Tab"
        elif "idea" in text or "note" in text:
            return "Idea"
        else:
            return "General Note"

    intent = intent(text)
    st.subheader("Detected intent")
    st.write(intent)


