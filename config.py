#!/usr/bin/env python3
"""
Configuration module for Cursor Transcriber
Loads settings from environment variables with sensible defaults
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Command words - can be overridden via environment variables
WAKE_WORD = os.getenv("WAKE_WORD", "bob")
CLEAR_WORD = os.getenv("CLEAR_WORD", "zip")
SEND_WORD = os.getenv("SEND_WORD", "go code it")
STOP_WORD = os.getenv("STOP_WORD", "stop")
QUIT_WORD = os.getenv("QUIT_WORD", "exit")

# Commands dictionary with explanations
COMMANDS = {
    WAKE_WORD: "Start recording/transcription",
    STOP_WORD: "Stop recording (only when recording)",
    CLEAR_WORD: "Clear all text in focused window (only when not recording)",
    SEND_WORD: "Send Enter key (only when recording)",
    QUIT_WORD: "Shut down the program",
}

# Whisper model configuration
MODEL_NAME = os.getenv("WHISPER_MODEL", "medium")
# Options: "tiny", "base", "small", "medium", "large", "turbo"

# Audio processing configuration
SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", "16000"))  # Whisper requires 16kHz
CHUNK_DURATION = float(
    os.getenv("CHUNK_DURATION", "2.0")
)  # Seconds for wake word detection
TRANSCRIBE_DURATION = float(
    os.getenv("TRANSCRIBE_DURATION", "5.0")
)  # Seconds for transcription chunks
SILENCE_THRESHOLD = float(
    os.getenv("SILENCE_THRESHOLD", "0.01")
)  # Audio level threshold

# Whisper transcription options
NO_SPEECH_THRESHOLD = float(
    os.getenv("NO_SPEECH_THRESHOLD", "0.6")
)  # Lower = more sensitive
CONDITION_ON_PREVIOUS_TEXT = (
    os.getenv("CONDITION_ON_PREVIOUS_TEXT", "false").lower() == "true"
)

# English text filtering
ENGLISH_WORD_THRESHOLD = float(
    os.getenv("ENGLISH_WORD_THRESHOLD", "0.7")
)  # 0.7 = 70% must be English
