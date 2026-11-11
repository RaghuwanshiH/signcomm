"""
Sign Language Assistant - Dual Mode (ISL & ASL)
Final Year Project Demonstration Application
Features:
- Sign to Voice (Interactive cards, Web Speech API & local gTTS text-to-speech, sentence pad)
- Voice to Sign (Typing search, live voice recognition via Web Speech, HD video player, ISL/ASL switch)
"""

import os
import base64
import streamlit as st
import streamlit.components.v1 as components

# ================= PAGE CONFIGURATION =================
st.set_page_config(
    page_title="SignComm | Dual-Mode Sign Language System",
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= PATHS & ASSETS =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
ISL_DIR = os.path.join(ASSETS_DIR, "isl")
ASL_DIR = os.path.join(ASSETS_DIR, "asl")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")

# ================= VOCABULARY DATA =================
WORDS_DATABASE = {
    "Hello": {
        "slug": "hello",
        "category": "Greetings",
        "emoji": "👋",
        "synonyms": ["hi", "hey", "namaste", "greetings", "hello"],
        "isl": {
            "name": "Namaste / Hello",
            "gesture": "Open flat palm raised to temple, moving smoothly outward with a slight bow or joining palms in Namaste.",
            "handshape": "Open B-palm or Anjali Mudra (folded hands)",
            "motion": "Forehead outward wave or chest palm press",
            "tip": "Maintain warm eye contact and a gentle affirming head tilt."
        },
        "asl": {
            "name": "Hello",
            "gesture": "Dominant B-hand starts near the forehead/temple and moves crisp and forward like an open salute.",
            "handshape": "B-hand (fingers flat together, thumb alongside)",
            "motion": "Forward temple salute",
            "tip": "Extend hand smoothly outward from temple at an angle."
        }
    },
    "Thank You": {
        "slug": "thank_you",
        "category": "Politeness",
        "emoji": "🙏",
        "synonyms": ["thanks", "thank you", "thankyou", "shukriya", "dhanyawad"],
        "isl": {
            "name": "Thank You / Shukriya",
            "gesture": "Flat fingers touch chin and lips, moving forward and slightly down towards the conversational partner.",
            "handshape": "Flat open palm, fingers together",
            "motion": "Lips outward projection",
            "tip": "Accompany with a pleasant smile acknowledging the listener."
        },
        "asl": {
            "name": "Thank You",
            "gesture": "Fingertips of dominant hand touch the chin/lips, then extend outward and slightly upward toward the listener.",
            "handshape": "Flat B-hand with palm facing inwards, then facing upward",
            "motion": "Chin to forward trajectory",
            "tip": "Ensure hand moves outward towards the person being thanked."
        }
    },
    "Yes": {
        "slug": "yes",
        "category": "Affirmation",
        "emoji": "👍",
        "synonyms": ["yes", "yeah", "yep", "haan", "correct", "agree"],
        "isl": {
            "name": "Yes / Haan",
            "gesture": "Right hand formed into a relaxed fist with wrist nodding up and down twice, mimicking an affirmative head nod.",
            "handshape": "Closed fist (S-hand)",
            "motion": "Vertical wrist nodding",
            "tip": "Synchronize with a slight physical head nod for clarity."
        },
        "asl": {
            "name": "Yes",
            "gesture": "Dominant hand forms an 'S' handshape (fist) and bends forward at the wrist repeatedly like a nodding head.",
            "handshape": "S-fist",
            "motion": "Repetitive wrist flexing downward",
            "tip": "Motion resembles a miniature person nodding yes."
        }
    },
    "No": {
        "slug": "no",
        "category": "Affirmation",
        "emoji": "🚫",
        "synonyms": ["no", "nah", "nope", "nahi", "negative", "never"],
        "isl": {
            "name": "No / Nahi",
            "gesture": "Index and middle fingers extend and tap closed against the thumb, or index finger shakes laterally side-to-side.",
            "handshape": "Two fingers meeting thumb or single index pointer",
            "motion": "Lateral shake or snapping closure",
            "tip": "Give a slight head shake left-to-right concurrently."
        },
        "asl": {
            "name": "No",
            "gesture": "Index and middle fingers extended together snap down to touch the tip of the extended thumb.",
            "handshape": "N/3 modified pinch",
            "motion": "Quick snapping clasp",
            "tip": "Snapping action is quick and decisive."
        }
    },
    "Help": {
        "slug": "help",
        "category": "Urgent Needs",
        "emoji": "🆘",
        "synonyms": ["help", "assist", "assistance", "madad", "support"],
        "isl": {
            "name": "Help / Madad",
            "gesture": "Right fist with extended thumb is placed directly on the open flat palm of the non-dominant hand; both rise upward.",
            "handshape": "Dominant fist over flat horizontal palm",
            "motion": "Vertical upward elevation",
            "tip": "Move hands toward the person who needs help (directional sign)."
        },
        "asl": {
            "name": "Help",
            "gesture": "Closed A-hand with thumb up rests upon the flat upward-facing palm of the non-dominant hand; both elevate together.",
            "handshape": "A-hand supported by flat B-hand",
            "motion": "Upward lift toward chest level",
            "tip": "Can be directional: move toward yourself for 'help me' or forward for 'help you'."
        }
    },
    "Water": {
        "slug": "water",
        "category": "Daily Needs",
        "emoji": "💧",
        "synonyms": ["water", "drink", "paani", "aqua", "hydrate"],
        "isl": {
            "name": "Water / Paani",
            "gesture": "Curved fingers form a cup or tilted glass shape, brought up near the mouth simulating taking a sip.",
            "handshape": "C-cup or tilted fist near mouth",
            "motion": "Tilting toward lips",
            "tip": "A universal intuitive gesture recognized widely in Indian Sign."
        },
        "asl": {
            "name": "Water",
            "gesture": "Dominant hand forms the 'W' handshape (index, middle, ring finger extended), and the side of the index taps the chin twice.",
            "handshape": "W-handshape",
            "motion": "Double tap against center chin",
            "tip": "Keep fingers comfortably spaced and upright."
        }
    },
    "Food": {
        "slug": "food",
        "category": "Daily Needs",
        "emoji": "🍲",
        "synonyms": ["food", "eat", "eating", "khana", "lunch", "dinner", "meal", "hungry"],
        "isl": {
            "name": "Food / Khana",
            "gesture": "Bunched fingertips of dominant hand (all fingers joined touching thumb) touch the mouth/lips repeatedly.",
            "handshape": "Flattened O-hand / bunched fingertips",
            "motion": "Gentle double tap to lips",
            "tip": "Natural dining motion indicating food or desire to eat."
        },
        "asl": {
            "name": "Food / Eat",
            "gesture": "Fingertips together touching the thumb (flat O-hand) tap against the lips 2 to 3 times for food, once for eat.",
            "handshape": "Squashed O-handshape",
            "motion": "Repetitive tap to lips",
            "tip": "A single motion denotes 'eat'; double motion denotes 'food'."
        }
    },
    "Please": {
        "slug": "please",
        "category": "Politeness",
        "emoji": "🤲",
        "synonyms": ["please", "pls", "plz", "kripya", "request"],
        "isl": {
            "name": "Please / Kripya",
            "gesture": "Both hands joined gently in front of chest in Namaste, or flat palm softly rubs center of chest in a circular path.",
            "handshape": "Joined open hands or flat chest palm",
            "motion": "Circular chest movement or folded palms",
            "tip": "Express gentle facial sincerity."
        },
        "asl": {
            "name": "Please",
            "gesture": "Flat open hand with fingers together rubs the center of the chest in a smooth clockwise circular movement.",
            "handshape": "Flat B-palm facing body",
            "motion": "Clockwise chest circular rub",
            "tip": "Keep palm in gentle contact with chest."
        }
    },
    "Name": {
        "slug": "name",
        "category": "Identity",
        "emoji": "🏷️",
        "synonyms": ["name", "naam", "called", "identity"],
        "isl": {
            "name": "Name / Naam",
            "gesture": "Index and middle fingers of right hand extend and tap crosswise over the matching fingers of the left hand twice.",
            "handshape": "H-handshapes on both hands",
            "motion": "Crosswise dual finger tap",
            "tip": "Ensure both hands are parallel at mid-chest level."
        },
        "asl": {
            "name": "Name",
            "gesture": "Both hands form 'H' shapes (index and middle fingers extended); dominant hand taps across the non-dominant hand twice at right angles.",
            "handshape": "Double H-handshape",
            "motion": "Double downward tap across fingers",
            "tip": "Fingers cross like an 'X' during the tap."
        }
    },
    "How are you": {
        "slug": "how_are_you",
        "category": "Greetings",
        "emoji": "❓",
        "synonyms": ["how are you", "how are u", "how r u", "how are you?", "kaise ho", "kya haal hai", "whats up"],
        "isl": {
            "name": "How are you? / Kaise ho?",
            "gesture": "Both hands held open with palms facing upward, curving inward and rolling outward accompanied by a questioning facial expression.",
            "handshape": "Open curved palms",
            "motion": "Outward roll & presentation",
            "tip": "Raise eyebrows slightly to denote a question."
        },
        "asl": {
            "name": "How are you?",
            "gesture": "Curved hands roll upward and outward into thumbs-up gesture (HOW), followed by dominant index finger pointing toward partner (YOU).",
            "handshape": "Curved hands moving to open point",
            "motion": "Roll upward + forward point",
            "tip": "Tilt head slightly forward with furrowed brows for WH-questions."
        }
    }
}

# ================= CUSTOM CSS STYLING =================
def inject_custom_css():
    st.markdown("""
    <style>
        /* Import clean Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Modern Gradient Header Banner */
        .project-banner {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f766e 100%);
            border-radius: 16px;
            padding: 24px 30px;
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.12);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
            margin-bottom: 24px;
        }
        
        .badge-pill {
            display: inline-block;
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(8px);
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-right: 8px;
        }

        .badge-isl {
            background: linear-gradient(90deg, #f97316 0%, #ea580c 100%);
            color: white;
            font-weight: 700;
        }

        .badge-asl {
            background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            font-weight: 700;
        }
        
        /* Interactive Cards */
        .word-card {
            background: #1e293b;
            border-radius: 14px;
            padding: 18px 20px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            transition: all 0.25s ease-in-out;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        .word-card:hover {
            transform: translateY(-3px);
            border-color: #38bdf8;
            box-shadow: 0 12px 20px -8px rgba(56, 189, 248, 0.25);
        }
        
        .audio-wave-box {
            background: linear-gradient(90deg, #0f172a, #1e293b);
            border: 1px solid #38bdf8;
            border-radius: 12px;
            padding: 16px;
            margin: 15px 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .sentence-pad {
            background: #0f172a;
            border: 1px dashed #64748b;
            border-radius: 12px;
            padding: 14px 18px;
            min-height: 54px;
            font-size: 1.1rem;
            font-weight: 600;
            color: #38bdf8;
            letter-spacing: 0.02em;
        }
        
        /* Video Container Styling */
        .video-box-card {
            background: #0f172a;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px;
            box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
        }

        .guide-step {
            background: rgba(255, 255, 255, 0.04);
            border-left: 3px solid #38bdf8;
            padding: 10px 14px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 8px;
            font-size: 0.92rem;
        }
        
        /* Tabs design */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 48px;
            background-color: rgba(30, 41, 59, 0.7);
            border-radius: 10px;
            padding: 0 24px;
            font-weight: 600;
            font-size: 0.95rem;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .stTabs [aria-selected="true"] {
            background-color: #0284c7 !important;
            color: white !important;
            border-color: #38bdf8 !important;
        }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ================= SESSION STATE INITIALIZATION =================
if "lang_mode" not in st.session_state:
    st.session_state.lang_mode = "ISL"  # Default to ISL for India as requested

if "active_speaking_word" not in st.session_state:
    st.session_state.active_speaking_word = None

if "sentence_tokens" not in st.session_state:
    st.session_state.sentence_tokens = []

if "selected_query_word" not in st.session_state:
    st.session_state.selected_query_word = "Hello"

if "trigger_speech_text" not in st.session_state:
    st.session_state.trigger_speech_text = None

# ================= HELPER FUNCTIONS =================
def speak_in_browser(text_to_speak):
    """Executes client-side Web Speech API utterance for instant, zero-latency speech."""
    escaped_text = text_to_speak.replace('"', '\\"').replace("'", "\\'")
    js_code = f"""
    <script>
        (function() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance("{escaped_text}");
                utterance.rate = 1.0;
                utterance.pitch = 1.0;
                utterance.lang = 'en-US';
                window.speechSynthesis.speak(utterance);
            }}
        }})();
    </script>
    """
    components.html(js_code, height=0, width=0)

def get_base64_video(file_path):
    """Loads local mp4 video into base64 data uri for clean autoplaying HTML5 video."""
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("utf-8")
    return None

def normalize_input(query):
    """Matches typed queries or speech transcripts against the 10 target words."""
    if not query:
        return None
    cleaned = query.strip().lower().replace("?", "").replace("!", "").replace(".", "")
    
    # 1. Direct match with words
    for word in WORDS_DATABASE.keys():
        if cleaned == word.lower():
            return word

    # 2. Match with synonyms
    for word, data in WORDS_DATABASE.items():
        for syn in data["synonyms"]:
            if syn in cleaned or cleaned in syn:
                return word

    # 3. Partial substring match
    for word in WORDS_DATABASE.keys():
        if word.lower() in cleaned:
            return word

    return None

# ================= SIDEBAR & NAVIGATION =================
with st.sidebar:
    st.markdown("### ⚙️ System Controls")
    
    # Mode Switch: ISL vs ASL
    st.markdown("**Select Sign Language Standard:**")
    mode_selection = st.radio(
        label="Sign Language Standard",
        options=["Indian Sign Language (ISL) 🇮🇳", "American Sign Language (ASL) 🇺🇸"],
        index=0 if st.session_state.lang_mode == "ISL" else 1,
        label_visibility="collapsed"
    )
    new_mode = "ISL" if "ISL" in mode_selection else "ASL"
    if new_mode != st.session_state.lang_mode:
        st.session_state.lang_mode = new_mode
        st.rerun()

    st.markdown("---")
    
    # Speech Engine Preferences
    st.markdown("### 🔊 Text-To-Speech Options")
    speech_rate = st.slider("Speech Speed Rate", min_value=0.75, max_value=1.5, value=1.0, step=0.25)
    auto_speak_card = st.checkbox("Auto-speak on word click", value=True)
    dual_audio_stream = st.checkbox("Enable Secondary Stream Player", value=True)

    st.markdown("---")
    
    # Project Diagnostics
    st.markdown("### 📋 Capstone Project Info")
    st.markdown("""
    - **Project:** Dual-Mode Interactive Sign Communication System
    - **Language Standards:** ISL (Default) & ASL
    - **Target Vocabulary:** 10 Core Survival & Conversational Words
    - **Engines:** Streamlit, gTTS, Web Speech API, FFmpeg H.264
    """)

    # Asset integrity counter
    isl_count = sum(1 for w in WORDS_DATABASE.values() if os.path.exists(os.path.join(ISL_DIR, f"{w['slug']}.mp4")))
    asl_count = sum(1 for w in WORDS_DATABASE.values() if os.path.exists(os.path.join(ASL_DIR, f"{w['slug']}.mp4")))
    audio_count = sum(1 for w in WORDS_DATABASE.values() if os.path.exists(os.path.join(AUDIO_DIR, f"{w['slug']}.mp3")))
    
    st.caption(f"✅ Assets Loaded: ISL ({isl_count}/10) | ASL ({asl_count}/10) | Audio ({audio_count}/10)")
    
    st.markdown("---")
    if st.button("🔄 Reset / Clear Session", use_container_width=True):
        st.session_state.active_speaking_word = None
        st.session_state.sentence_tokens = []
        st.session_state.selected_query_word = "Hello"
        st.session_state.trigger_speech_text = None
        st.rerun()

# ================= TOP HERO BANNER =================
current_lang_badge = "badge-isl" if st.session_state.lang_mode == "ISL" else "badge-asl"
current_lang_name = "Indian Sign Language (ISL)" if st.session_state.lang_mode == "ISL" else "American Sign Language (ASL)"
flag_icon = "🇮🇳" if st.session_state.lang_mode == "ISL" else "🇺🇸"

st.markdown(f"""
<div class="project-banner">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px;">
        <div>
            <div style="margin-bottom: 10px;">
                <span class="badge-pill">Final Year Project Demo</span>
                <span class="badge-pill {current_lang_badge}">Active: {current_lang_name} {flag_icon}</span>
                <span class="badge-pill">10-Word Vocabulary</span>
            </div>
            <h1 style="margin: 0; font-size: 2.1rem; font-weight: 800; color: #ffffff;">
                🤟 SignComm : Bilingual Sign Language Bridge
            </h1>
            <p style="margin: 8px 0 0 0; color: #cbd5e1; font-size: 1.02rem;">
                Bridging communication between the hearing community and the deaf/hard-of-hearing with real-time bidirectional translation.
            </p>
        </div>
        <div style="text-align: right; background: rgba(0,0,0,0.25); padding: 12px 18px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
            <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 600;">ACTIVE STANDARD</div>
            <div style="font-size: 1.3rem; font-weight: 800; color: #38bdf8;">{st.session_state.lang_mode} MODE</div>
            <div style="font-size: 0.75rem; color: #a5f3fc;">Switch anytime from sidebar</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Client-side audio trigger handler if queued
