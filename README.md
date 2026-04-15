# 🎙️ Voice-Controlled Local AI Agent

[cite_start]A local AI agent built for the Mem0 Developer Intern Assignment[cite: 1, 2]. [cite_start]This agent accepts audio input via microphone or file upload, transcribes it, classifies user intent using a Large Language Model, and executes local system tools[cite: 4].

## 🚀 Features
- [cite_start]**Dual Audio Input**: Supports direct microphone recording and `.wav`/`.mp3` file uploads[cite: 7, 8, 9].
- [cite_start]**Local STT**: Powered by the `Faster-Whisper` model for high-efficiency transcription[cite: 10, 13].
- [cite_start]**Intent Understanding**: Uses `Ollama` with `Llama 3.2 1B` to classify intents: Create File, Write Code, Summarize, and General Chat[cite: 16, 17, 18].
- [cite_start]**Automated Tool Execution**: Automatically creates files or processes text based on voice commands[cite: 23, 24].
- [cite_start]**Safety First**: All file operations are strictly restricted to a dedicated `output/` folder.

## 🏗️ Architecture
The system follows a 4-step pipeline:
1. [cite_start]**Audio Capture**: Streamlit frontend handles microphone or file input[cite: 30, 31].
2. [cite_start]**Transcription**: Faster-Whisper converts audio bytes into text[cite: 11].
3. [cite_start]**Intent Mapping**: The text is sent to a local LLM which returns a structured JSON object containing the intent, filename, and content[cite: 17, 33].
4. [cite_start]**Tool Execution**: Python's `os` library executes the requested action (e.g., file creation)[cite: 24, 34].

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.9+
- [Ollama](https://ollama.com/) installed and running.

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure Ollama is running**
   ```bash
   # In a separate terminal, start Ollama server
   ollama serve
   ```

5. **Pull the phi3:mini model (first time only)**
   ```bash
   ollama pull phi3:mini
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

7. **Open in browser**
   ```
   http://localhost:8501
   ```

   ### Components

| Component | Technology | Mode | Purpose |
|-----------|-----------|------|---------|
| **UI** | Streamlit | Web | Real-time user interface |
| **Audio Input** | sounddevice + scipy | Local | Microphone recording |
| **Audio Processing** | pydub + ffmpeg | Local | Format conversion |
| **Speech-to-Text** | faster-whisper | CPU | Audio transcription |
| **Intent Detection** | Ollama + phi3:mini | CPU | LLM-based classification |
| **File Operations** | Python pathlib | Local | Safe file management |

##  Why CPU Mode for Ollama?

The phi3:mini model runs on **CPU mode** due to a compatibility issue with Ollama's GPU runner on certain systems.

### Issue Encountered
```
ERROR: llama runner process has terminated unexpectedly
```

### Solution Applied
```python
options={"num_gpu_layers": 0}  # Force CPU computation
```

### Why This Works
- **phi3:mini** is a tiny 3.8B parameter model
- **Int8 quantization** reduces memory footprint significantly
- CPU execution is **deterministic and reliable**
- Trade-off: ~0.5-1 second slower per inference (acceptable for voice agent)

### Performance (Measured on Intel i3 7020U)
- Transcription (5s audio): ~2-3 seconds
- Intent detection: ~1-2 seconds
- Total pipeline: ~3-5 seconds

##  Security Features

1. **Path Sanitization**
   - Filenames validated against regex: `^[a-zA-Z0-9._\-]+$`
   - No directory traversal (`..`, `/` prefixes blocked)
   - All operations verified to be within `./output/`

2. **Input Validation**
   - Max filename length: 100 characters
   - Max content length: 50,000 characters
   - Audio file size checks

3. **Error Handling**
   - No broad exception catching; specific error types handled
   - Detailed logging for audit trails
   - Graceful fallbacks for all failure modes

4. **Human Oversight**
   - Confirmation dialog before file create/write operations
   - Full JSON intent display for transparency
   - File size display in output folder
##  Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'ollama'"
**Solution:**
```bash
pip install ollama
```

### Issue: "Ollama connection refused"
**Solution:** Ensure Ollama is running in a separate terminal:
```bash
ollama serve
```

### Issue: "No module named 'faster_whisper'"
**Solution:**
```bash
pip install faster-whisper
```

### Issue: "ffmpeg not found"
**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
choco install ffmpeg
```

### Issue: Recording produces empty/silent output
**Solution:**
- Check microphone permissions
- Verify `sounddevice` can access audio: `python -m sounddevice`
- Increase recording duration in code

### Issue: Transcription returns empty text
**Solution:**
- Ensure audio is clear (minimal background noise)
- Speak clearly and at normal pace
- Try uploading a .wav file of better quality

##  Performance Optimization

For improved speed on slower machines:
1. Use `device="cuda"` in `load_whisper_model()` (requires NVIDIA GPU + CUDA)
2. Switch to `faster-whisper` tiny model: `WhisperModel("tiny")`
3. Increase `num_gpu_layers` in Ollama options (if using GPU)

##  Learning Outcomes

This project demonstrates:
-  Local LLM inference with Ollama
-  Speech recognition with faster-whisper
-  Intent classification and NLP
-  Real-time streaming UI with Streamlit
-  Security best practices (path sanitization, input validation)
-  Error handling and logging
-  State management in web applications
-  Hardware-aware optimization (CPU mode for compatibility)

##  Project Structure

```
voice-ai-agent/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── output/                # Safe directory for file operations
    ├── test.txt
    ├── script.py
    └── ...
```

##  Future Enhancements

- [ ] Support for compound commands ("Create a file AND write code to it")
- [ ] Multi-language support (Spanish, French, etc.)
- [ ] Voice output (text-to-speech feedback)
- [ ] Command history and favorites
- [ ] Integration with local vector database for memory/context
- [ ] Web API for remote access (with authentication)
- [ ] Docker containerization for easy deployment

##  License

This project is part of the Mem0 AI &  Internship Assigment.