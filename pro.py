import streamlit as st 
from streamlit_mic_recorder import mic_recorder

st.title("AUDIO TO ACTION")
st.write("Record your voice note and convert it into actions.")
st.subheader("RECORD VOICE")
audio = mic_recorder(start_prompt="Start recording",stop_prompt="Stop recording",just_once=True)
if audio:
    st.success("recording successful")
    st.audio(audio["bytes"],format="audio\wav")
    with open("recorded.wav","wb") as f:
        f.write(audio["bytes"])
    st.write("Audio saved")