if st.session_state.trigger_speech_text:
    speak_in_browser(st.session_state.trigger_speech_text)
    st.session_state.trigger_speech_text = None

# ================= MAIN APPLICATION TABS =================
tab_sign_to_voice, tab_voice_to_sign = st.tabs([
    "🔊 Tab 1 : Sign to Voice (Click ➔ Speech)",
    "🎥 Tab 2 : Voice to Sign (Type ➔ Sign Video)"
])

# =========================================================
# TAB 1: SIGN TO VOICE
# =========================================================
with tab_sign_to_voice:
    st.markdown("### 🔊 Sign to Voice Translation")
    st.markdown("Click any sign card below to **speak the word out loud via Text-to-Speech (TTS)** and view its anatomical gesture breakdown.")

    # Sentence Builder Pad
    st.markdown("#### 📝 Live Communication Pad (Sentence Builder)")
    pad_col1, pad_col2, pad_col3 = st.columns([4, 1, 1])
    
    with pad_col1:
        sentence_str = " ".join(st.session_state.sentence_tokens) if st.session_state.sentence_tokens else "Click words below to assemble a sentence..."
        st.markdown(f'<div class="sentence-pad">{sentence_str}</div>', unsafe_allow_html=True)

    with pad_col2:
        if st.button("🗣️ Speak Sentence", use_container_width=True, disabled=len(st.session_state.sentence_tokens) == 0):
            full_text = " ".join(st.session_state.sentence_tokens)
            st.session_state.trigger_speech_text = full_text
            st.rerun()

    with pad_col3:
        if st.button("🧹 Clear Pad", use_container_width=True, disabled=len(st.session_state.sentence_tokens) == 0):
            st.session_state.sentence_tokens = []
            st.rerun()

    st.markdown("---")

    # Display Active Speaking Word Alert & Streamlit Audio Player
    active_word = st.session_state.active_speaking_word
    if active_word and active_word in WORDS_DATABASE:
        w_data = WORDS_DATABASE[active_word]
        lang_key = st.session_state.lang_mode.lower()
        info = w_data[lang_key]
        
        st.markdown(f"""
        <div class="audio-wave-box">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="font-size: 2.2rem;">{w_data['emoji']}</div>
                <div>
                    <div style="font-size: 0.8rem; color: #38bdf8; font-weight: 700; text-transform: uppercase;">
                        Now Speaking • {st.session_state.lang_mode} Standard
                    </div>
                    <div style="font-size: 1.5rem; font-weight: 800; color: #ffffff;">
                        "{active_word}" <span style="font-size: 1rem; color: #94a3b8; font-weight: 500;">({info['name']})</span>
                    </div>
                    <div style="font-size: 0.9rem; color: #e2e8f0; margin-top: 2px;">
                        <strong>Gesture:</strong> {info['gesture']}
                    </div>
                </div>
            </div>
            <div style="text-align: right;">
                <span class="badge-pill {current_lang_badge}">Speaking Active</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if dual_audio_stream:
            mp3_path = os.path.join(AUDIO_DIR, f"{w_data['slug']}.mp3")
            if os.path.exists(mp3_path):
                st.audio(mp3_path, format="audio/mp3", autoplay=True)

    # 10 Words Grid Display
    st.markdown(f"#### 📚 Vocabulary Word Cards ({st.session_state.lang_mode} Mode)")
    
    words_list = list(WORDS_DATABASE.keys())
    
    # 2 rows of 5 cards each
    row1 = words_list[:5]
    row2 = words_list[5:]

    def render_word_row(row_words):
        cols = st.columns(len(row_words))
        for idx, word in enumerate(row_words):
            data = WORDS_DATABASE[word]
            lang_key = st.session_state.lang_mode.lower()
            info = data[lang_key]
            
            with cols[idx]:
                with st.container(border=True):
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <span style="font-size: 2.2rem;">{data['emoji']}</span>
                        <div style="font-size: 1.25rem; font-weight: 800; color: #f8fafc; margin-top: 4px;">{word}</div>
                        <div style="font-size: 0.8rem; color: #38bdf8; font-weight: 600;">{info['name']}</div>
                        <div style="font-size: 0.75rem; color: #94a3b8; margin: 8px 0; min-height: 38px;">
                            {info['motion']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    btn_col1, btn_col2 = st.columns([2, 1])
                    with btn_col1:
                        if st.button(f"🗣️ Speak", key=f"btn_speak_{word}", use_container_width=True):
                            st.session_state.active_speaking_word = word
                            st.session_state.trigger_speech_text = word
                            st.rerun()
                    with btn_col2:
                        if st.button(f"➕", key=f"btn_add_{word}", help=f"Add '{word}' to sentence pad", use_container_width=True):
                            st.session_state.sentence_tokens.append(word)
                            st.rerun()

    render_word_row(row1)
    st.write("")
    render_word_row(row2)

# =========================================================
# TAB 2: VOICE TO SIGN
# =========================================================
with tab_voice_to_sign:
    st.markdown("### 🎥 Voice to Sign Translation")
    st.markdown("Type a word (or speak it into your microphone) to immediately display its **animated Sign Language Video**.")

    v_col1, v_col2 = st.columns([3, 2], gap="large")

    with v_col1:
        st.markdown("#### 🔍 Input Word / Voice Recognition")

        # Live Web Speech Recognition Widget (Microphone button)
        components.html("""
        <div style="background: #1e293b; padding: 14px 18px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 15px; display: flex; align-items: center; justify-content: space-between;">
            <div style="color: #f8fafc; font-size: 0.95rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
                🎙️ <strong>Live Microphone Voice Recognition:</strong> Click button to dictate.
            </div>
            <button id="micBtn" onclick="startDictation()" style="background: #0284c7; color: white; border: none; padding: 8px 16px; border-radius: 8px; font-weight: 600; cursor: pointer;">
                Start Mic Voice
            </button>
        </div>
        <div id="speechOutput" style="color: #38bdf8; font-size: 0.85rem; font-family: monospace; min-height: 20px;"></div>
        <script>
            function startDictation() {
                const btn = document.getElementById('micBtn');
                const out = document.getElementById('speechOutput');
                if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                    out.innerText = "Speech recognition is not supported in this browser. Please type below.";
                    return;
                }
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                const recognition = new SpeechRecognition();
                recognition.lang = 'en-US';
                recognition.interimResults = false;
                recognition.maxAlternatives = 1;

                btn.innerText = "🔴 Listening...";
                btn.style.background = "#ef4444";
                out.innerText = "Listening for words: Hello, Thank you, Yes, No, Help, Water, Food, Please, Name, How are you...";

                recognition.onresult = function(event) {
                    const text = event.results[0][0].transcript;
                    out.innerText = "Recognized: '" + text + "' (Type it below or select from quick chips!)";
                    btn.innerText = "Start Mic Voice";
                    btn.style.background = "#0284c7";
                };

                recognition.onerror = function(event) {
                    out.innerText = "Mic Error/Permission: " + event.error + ". Please type the word below.";
                    btn.innerText = "Start Mic Voice";
                    btn.style.background = "#0284c7";
                };

                recognition.onend = function() {
                    btn.innerText = "Start Mic Voice";
                    btn.style.background = "#0284c7";
                };

                recognition.start();
            }
        </script>
        """, height=90)

        # Typing Input Box
        typed_input = st.text_input(
            label="Type a word or phrase here:",
            value=st.session_state.selected_query_word,
            placeholder="e.g. Hello, Thank You, Yes, No, Water, Help, Food...",
            help="Type any of the 10 target words or common conversational variations."
        )

        matched_word = normalize_input(typed_input)
        if matched_word:
            st.session_state.selected_query_word = matched_word

        # Quick Select Chip Pills
        st.markdown("<div style='font-size: 0.85rem; color: #94a3b8; font-weight: 600; margin: 10px 0 6px 0;'>QUICK SELECTION CHIPS (TEST IN 1 CLICK):</div>", unsafe_allow_html=True)
        
        chip_cols = st.columns(5)
        for idx, w in enumerate(list(WORDS_DATABASE.keys())[:5]):
            with chip_cols[idx]:
                if st.button(w, key=f"chip_top_{w}", use_container_width=True):
                    st.session_state.selected_query_word = w
                    st.rerun()

        chip_cols2 = st.columns(5)
        for idx, w in enumerate(list(WORDS_DATABASE.keys())[5:]):
            with chip_cols2[idx]:
                if st.button(w, key=f"chip_bot_{w}", use_container_width=True):
                    st.session_state.selected_query_word = w
                    st.rerun()

        st.markdown("---")

        # Target Word Details
        display_word = st.session_state.selected_query_word
        if display_word in WORDS_DATABASE:
            w_info = WORDS_DATABASE[display_word]
            lang_key = st.session_state.lang_mode.lower()
            details = w_info[lang_key]
            
            st.markdown(f"#### 📖 Sign Specification ({st.session_state.lang_mode})")
            st.markdown(f"""
            <div class="guide-step">
                <strong>Sign Concept:</strong> {details['name']}
            </div>
            <div class="guide-step">
                <strong>Handshape:</strong> {details['handshape']}
            </div>
            <div class="guide-step">
                <strong>Motion Vector:</strong> {details['motion']}
            </div>
            <div class="guide-step">
                <strong>Gesture Execution:</strong> {details['gesture']}
            </div>
            <div class="guide-step">
                <strong>Demonstration Tip:</strong> {details['tip']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning(f"Word '{typed_input}' not in the 10 target words. Try one from: {', '.join(WORDS_DATABASE.keys())}")

    with v_col2:
        st.markdown("#### 📺 Sign Language Video Player")
        
        display_word = st.session_state.selected_query_word
        if display_word in WORDS_DATABASE:
            w_slug = WORDS_DATABASE[display_word]["slug"]
            
            # Select target video folder based on active language mode
            target_dir = ISL_DIR if st.session_state.lang_mode == "ISL" else ASL_DIR
            video_file = os.path.join(target_dir, f"{w_slug}.mp4")
            
            # Video Header Card
            st.markdown(f"""
            <div style="background: #0f172a; border-radius: 12px 12px 0 0; padding: 12px 18px; border: 1px solid rgba(255,255,255,0.1); border-bottom: none; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-size: 1.1rem; font-weight: 700; color: #ffffff;">{display_word.upper()}</span>
                    <span style="font-size: 0.85rem; color: #94a3b8; margin-left: 8px;">({st.session_state.lang_mode} Video)</span>
                </div>
                <span class="badge-pill {current_lang_badge}">HD H.264 MP4</span>
            </div>
            """, unsafe_allow_html=True)

            if os.path.exists(video_file):
                # Native Streamlit video player
                st.video(video_file, autoplay=True, loop=True)
            else:
                st.error(f"Video file missing for {display_word} at {video_file}")

            # Comparative Toggle: Compare ISL vs ASL
            with st.expander("🔄 Compare with alternate sign language"):
                alt_lang = "ASL" if st.session_state.lang_mode == "ISL" else "ISL"
                alt_dir = ASL_DIR if st.session_state.lang_mode == "ISL" else ISL_DIR
                alt_video = os.path.join(alt_dir, f"{w_slug}.mp4")
                
                st.markdown(f"**Alternate Video: {display_word} in {alt_lang}**")
                if os.path.exists(alt_video):
                    st.video(alt_video, autoplay=False, loop=True)
                else:
                    st.info(f"Alternate {alt_lang} video available.")

# ================= FOOTER =================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 10px 0;">
    🎓 <strong>B.Tech / Final Year Capstone Demonstration</strong> • Real-Time Sign Language Bridge (ISL & ASL)<br/>
    Powered by Python Streamlit • Google gTTS • Web Speech API • FFmpeg Video Synthesizer
</div>
""", unsafe_allow_html=True)
