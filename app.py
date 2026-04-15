import streamlit as st
import os
import json
from faster_whisper import WhisperModel
import ollama

# --- 1. CONFIGURATION & SAFETY ---
# Restriction: All file operations are saved in the dedicated output/ folder [cite: 26]
OUTPUT_DIR = "output"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- 2. PIPELINE FUNCTIONS ---

def transcribe_audio(audio_path):
    """Converts audio to text using a local Whisper model[cite: 13]."""
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_path)
    return " ".join([segment.text for segment in segments])

def get_intent_analysis(text):
    """Analyzes text to classify intent using Llama 3.2 1B[cite: 17]."""
    prompt = f"""
    Analyze the user input and return ONLY a JSON object with:
    'intent': (CREATE_FILE, WRITE_CODE, SUMMARIZE, CHAT)
    'filename': (suggested filename with extension)
    'content': (the code or text to process)
    'response': (a short status message)
    
    Input: "{text}"
    """
    response = ollama.generate(model='llama3.2:1b', prompt=prompt, format='json')
    return json.loads(response['response'])

# --- 3. STREAMLIT USER INTERFACE ---

st.set_page_config(page_title="Voice AI Agent", layout="wide")

# Main Header - Updated as requested
st.title("Voice AI Agent") 
process_btn = st.button("Process Audio", type="primary")

# Sidebar for audio input [cite: 7, 8, 9]
with st.sidebar:
    st.header("Audio Input")
    audio_mic = st.audio_input("Record Command")
    audio_file = st.file_uploader("Upload Audio File", type=["wav", "mp3"])

input_source = audio_mic if audio_mic else audio_file

if input_source and process_btn:
    temp_path = "temp_audio.wav"
    with open(temp_path, "wb") as f:
        f.write(input_source.read())

    # --- Step 1: Transcription [cite: 11, 32] ---
    st.subheader("📝 Transcribed Text")
    transcription = transcribe_audio(temp_path)
    st.info(f"**Your audio was transcribed as:**\n\n{transcription}")

    # --- Step 2: Intent Understanding [cite: 33] ---
    st.subheader("🎯 Detected Intent")
    analysis = get_intent_analysis(transcription)
    
    # Modern Badge UI for Intent and Filename
    c1, c2 = st.columns(2)
    with c1:
        st.success(f"**Intent:** {analysis.get('intent')}")
    with c2:
        st.info(f"**File:** {analysis.get('filename', 'N/A')}")

    # Expandable JSON Data
    with st.expander("📂 Full Intent Data (JSON)", expanded=True):
        st.code(json.dumps(analysis, indent=4), language="json")

    # --- Step 3: Tool Execution [cite: 24, 34, 35] ---
    st.subheader("⚙️ Executing Action")
    
    with st.expander("✅ Action Result", expanded=True):
        intent = str(analysis.get("intent", "")).lower()
        filename = analysis.get("filename", "output.txt")
        content = analysis.get("content", "")
        file_path = os.path.join(OUTPUT_DIR, filename)

        # File Operations [cite: 19, 20, 25, 27]
        if "file" in intent or "code" in intent:
            with open(file_path, "w") as f:
                f.write(content)
            st.success(f"**File created:** {filename} ({os.path.getsize(file_path)} bytes)")
            st.code(f"Saved at: {file_path}")
        
        # Text Processing [cite: 21, 28]
        elif "summarize" in intent:
            summary = ollama.generate(model='llama3.2:1b', prompt=f"Summarize this: {content}")['response']
            st.write(f"**Summary Result:** {summary}")
        
        # General Chat [cite: 22]
        else:
            st.write(analysis.get("response", "Conversation processed."))

    # --- Step 4: System Result / Contents  ---
    st.subheader("📁 Output Folder Contents")
    files = os.listdir(OUTPUT_DIR)
    if files:
        for i, f in enumerate(files, 1):
            st.write(f"{i}. {f}")
            
elif not input_source and process_btn:
    st.warning("Please record or upload audio first.")