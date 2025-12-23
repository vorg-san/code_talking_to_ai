# OpenAI Whisper Setup Guide

## Installation

### 1. Virtual Environment (Already Created)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Whisper
```bash
pip install -U openai-whisper
```

### 3. Install FFmpeg (Required)
```bash
# macOS (using Homebrew)
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg
```

## Usage

### Command Line
```bash
# Basic transcription
whisper audio.mp3 --model base

# Specify language
whisper japanese.wav --language Japanese

# Translate to English
whisper japanese.wav --model medium --language Japanese --task translate

# Use turbo model (fastest, good for English)
whisper audio.flac --model turbo
```

### Python Script
```bash
# Activate virtual environment first
source venv/bin/activate

# Run test script
python test_whisper.py audio.mp3 base
```

### Python Code Example
```python
import whisper

# Load model (downloads automatically on first use)
model = whisper.load_model("base")

# Transcribe
result = model.transcribe("audio.mp3")
print(result["text"])
```

## Available Models

| Model   | Size  | VRAM  | Speed | Best For                    |
|---------|-------|-------|-------|-----------------------------|
| tiny    | 39M   | ~1GB  | ~10x  | Quick tests, low accuracy   |
| base    | 74M   | ~1GB  | ~7x   | Good balance (recommended)  |
| small   | 244M  | ~2GB  | ~4x   | Better accuracy             |
| medium  | 769M  | ~5GB  | ~2x   | High accuracy               |
| large   | 1550M | ~10GB | 1x    | Best accuracy               |
| turbo   | 809M  | ~6GB  | ~8x   | Fast, optimized (English)   |

**Note:** The `turbo` model is optimized for English and doesn't support translation tasks.

## Offline Usage

**YES, Whisper works completely offline!** 

- Models are downloaded once and stored locally in `~/.cache/whisper/`
- After the initial download, no internet connection is required
- All processing happens locally on your machine
- No data is sent to OpenAI or any external servers

### First Run
- On first use, Whisper downloads the model you specify
- This requires an internet connection
- Models range from ~39MB (tiny) to ~3GB (large)

### Subsequent Runs
- Once downloaded, models are cached locally
- You can work completely offline
- No network activity during transcription

## Model Storage Location

Models are stored in:
- **macOS/Linux**: `~/.cache/whisper/`
- **Windows**: `C:\Users\<username>\.cache\whisper\`

You can check what models you have downloaded:
```bash
ls ~/.cache/whisper/
```

## Troubleshooting

### FFmpeg not found
Make sure ffmpeg is installed and in your PATH:
```bash
which ffmpeg
ffmpeg -version
```

### Out of memory
- Use a smaller model (tiny, base, or small)
- Process shorter audio files
- Close other applications

### Slow performance
- Use a smaller model
- Process audio in chunks
- Use GPU acceleration if available (requires CUDA/ROCm)

## Example Workflow

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Transcribe an audio file
whisper my_audio.mp3 --model base

# 3. Or use Python
python test_whisper.py my_audio.mp3 base
```

