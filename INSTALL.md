# Installation Guide

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd transcriber
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install FFmpeg:**
   - macOS: `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt update && sudo apt install ffmpeg`
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

5. **Configure settings:**
   ```bash
   cp .env.example .env
   # Edit .env to customize command words and settings
   ```

6. **Grant permissions (macOS):**
   - System Settings > Privacy & Security > Microphone (enable Terminal)
   - System Settings > Privacy & Security > Accessibility (enable Terminal)

7. **Run:**
   ```bash
   ./start_transcriber.sh
   ```

## Detailed Installation

### Prerequisites

- Python 3.8 or higher
- FFmpeg installed and in PATH
- Microphone access
- macOS: Accessibility permissions for keyboard simulation

### Step-by-Step

#### 1. Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows
```

#### 2. Install Python Packages

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- `openai-whisper` - Speech recognition
- `sounddevice` - Audio capture
- `numpy` - Audio processing
- `pynput` - Keyboard simulation
- `python-dotenv` - Configuration management

#### 3. Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Linux (Arch):**
```bash
sudo pacman -S ffmpeg
```

**Windows:**
- Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Extract and add to PATH
- Or use package manager:
  - Chocolatey: `choco install ffmpeg`
  - Scoop: `scoop install ffmpeg`

#### 4. Configuration

Copy the example configuration:
```bash
cp .env.example .env
```

Edit `.env` to customize:
- Command words (wake word, clear, go code it, stop, exit)
- Whisper model (tiny, base, small, medium, large, turbo)
- Audio processing settings
- Advanced options

#### 5. Permissions Setup (macOS)

**Microphone Access:**
1. Open System Settings
2. Go to Privacy & Security > Microphone
3. Enable Terminal (or your terminal app)

**Accessibility (for keyboard simulation):**
1. Open System Settings
2. Go to Privacy & Security > Accessibility
3. Enable Terminal (or your terminal app)
4. Restart Terminal after enabling

#### 6. Verify Installation

Test Whisper installation:
```bash
./test_whisper.sh
```

Test keyboard simulation:
```bash
source venv/bin/activate
python test_keyboard.py
```

## Troubleshooting

### Virtual Environment Issues

If `venv` folder is missing:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### FFmpeg Not Found

Verify FFmpeg is installed:
```bash
ffmpeg -version
```

If not found, add to PATH or reinstall.

### Permission Denied

Make scripts executable:
```bash
chmod +x start_transcriber.sh
chmod +x test_whisper.sh
```

### Import Errors

If you get import errors:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration Not Loading

Ensure `.env` file exists:
```bash
cp .env.example .env
```

Check that `python-dotenv` is installed:
```bash
pip install python-dotenv
```

## Next Steps

After installation, see [README.md](README.md) for usage instructions.

