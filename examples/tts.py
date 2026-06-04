"""Abena AI — Text-to-Speech example.

Turns text into a WAV file. No API key needed (uses the free tier).

Run:
    python tts.py
"""

import base64
import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen

API = "https://abena.mobobi.com/playground/api/v1/tts/synthesize/"


def synthesize(text, voice="akua_eng", speed=1.0, out_file="speech.wav", api_key=None):
    payload = json.dumps({"text": text, "voice": voice, "speed": speed}).encode("utf-8")
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    req = Request(
        API,
        data=payload,
        headers=headers,
        method="POST",
    )
    try:
        with urlopen(req, timeout=120) as res:
            status_code = res.status
            data = json.loads(res.read().decode("utf-8"))
    except HTTPError as e:
        status_code = e.code
        data = json.loads(e.read().decode("utf-8"))

    if status_code == 200 and data.get("status") == "success":
        with open(out_file, "wb") as f:
            f.write(base64.b64decode(data["audio_base64"]))
        print(f"Saved {out_file} ({data['duration_seconds']}s of audio)")
    else:
        print("Error:", data.get("message") or data.get("error") or status_code)


if __name__ == "__main__":
    synthesize("Akwaaba, wo ho te sen?", voice="abena_twi")
