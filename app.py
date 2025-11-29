import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import speech_recognition as sr
import io
from gtts import gTTS

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Language configurations
LANGUAGES = {
    "English": "en-US",
    "Chinese (Mandarin)": "zh-CN"
}

# Function to generate TTS audio
def generate_tts_audio(text, language_code="en", max_retries=2):
    """Generate text-to-speech audio using gTTS with retry mechanism"""
    # Truncate very long messages for TTS performance
    if len(text) > 1000:
        text = text[:1000] + "..."

    for attempt in range(max_retries):
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang=language_code, slow=False)
            # Save to bytes buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            return audio_buffer.getvalue()
        except Exception as e:
            if attempt == max_retries - 1:
                return None
            continue
    return None

# Function to transcribe audio to text
def transcribe_audio(audio_file, language_code="en-US"):
    """Convert audio file to text using Google Speech Recognition"""
    if audio_file is None:
        return None

    try:
        recognizer = sr.Recognizer()
        # Use the audio file directly with speech recognition
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        # Use Google Speech Recognition with specified language
        text = recognizer.recognize_google(audio_data, language=language_code)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Error with speech recognition service: {e}"
    except Exception as e:
        return f"Error: {e}"

# Personality configurations with language support
def get_personality_prompt(personality_name, language):
    """Get personality prompt based on selected language"""
    base_prompts = {
        "General Assistant": {
            "English": "You are a helpful and friendly AI assistant. Provide clear, accurate, and concise responses to user questions.",
            "Chinese (Mandarin)": "You are a helpful and friendly AI assistant. ALWAYS respond in Chinese (中文). Provide clear, accurate, and concise responses to user questions. Even if the user speaks in English, respond in Chinese."
        },
        "Study Buddy": {
            "English": "You are a patient and knowledgeable study buddy. Help users understand concepts by breaking them down into simple explanations, providing examples, and encouraging learning. Use an encouraging and supportive tone.",
            "Chinese (Mandarin)": "You are a patient and knowledgeable study buddy. ALWAYS respond in Chinese (中文). Help users understand concepts by breaking them down into simple explanations, providing examples, and encouraging learning. Use an encouraging and supportive tone. Even if the user speaks in English, respond in Chinese."
        },
        "Fitness Coach": {
            "English": "You are an enthusiastic and motivating fitness coach. Provide workout advice, nutrition tips, and encouragement. Keep your tone energetic and supportive. Always remind users to consult healthcare professionals for medical advice.",
            "Chinese (Mandarin)": "You are an enthusiastic and motivating fitness coach. ALWAYS respond in Chinese (中文). Provide workout advice, nutrition tips, and encouragement. Keep your tone energetic and supportive. Always remind users to consult healthcare professionals for medical advice. Even if the user speaks in English, respond in Chinese."
        },
        "Gaming Helper": {
            "English": "You are a knowledgeable and enthusiastic gaming expert. Help users with game strategies, tips, recommendations, and gaming-related questions. Use casual, friendly language and share your passion for gaming.",
            "Chinese (Mandarin)": "You are a knowledgeable and enthusiastic gaming expert. ALWAYS respond in Chinese (中文). Help users with game strategies, tips, recommendations, and gaming-related questions. Use casual, friendly language and share your passion for gaming. Even if the user speaks in English, respond in Chinese."
        }
    }
    return base_prompts[personality_name][language]

PERSONALITIES = {
    "General Assistant": {
        "icon": "🤖",
        "description": "A helpful, friendly AI assistant ready to help with any questions"
    },
    "Study Buddy": {
        "icon": "📚",
        "description": "Your academic companion for learning and understanding concepts"
    },
    "Fitness Coach": {
        "icon": "💪",
        "description": "Motivating fitness expert for workout and nutrition guidance"
    },
    "Gaming Helper": {
        "icon": "🎮",
        "description": "Gaming expert for tips, strategies, and game recommendations"
    }
}

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "personality" not in st.session_state:
    st.session_state.personality = "General Assistant"

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

if "language" not in st.session_state:
    st.session_state.language = "English"

if "tts_audio" not in st.session_state:
    st.session_state.tts_audio = {}

if "processing" not in st.session_state:
    st.session_state.processing = False

if "last_audio_bytes" not in st.session_state:
    st.session_state.last_audio_bytes = None


# Sidebar
with st.sidebar:
    st.title("🤖 AI Chatbot")
    st.markdown("---")

    # Personality selector
    st.subheader("Choose Personality")
    selected_personality = st.selectbox(
        "Select AI personality:",
        options=list(PERSONALITIES.keys()),
        index=list(PERSONALITIES.keys()).index(st.session_state.personality)
    )

    # Update personality if changed
    if selected_personality != st.session_state.personality:
        st.session_state.personality = selected_personality
        st.session_state.messages = []  # Clear chat history on personality change
        st.session_state.tts_audio = {}  # Clear TTS audio on personality change
        st.rerun()

    # Display personality info
    current_personality = PERSONALITIES[st.session_state.personality]
    st.markdown(f"### {current_personality['icon']} {st.session_state.personality}")
    st.info(current_personality['description'])

    st.markdown("---")

    # Language selector in expander
    with st.expander("🌐 Language Settings", expanded=False):
        selected_language = st.selectbox(
            "Select language:",
            options=list(LANGUAGES.keys()),
            index=list(LANGUAGES.keys()).index(st.session_state.language),
            help="Choose language for voice input and AI responses"
        )

        # Update language if changed
        if selected_language != st.session_state.language:
            st.session_state.language = selected_language
            st.rerun()

        st.info("💡 AI will respond in the selected language")

    st.markdown("---")

    # About section in expander
    with st.expander("ℹ️ About", expanded=False):
        st.markdown("""
        This chatbot uses Google's Gemini AI to provide intelligent responses with voice capabilities.

        **Features:**
        - 🎤 Voice input & output
        - 🌐 Multi-language support
        - 🤖 Multiple AI personalities
        - 💬 Text & voice chat

        **Powered by:**
        - Streamlit
        - Google Gemini API (gemini-2.5-flash)
        - Google TTS & Speech Recognition
        """)

    st.markdown("---")

    # Clear history button with confirmation
    if st.button("🗑️ Clear Chat History", type="secondary", use_container_width=True, help="Clear all messages and audio"):
        st.session_state.messages = []
        st.session_state.tts_audio = {}
        st.rerun()

