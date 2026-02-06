import streamlit as st 
from pydub import AudioSegment
import whisper
import os
import tempfile
from streamlit_mic_recorder import mic_recorder

st.title("AUDIO TO ACTION")
st.write("Record your voice note and convert it into actions.")
st.subheader("RECORD VOICE")
model = whisper.load_model("base")
audio = mic_recorder(start_prompt="Start recording",stop_prompt="Stop recording",just_once=True)
if audio:
    with open("temp_audio.webm","wb") as f:
        f.write(audio["bytes"])
        sound = AudioSegment.from_file("temp_audio.webm")
        sound.export("temp_audio.wav",format="wav")

        result = model.transcribe("temp_audio.wav")
        st.subheader("recognised text")
        st.write(result["text"])


