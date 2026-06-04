"""Abena AI — Speech Recognition example.

Turns an audio file into text. No API key needed (uses the free tier).

Run:
    pip install requests
    python asr.py recording.wav
"""

import sys
import requests

API = "https://abena.mobobi.com/playground/api/v1/asr/transcribe/"


def transcribe(path, language="en", api_key=None):
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    with open(path, "rb") as audio:
        res = requests.post(
            API,
            files={"audio_file": audio},
            data={"language": language},
            headers=headers,
            timeout=120,
        )
    data = res.json()

    if res.ok and "text" in data:
        print("Transcript:", data["text"])
    else:
        print("Error:", data.get("message") or data.get("error") or res.status_code)


if __name__ == "__main__":
    audio_path = sys.argv[1] if len(sys.argv) > 1 else "recording.wav"
    transcribe(audio_path)