# Main chat interface
st.title(f"{PERSONALITIES[st.session_state.personality]['icon']} Chat with {st.session_state.personality}")

# Show welcome message if no messages yet
if len(st.session_state.messages) == 0:
    st.info(f"""
    👋 **Welcome!** I'm your {st.session_state.personality}.

    **Get started:**
    - 🎤 Use voice input below to speak your message
    - ⌨️ Or type your message in the text box
    - 🔊 I'll respond with both text and audio

    Current language: **{st.session_state.language}**
    """)
    st.markdown("---")

# Display chat messages with TTS audio
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

    # Add TTS audio player for assistant messages (outside chat_message)
    if message["role"] == "assistant":
        message_key = f"msg_{idx}"

        # Generate TTS audio if not already generated
        if message_key not in st.session_state.tts_audio:
            # Determine language code for TTS
            tts_lang = "en" if st.session_state.language == "English" else "zh-CN"

            # Show warning for long messages
            if len(message["content"]) > 500:
                st.caption("⏳ Long message - audio generation may take a moment...")

            # Generate audio with spinner feedback
            with st.spinner("🎵 Generating audio..."):
                audio_bytes = generate_tts_audio(message["content"], tts_lang)

            if audio_bytes:
                st.session_state.tts_audio[message_key] = audio_bytes
            else:
                st.error("❌ Audio generation failed. Please try again.")

        # Display audio player if audio exists
        if message_key in st.session_state.tts_audio:
            # Add visual separation
            st.markdown("---")

            # Use columns for better layout
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown("**🔊 Listen to response:**")
            with col2:
                msg_length = len(message["content"])
                st.caption(f"{msg_length} chars")

            # Full-width audio player for mobile-friendly design
            st.audio(st.session_state.tts_audio[message_key], format="audio/mp3")
            st.markdown("")  # Add spacing

# Voice input section
st.markdown("### 🎤 Voice Input")

# Add helpful usage tip
with st.expander("💡 How to use voice input", expanded=False):
    st.markdown("""
    1. Click the microphone button below
    2. Allow microphone access when prompted
    3. Speak clearly into your microphone
    4. Click stop when finished
    5. Your message will be automatically transcribed and sent to the AI

    **Tip:** For best results, speak in a quiet environment
    """)

# Initialize last audio hash to track new recordings
if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None

audio_file = st.audio_input("Record your message", help="Click to start recording your voice message")

# Check if this is a new audio recording
if audio_file:
    audio_hash = hash(audio_file.getvalue())

    # Only transcribe if this is a new recording
    if audio_hash != st.session_state.last_audio_hash:
        st.session_state.last_audio_hash = audio_hash

        # Automatically transcribe when audio is recorded
        with st.spinner("Transcribing..."):
            language_code = LANGUAGES[st.session_state.language]
            transcribed_text = transcribe_audio(audio_file, language_code)
            if transcribed_text and not transcribed_text.startswith("Could not") and not transcribed_text.startswith("Error"):
                st.session_state.voice_text = transcribed_text
                st.success(f"Transcribed: {transcribed_text}")

                # Automatically send the transcribed message
                st.session_state.messages.append({"role": "user", "content": transcribed_text})

                # Generate AI response immediately
                with st.spinner("Thinking..."):
                    try:
                        # Get system prompt based on selected language
                        system_prompt = get_personality_prompt(st.session_state.personality, st.session_state.language)
                        model = genai.GenerativeModel(
                            'gemini-2.5-flash',
                            system_instruction=system_prompt
                        )
                        response = model.generate_content(transcribed_text)
                        ai_response = response.text
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    except Exception as e:
                        error_message = f"Error: {str(e)}"
                        st.session_state.messages.append({"role": "assistant", "content": error_message})

                # Clear voice text
                st.session_state.voice_text = ""
                st.rerun()
            else:
                st.error(transcribed_text)
else:
    # Reset hash when audio is cleared
    st.session_state.last_audio_hash = None

st.markdown("---")

# Text input section
st.markdown("### ⌨️ Text Input")
st.info("💡 You can also type your message instead of using voice")

prompt = st.text_input(
    "Type your message here:",
    key="text_input",
    placeholder="Enter your message and click Send...",
    help="Type your message and press Send to chat with the AI"
)

# Send button for typed messages
if st.button("Send Message", type="primary", use_container_width=True) and prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate AI response
    with st.spinner("Thinking..."):
        try:
            # Get system prompt based on selected language
            system_prompt = get_personality_prompt(st.session_state.personality, st.session_state.language)
            model = genai.GenerativeModel(
                'gemini-2.5-flash',
                system_instruction=system_prompt
            )
            response = model.generate_content(prompt)
            ai_response = response.text
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            error_message = f"Error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_message})

    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px;'>
        <p style='margin: 5px;'>🤖 <strong>Voice AI Assistant</strong></p>
        <p style='margin: 5px; font-size: 0.9em;'>Built with Streamlit & Google Gemini API</p>
        <p style='margin: 5px; font-size: 0.8em;'>Powered by AI • Voice-enabled • Multi-language</p>
    </div>
    """,
    unsafe_allow_html=True
)
