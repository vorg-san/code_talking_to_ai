#!/bin/bash

# Start Cursor Transcriber
# This script activates the virtual environment and starts the transcriber

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "❌ ERROR: Virtual environment not found at $VENV_DIR"
    echo "   Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Check if .env file exists, if not, create from example
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    if [ -f "$SCRIPT_DIR/.env.example" ]; then
        echo "Creating .env file from .env.example..."
        cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
        echo "✅ Created .env file. You can customize it if needed."
    else
        echo "⚠️  Warning: No .env file found. Using default configuration."
        echo "   Create .env.example file for configuration template."
    fi
fi

# Check if required packages are installed
python -c "import whisper, sounddevice, numpy, pynput, dotenv" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required packages..."
    pip install -q -r requirements.txt
fi

# Run the transcriber
python "$SCRIPT_DIR/cursor_transcriber.py"

