# Cursor Transcriber

Real-time voice transcription tool that listens for wake words and transcribes your speech directly into any focused window. Perfect for voice-to-text input in chat applications, text editors, and more.

## Features

- 🎤 **Wake Word Activation**: Say a command word to start transcription
- 🗣️ **Real-time Transcription**: Uses OpenAI Whisper for accurate speech-to-text
- ⌨️ **Auto-typing**: Automatically types transcribed text into the focused window
- 🔒 **Privacy**: All processing happens locally on your machine (offline after model download)
- ⚙️ **Configurable**: All commands and settings can be customized via config file
- 🌍 **English Filtering**: Only types English words, filters out noise and non-English text
- 🔇 **Silence Detection**: Doesn't type during pauses or silence

## Requirements

- **macOS** (for keyboard simulation - can be adapted for Linux/Windows)
- **Python 3.8+**
- **Microphone access permissions**
- **FFmpeg** (for Whisper audio processing)
- **Accessibility permissions** (for keyboard simulation on macOS)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd transcriber
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**Arch Linux:**
```bash
sudo pacman -S ffmpeg
```

**Windows:**
- Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Or use Chocolatey: `choco install ffmpeg`
- Or use Scoop: `scoop install ffmpeg`

### 5. Configure Settings

Create your configuration file:

```bash
# If .env.example exists, copy it
cp .env.example .env

# Or create .env manually with your settings
# See Configuration section below for available options
```

Edit `.env` to customize command words and settings (see Configuration section below).

**Note:** If `.env.example` doesn't exist, the script will use default values. You can create `.env` manually with any settings you want to override.

### 6. Grant Permissions

**macOS:**

1. **Microphone permissions:**
   - System Settings > Privacy & Security > Microphone
   - Enable access for Terminal (or your terminal app)

2. **Accessibility permissions:**
   - System Settings > Privacy & Security > Accessibility
   - Enable Terminal (or your terminal app)
   - Required for keyboard simulation

## Usage

### Quick Start

**Using the startup script:**
```bash
./start_transcriber.sh
```

**Or directly:**
```bash
source venv/bin/activate
python cursor_transcriber.py
```

### Available Commands

The program will display all available commands on startup. Default commands:

- **Bob**: Start recording/transcription
- **Stop**: Stop recording (only when recording)
- **Zip**: Clear all text in focused window (only when not recording)
- **Go**: Send Enter key (only when recording)
- **Quit**: Shut down the program (works anytime)

### How It Works

1. **Start the script** - It begins listening for the wake word
2. **Say the wake word** (default: "Bob") - This activates transcription mode
3. **Speak your message** - Your speech is transcribed and typed into the focused window
4. **Say "go code it"** - Presses Enter to send/submit
5. **Say "stop"** - Returns to listening mode for the wake word
6. **Say "exit"** - Shuts down the program

### Example Workflow

```
[Script running...]
Available commands:
  • Bob: Start recording/transcription
  • Stop: Stop recording (only when recording)
  • Zip: Clear all text in focused window (only when not recording)
  • Go code it: Send Enter key (only when recording)
  • Exit: Shut down the program

[You say: "Bob"]
🎤 Recording started (say 'stop' to end)

[You say: "Hello world how are you"]
📝 Hello world how are you

[You say: "go code it"]
📤 Sending Enter...

[You say: "stop"]
🛑 Recording stopped
```

## Configuration

All settings can be configured via the `.env` file. Copy `.env.example` to `.env` and modify:

### Command Words

```env
WAKE_WORD=bob          # Word to start recording
CLEAR_WORD=zip         # Word to clear text (when not recording)
SEND_WORD="go code it" # Phrase to send Enter (when recording)
STOP_WORD=stop         # Word to stop recording
QUIT_WORD=exit         # Word to exit the program
```

### Whisper Model

```env
WHISPER_MODEL=medium   # Options: tiny, base, small, medium, large, turbo
```

**Model Comparison:**

| Model   | Size  | VRAM  | Speed | Accuracy |
|---------|-------|-------|-------|----------|
| tiny    | 39M   | ~1GB  | ~10x  | Lowest   |
| base    | 74M   | ~1GB  | ~7x   | Low      |
| small   | 244M  | ~2GB  | ~4x   | Good     |
| medium  | 769M  | ~5GB  | ~2x   | High     |
| large   | 1550M | ~10GB | 1x    | Best     |
| turbo   | 809M  | ~6GB  | ~8x   | High (English only) |

### Audio Processing

```env
SAMPLE_RATE=16000              # Audio sample rate (Whisper requires 16kHz)
CHUNK_DURATION=2.0             # Seconds for wake word detection chunks
TRANSCRIBE_DURATION=5.0        # Seconds for transcription chunks
SILENCE_THRESHOLD=0.01         # Audio level threshold for silence detection
```

### Advanced Options

```env
NO_SPEECH_THRESHOLD=0.6              # Lower = more sensitive to short speech
CONDITION_ON_PREVIOUS_TEXT=false    # Set to true to allow context-based autocompletion
ENGLISH_WORD_THRESHOLD=0.7          # 0.7 = 70% of words must be English-like
```

## Running in Background

To run as a background service:

```bash
nohup ./start_transcriber.sh > transcriber.log 2>&1 &
```

Stop it with:
```bash
pkill -f cursor_transcriber.py
```

## Troubleshooting

### Microphone Not Working
- Check System Settings > Privacy & Security > Microphone
- Ensure your terminal app has microphone permissions
- Try listing available audio devices:
  ```bash
  python -c "import sounddevice; print(sounddevice.query_devices())"
  ```

### Keyboard Simulation Not Working
- Make sure the target window is focused
- Grant Accessibility permissions: System Settings > Privacy & Security > Accessibility
- Enable Terminal (or your terminal app)
- Restart Terminal after granting permissions

### Poor Transcription Accuracy
- Use a better microphone
- Reduce background noise
- Try a larger Whisper model (medium or large)
- Adjust `SILENCE_THRESHOLD` if needed

### Commands Not Detected
- Speak clearly and ensure good microphone quality
- Check that command words match your `.env` configuration
- Try using the "tiny" model for faster wake word detection

### High CPU Usage
- Use a smaller model (tiny, base, or small)
- Increase `TRANSCRIBE_DURATION` to process less frequently
- Close other applications

## Privacy & Security

- ✅ All processing happens locally on your machine
- ✅ No data is sent to external servers (except initial model download)
- ✅ Audio is processed in memory, not saved to disk
- ✅ Works completely offline after model download
- ✅ `.env` file is gitignored and never committed

## Model Storage

Whisper models are downloaded automatically and stored in:
- **macOS/Linux**: `~/.cache/whisper/`
- **Windows**: `C:\Users\<username>\.cache\whisper\`

Check downloaded models:
```bash
ls ~/.cache/whisper/
```

## Development

### Project Structure

```
transcriber/
├── cursor_transcriber.py    # Main application
├── config.py                 # Configuration module
├── start_transcriber.sh      # Startup script
├── test_keyboard.py          # Keyboard simulation test
├── test_whisper.sh           # Installation test script
├── requirements.txt          # Python dependencies
├── .env.example             # Configuration template
├── .env                      # Your configuration (gitignored)
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

### Testing

Test keyboard simulation:
```bash
source venv/bin/activate
python test_keyboard.py
```

Test Whisper installation:
```bash
./test_whisper.sh
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Built with [OpenAI Whisper](https://github.com/openai/whisper)
- Uses [sounddevice](https://python-sounddevice.readthedocs.io/) for audio capture
- Uses [pynput](https://pynput.readthedocs.io/) for keyboard simulation
