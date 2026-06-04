"""Abena AI — Text-to-Speech example.

Turns text into a WAV file. No API key needed (uses the free tier).

Run:
    pip install requests
    python tts.py
"""

import base64
import requests

API = "https://abena.mobobi.com/playground/api/v1/tts/synthesize/"


def synthesize(text, voice="akua", speed=1.0, out_file="speech.wav", api_key=None):
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    res = requests.post(
        API,
        json={"text": text, "voice": voice, "speed": speed},
        headers=headers,
        timeout=120,  # the first request to a voice can take ~10-15s to warm up
    )
    data = res.json()

    if res.ok and data.get("status") == "success":
        with open(out_file, "wb") as f:
            f.write(base64.b64decode(data["audio_base64"]))
        print(f"Saved {out_file} ({data['duration_seconds']}s of audio)")
    else:
        print("Error:", data.get("message") or data.get("error") or res.status_code)


if __name__ == "__main__":
    synthesize("Akwaaba, wo ho te sen?", voice="abena")
