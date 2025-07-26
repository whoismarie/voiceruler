import os
import time
import json
import sys
import pyautogui
import pyaudio
from vosk import Model, KaldiRecognizer

MODEL_PATH = "vosk-model-small-en-us-0.15"

if not os.path.exists(MODEL_PATH):
    print(f"[ERROR] Model not found at {MODEL_PATH}")
    sys.exit(1)

print("[INFO] Loading Vosk model...")
model = Model(MODEL_PATH)
rec = KaldiRecognizer(model, 16000)

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=16000,
                 input=True,
                 frames_per_buffer=8000)
stream.start_stream()

print("[INFO] Listening for commands... (Ctrl+C to quit)")

try:
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "").strip()
            if text:
                print("[VOICE]", text)

                # First-letter delay hack
                pyautogui.typewrite(text[0])
                time.sleep(0.3)
                if len(text) > 1:
                    pyautogui.typewrite(text[1:])
                pyautogui.press('enter')

                time.sleep(0.2)

except KeyboardInterrupt:
    print("\n[INFO] Exiting cleanly...")
finally:
    stream.stop_stream()
    stream.close()
    pa.terminate()
    print("[INFO] Microphone stream closed. Goodbye!")