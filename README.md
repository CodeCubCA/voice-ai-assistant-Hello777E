[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Mbf-Zm77)

# Voice AI Assistant

A multi-language AI chatbot web application built with Streamlit and Google Gemini API, featuring voice input capabilities and multiple AI personalities.

## Features

- **Voice Input**: Record your voice and get automatic speech-to-text transcription
- **Multi-Language Support**: Switch between English and Chinese (Mandarin)
- **AI Personalities**: Choose from 4 different AI personalities:
  - General Assistant - Helpful and friendly for any questions
  - Study Buddy - Patient learning companion
  - Fitness Coach - Energetic workout and nutrition guide
  - Gaming Helper - Expert gaming tips and strategies
- **Text Input**: Type messages manually as an alternative to voice input
- **Chat History**: View your conversation history with the AI
- **Language-Aware Responses**: AI responds in the language you select

## Tech Stack

- **Frontend**: Streamlit
- **AI Model**: Google Gemini 2.5 Flash
- **Speech Recognition**: Google Speech Recognition API
- **Python Libraries**:
  - streamlit
  - google-generativeai
  - python-dotenv
  - SpeechRecognition

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- A Google Gemini API key

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/CodeCubCA/voice-ai-assistant-Hello777E.git
   cd voice-ai-assistant-Hello777E
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```

4. Add your Google Gemini API key to the `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

   Get your API key from: https://makersuite.google.com/app/apikey

### Running the Application

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## Usage

1. **Select a Personality**: Choose an AI personality from the sidebar
2. **Choose Language**: Select your preferred language (English or Chinese)
3. **Voice Input**: Click the microphone button to record your voice message
4. **Text Input**: Alternatively, type your message in the text box and click "Send Message"
5. **Clear History**: Use the "Clear Chat History" button in the sidebar to start fresh

## Project Structure

```
voice-ai-assistant/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not committed)
├── .env.example          # Template for environment variables
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## Security Notes

- The `.env` file containing your API key is excluded from version control
- Never commit your actual API key to the repository
- Use the `.env.example` file as a template for setting up your own environment

## License

This project is for educational purposes as part of a GitHub Classroom assignment.