#!/usr/bin/env python3
"""
Cursor Transcriber - Real-time voice transcription for Cursor AI chat
Listens for "Bob" wake word and transcribes speech into Cmd+L chat window
"""

import whisper
import numpy as np
import sounddevice as sd
import queue
import threading
import time
import sys
import re
from pynput import keyboard
from pynput.keyboard import Key, Controller

# Import configuration
from config import (
    WAKE_WORD,
    CLEAR_WORD,
    SEND_WORD,
    STOP_WORD,
    QUIT_WORD,
    COMMANDS,
    MODEL_NAME,
    SAMPLE_RATE,
    CHUNK_DURATION,
    TRANSCRIBE_DURATION,
    SILENCE_THRESHOLD,
    NO_SPEECH_THRESHOLD,
    CONDITION_ON_PREVIOUS_TEXT,
    ENGLISH_WORD_THRESHOLD,
)


class CursorTranscriber:
    def __init__(self):
        print("Loading Whisper model...")
        self.model = whisper.load_model(MODEL_NAME)
        self.audio_queue = queue.Queue()
        self.is_listening = False
        self.is_transcribing = False
        self.keyboard_controller = Controller()
        print("Available commands:")
        for command, explanation in COMMANDS.items():
            print(f"  • {command.capitalize()}: {explanation}")
        print()

    def audio_callback(self, indata, frames, time_info, status):
        """Callback for audio input stream"""
        if status:
            print(f"[WARNING] Audio status: {status}", file=sys.stderr)
        self.audio_queue.put(indata.copy())

    def is_english_text(self, text):
        """Check if text contains only English words and characters"""
        if not text:
            return False

        # Always allow command words (go code it, stop, bob, zip, exit)
        text_lower = text.lower().strip()
        command_words = [WAKE_WORD, STOP_WORD, CLEAR_WORD, SEND_WORD, QUIT_WORD]
        if any(cmd in text_lower for cmd in command_words):
            return True

        # Remove common punctuation and check if remaining is English
        # English words contain only letters, apostrophes, and hyphens
        text_clean = re.sub(r"[^\w\s\'-]", "", text.lower())
        words = text_clean.split()

        if not words:
            return False

        # For very short text (1-2 words), be more lenient
        if len(words) <= 2:
            english_pattern = re.compile(r"^[a-z]+(['-][a-z]+)*$")
            return any(english_pattern.match(word) for word in words)

        # Check if words contain only English letters, apostrophes, and hyphens
        english_pattern = re.compile(r"^[a-z]+(['-][a-z]+)*$")
        english_word_count = sum(1 for word in words if english_pattern.match(word))

        # Use configurable threshold for English word percentage
        return (
            english_word_count / len(words) >= ENGLISH_WORD_THRESHOLD
            if words
            else False
        )

    def has_speech(self, audio_data):
        """Check if audio contains actual speech (not just silence)"""
        # Calculate RMS (Root Mean Square) to detect audio level
        audio_float = (
            audio_data.astype(np.float32) / 32768.0
            if audio_data.dtype == np.int16
            else audio_data.astype(np.float32)
        )
        rms = np.sqrt(np.mean(audio_float**2))
        # Use configurable threshold for silence detection
        return rms > SILENCE_THRESHOLD

    def is_command_word(self, text):
        """Check if text contains any command word"""
        if not text:
            return False
        text_lower = text.lower().strip()
        command_words = [WAKE_WORD, STOP_WORD, CLEAR_WORD, SEND_WORD, QUIT_WORD]
        return any(cmd in text_lower for cmd in command_words)

    def transcribe_audio_chunk(self, audio_data, skip_silence_check=False):
        """Transcribe a chunk of audio using Whisper"""
        try:
            # For command detection, skip silence check to ensure commands are always transcribed
            # For regular text, check silence first to avoid unnecessary transcription
            if not skip_silence_check and not self.has_speech(audio_data):
                return ""

            # Convert int16 to float32 and normalize to [-1, 1]
            if audio_data.dtype == np.int16:
                audio_float32 = audio_data.astype(np.float32) / 32768.0
            else:
                audio_float32 = audio_data.astype(np.float32)

            # Ensure audio is in the right shape (1D array)
            if len(audio_float32.shape) > 1:
                audio_float32 = audio_float32.flatten()

            result = self.model.transcribe(
                audio_float32,
                language="en",
                condition_on_previous_text=CONDITION_ON_PREVIOUS_TEXT,
                no_speech_threshold=NO_SPEECH_THRESHOLD,
            )
            text = result["text"].strip()

            # Remove trailing periods that Whisper might add
            text = text.rstrip(".")

            # Always allow command words - bypass English filtering and silence checks
            if text and self.is_command_word(text):
                return text

            # For non-command text, apply English filtering
            if text and not self.is_english_text(text):
                return ""

            return text
        except Exception as e:
            print(f"[WARNING] Transcription error: {e}")
            return ""

    def check_wake_word(self, text):
        """Check if wake word is in transcribed text"""
        return WAKE_WORD in text.lower()

    def check_quit_command(self, text):
        """Check if quit command is in transcribed text"""
        import re

        text_lower = text.lower().strip()
        # Remove punctuation and split into words
        words_clean = re.sub(r"[^\w\s]", "", text_lower).split()
        # Check if it's just "exit" or a short phrase with "exit" (ignoring punctuation)
        return len(words_clean) <= 3 and QUIT_WORD in words_clean

    def check_clear_command(self, text):
        """Check if clear command is in transcribed text"""
        import re

        text_lower = text.lower().strip()
        # Remove punctuation and split into words
        words_clean = re.sub(r"[^\w\s]", "", text_lower).split()
        # Check if it's just "zip" or a short phrase with "zip" (ignoring punctuation)
        return len(words_clean) <= 3 and CLEAR_WORD in words_clean

    def check_send_command(self, text):
        """Check if send command is in transcribed text"""
        import re

        text_lower = text.lower().strip()
        # Remove punctuation and split into words
        words_clean = re.sub(r"[^\w\s]", "", text_lower).split()
        send_words = SEND_WORD.lower().split()
        # Check if all words of the send command are present in the text (ignoring punctuation)
        # Allow up to 5 total words (to account for extra words)
        return len(words_clean) <= 5 and all(word in words_clean for word in send_words)

    def send_enter(self):
        """Press Enter key"""
        try:
            self.keyboard_controller.press(Key.enter)
            self.keyboard_controller.release(Key.enter)
        except Exception as e:
            print(f"[WARNING] Could not send Enter: {e}")
            print(
                "          Grant Accessibility permissions: System Settings > Privacy & Security > Accessibility"
            )

    def clear_text(self):
        """Select all text and delete it"""
        try:
            # Select all: Cmd+A
            self.keyboard_controller.press(Key.cmd)
            self.keyboard_controller.press("a")
            self.keyboard_controller.release("a")
            self.keyboard_controller.release(Key.cmd)
            time.sleep(0.1)  # Brief delay

            # Delete: Backspace or Delete key
            self.keyboard_controller.press(Key.backspace)
            self.keyboard_controller.release(Key.backspace)
        except Exception as e:
            print(f"[WARNING] Could not clear text: {e}")
            print(
                "          Grant Accessibility permissions: System Settings > Privacy & Security > Accessibility"
            )

    def type_text(self, text):
        """Type text directly into the focused window"""
        try:
            if text:
                # Add a space at the end to prevent words from joining together
                text_with_space = text if text.endswith(" ") else text + " "
                self.keyboard_controller.type(text_with_space)
        except Exception as e:
            print(f"[WARNING] Could not type text: {e}")
            print(
                "          Grant Accessibility permissions: System Settings > Privacy & Security > Accessibility"
            )

    def process_audio_stream(self):
        """Main audio processing loop"""
        audio_buffer = []
        frames_per_chunk = int(SAMPLE_RATE * CHUNK_DURATION)

        while True:
            try:
                # Get audio data from queue
                audio_data = self.audio_queue.get(timeout=1.0)
                audio_buffer.append(audio_data)

                # Keep buffer size manageable
                total_frames = sum(len(chunk) for chunk in audio_buffer)
                if total_frames > frames_per_chunk * 3:
                    audio_buffer = audio_buffer[-2:]  # Keep last 2 chunks

                # Process chunk for wake word detection and clear command
                if not self.is_transcribing:
                    total_frames = sum(len(chunk) for chunk in audio_buffer)

                    if total_frames >= frames_per_chunk:
                        # Concatenate audio chunks
                        recent_audio = np.concatenate(audio_buffer)

                        # Transcribe chunk - skip silence check for command detection
                        text = self.transcribe_audio_chunk(
                            recent_audio, skip_silence_check=True
                        )

                        if text:
                            # Check for quit command first (works anytime)
                            if self.check_quit_command(text):
                                print("\n👋 Shutting down...\n")
                                import sys

                                sys.exit(0)
                            # Check for clear command (only when not recording)
                            elif self.check_clear_command(text):
                                print("🗑️ Clearing text...\n")
                                self.clear_text()
                                audio_buffer = []  # Clear buffer
                            # Check for wake word
                            elif self.check_wake_word(text):
                                print("\n🎤 Recording started (say 'stop' to end)\n")
                                try:
                                    self.is_transcribing = True
                                    audio_buffer = []  # Clear buffer
                                except KeyboardInterrupt:
                                    raise
                                except Exception as e:
                                    print(
                                        f"[WARNING] Error starting transcription: {e}"
                                    )
                                    self.is_transcribing = False
                            else:
                                # Keep only recent audio (last chunk) for next check
                                audio_buffer = audio_buffer[-1:] if audio_buffer else []
                        else:
                            # Keep only recent audio
                            audio_buffer = audio_buffer[-1:] if audio_buffer else []

                # Process transcription when active
                elif self.is_transcribing:
                    total_frames = sum(len(chunk) for chunk in audio_buffer)
                    frames_for_transcribe = int(SAMPLE_RATE * TRANSCRIBE_DURATION)

                    if total_frames >= frames_for_transcribe:
                        # Concatenate audio for transcription
                        audio_to_transcribe = np.concatenate(audio_buffer)
                        audio_buffer = []  # Clear buffer

                        # Transcribe - skip silence check to ensure commands are detected
                        text = self.transcribe_audio_chunk(
                            audio_to_transcribe, skip_silence_check=True
                        )

                        if text:
                            # Check for quit command first (works anytime, even when recording)
                            if self.check_quit_command(text):
                                print("\n👋 Shutting down...\n")
                                import sys

                                sys.exit(0)

                            # Remove wake word if present
                            clean_text = text.replace(WAKE_WORD, "").strip()

                            if not clean_text:
                                continue

                            # Check for send command (only when recording)
                            if self.check_send_command(clean_text):
                                print("📤 Sending Enter...\n")
                                self.send_enter()
                                print("🛑 Recording stopped\n")
                                self.is_transcribing = False
                                continue

                            # Check if this is a stop command (must be short phrase, <= 3 words, and contains "stop")
                            import re

                            text_lower = clean_text.lower().strip()
                            # Remove punctuation and split into words
                            words_clean = re.sub(r"[^\w\s]", "", text_lower).split()

                            # If it's just "stop" or a very short phrase with "stop", stop recording without typing
                            if len(words_clean) <= 3 and STOP_WORD in words_clean:
                                print("🛑 Recording stopped\n")
                                self.is_transcribing = False
                            else:
                                # Check if text ends with "stop" (with or without punctuation)
                                import re

                                # Check if the last word (after removing punctuation) is "stop"
                                words_list = clean_text.split()
                                should_stop = False

                                if len(words_list) > 0:
                                    last_word = words_list[-1].lower().rstrip(".,!?;:")
                                    if last_word == STOP_WORD:
                                        # Remove "stop" from the end
                                        words_list = words_list[:-1]
                                        clean_text = " ".join(words_list).strip()
                                        should_stop = True

                                # Type the text (without "stop" at the end if it was there)
                                # Remove trailing periods that Whisper might add
                                clean_text = clean_text.rstrip(".")
                                if clean_text:
                                    print(f"📝 {clean_text}")
                                    self.type_text(clean_text)

                                # Stop recording if "stop" was at the end
                                if should_stop:
                                    print("🛑 Recording stopped\n")
                                    self.is_transcribing = False

            except queue.Empty:
                continue
            except KeyboardInterrupt:
                self.is_transcribing = False
                break
            except Exception as e:
                print(f"[WARNING] Audio processing error: {e}")
                continue

    def run(self):
        """Start the transcriber"""
        try:
            # Start audio stream
            with sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype=np.int16,
                blocksize=int(SAMPLE_RATE * 0.1),  # 100ms blocks
                callback=self.audio_callback,
            ):
                # Start processing thread
                processing_thread = threading.Thread(
                    target=self.process_audio_stream, daemon=True
                )
                processing_thread.start()

                # Keep main thread alive
                try:
                    processing_thread.join()
                except KeyboardInterrupt:
                    print("\nShutting down...")
                    sys.exit(0)

        except Exception as e:
            print(f"[WARNING] Error starting audio stream: {e}")
            print("          Make sure microphone permissions are granted")
            sys.exit(1)


def main():
    """Main entry point"""
    transcriber = CursorTranscriber()
    transcriber.run()


if __name__ == "__main__":
    main()
