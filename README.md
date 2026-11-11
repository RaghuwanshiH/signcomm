### 🚀 Live App - Click Here To Open 👇
### https://signcomm.streamlit.app

---
# 🤟 SignComm : Dual-Mode Sign Language Assistant (ISL & ASL)
**Final Year Capstone Project Demonstration**

A 100% functional, bilingual Sign Language translation web application developed using **Python Streamlit**, **FFmpeg**, **Google gTTS**, and the **Web Speech API**.

---

## 🌟 Key Features

### 1. 🔊 Tab 1: Sign to Voice (Click ➔ Speech)
- **10 Core Vocabulary Cards:** `Hello`, `Thank You`, `Yes`, `No`, `Help`, `Water`, `Food`, `Please`, `Name`, `How are you`.
- **Instant Dual-Layer Text-to-Speech (TTS):**
  - **Browser Native Speech:** Zero-latency speech synthesis via HTML5 Web Speech API (`SpeechSynthesisUtterance`).
  - **Secondary Audio Stream:** High-fidelity pre-rendered `.mp3` audio files served via `st.audio` for 100% offline and cross-browser reliability.
- **Anatomical Sign Guide:** Detailed breakdown of handshape, motion vector, and execution tips for each sign.
- **Communication Pad (Sentence Builder):** Click the `➕` button on any card to assemble complex sentences (e.g., *"Hello Help Water Please"*) with one-click **"🗣️ Speak Sentence"** and **"🧹 Clear Pad"** controls.

### 2. 🎥 Tab 2: Voice to Sign (Type / Speak ➔ Sign Video)
- **Word Typing with Smart Matching:** Type any word or synonym (e.g., *"thanks"*, *"hi"*, *"drink"*, *"food"*) to immediately locate and display its sign video.
- **Quick Selection Chips:** 1-click test chips for rapid demonstrations to evaluators.
- **Live Microphone Dictation:** Integrated HTML5 Web Speech recognition widget to dictate speech directly from your microphone into the sign video player.
- **High-Definition Video Player:** Auto-looping 720p H.264 MP4 videos showing precise gesture motion and execution cues.
- **Comparative Sign View:** Expandable comparison viewer to see how the gesture differs between Indian Sign Language (ISL) and American Sign Language (ASL).

### 3. 🇮🇳 Dual-Mode Language Architecture
- **Default:** **Indian Sign Language (ISL)** optimized for Indian deaf education curricula and regional signs (e.g., *Namaste*, *Shukriya*, *Madad*, *Paani*).
- **Switch:** **American Sign Language (ASL)** accessible via the sidebar standard toggle.

---

## 📂 Project Structure

```text
c:\Users\Lenovo\Downloads\SL-app/
├── app.py                  # Main Streamlit web application
├── generate_assets.py      # Video and TTS generation script
├── download_assets.py      # Asset verification and conversion utility
├── README.md               # Project documentation
└── assets/
    ├── isl/                # 10 ISL animated gesture MP4 videos
    │   ├── hello.mp4
    │   ├── thank_you.mp4
    │   ├── yes.mp4
    │   ├── no.mp4
    │   ├── help.mp4
    │   ├── water.mp4
    │   ├── food.mp4
    │   ├── please.mp4
    │   ├── name.mp4
    │   └── how_are_you.mp4
    ├── asl/                # 10 ASL animated gesture MP4 videos
    │   ├── hello.mp4
    │   ...
    │   └── how_are_you.mp4
    └── audio/              # 10 gTTS generated speech MP3 files
        ├── hello.mp3
        ...
        └── how_are_you.mp3
```

---

## 🚀 How to Run the App

1. Open PowerShell / Command Prompt in the project folder:
   ```powershell
   cd c:\Users\Lenovo\Downloads\SL-app
   ```

2. Start the Streamlit application:
   ```powershell
   python -m streamlit run app.py
   ```

3. Open your browser at:
   ```text
   http://localhost:8501
   ```
