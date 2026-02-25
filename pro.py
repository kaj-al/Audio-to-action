import streamlit as st 
from pydub import AudioSegment
import whisper
from intent_detection import intent
from datetime import datetime
from data_auto import automate,data
from streamlit_mic_recorder import mic_recorder

st.title("AUDIO TO ACTION")
st.write("Record your voice note and convert it into actions.")
st.subheader("RECORD VOICE")

@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

if "history" not in st.session_state:
    st.session_state.history = []
if "text" not in st.session_state:
    st.session_state.text = ""
if "intent" not in st.session_state:
    st.session_state.intent= ""

# recording
audio = mic_recorder(start_prompt="Start recording",stop_prompt="Stop recording",just_once=True)
if audio:
    with open("temp_audio.webm","wb") as f:
        f.write(audio["bytes"])
        sound = AudioSegment.from_file("temp_audio.webm")
        sound.export("temp_audio.wav",format="wav")
        result = model.transcribe("temp_audio.wav")
        st.session_state.text = result["text"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.history.append(f"{timestamp} - {result['text']}")

# detection
if st.session_state.text:
    st.subheader("Text")
    st.write(st.session_state.text)
    if st.button("Detect intent"):
        with st.spinner("Detecting.."):
            output = intent(st.session_state.text)
            st.session_state.intent = output 
            automate(output)

if st.session_state.intent:
    st.subheader("Intent")
    st.json(st.session_state.intent)

# dashboard
st.markdown("## Dashboard Overview")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Tasks")
    for t in data["tasks"]:
        st.write(f"• {t.get('task')} | Priority: {t.get('priority')} | Date: {t.get('date')} {t.get('time')}")

with col2:
    st.markdown("### Reminders & Events")
    for r in  data["events"]:
        st.write(f"• {r.get('task')} | Date: {r.get('date')} {r.get('time')}")

with col3:
    st.markdown("### Notes / Shopping")
    for n in data["notes"]:
        st.write(f"• {n.get('task')}")

# history
if st.session_state.history:
    st.subheader("History")
    for item in reversed(st.session_state.history):
        st.write(item)     


    
