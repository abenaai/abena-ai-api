"""Abena AI — Speech Recognition example.

Turns an audio file into text. No API key needed (uses the free tier).

Run:
    python asr.py recording.wav
"""

import json
import mimetypes
import sys
import uuid
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

API = "https://abena.mobobi.com/playground/api/v1/asr/transcribe/"


def transcribe(path, language="en", api_key=None):
    audio_path = Path(path)
    audio_bytes = audio_path.read_bytes()
    content_type = mimetypes.guess_type(audio_path.name)[0] or "application/octet-stream"
    boundary = "----abena-" + uuid.uuid4().hex
    body = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="language"\r\n\r\n'
        f"{language}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="audio_file"; filename="{audio_path.name}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode("utf-8") + audio_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Accept": "application/json",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    req = Request(API, data=body, headers=headers, method="POST")
    try:
        with urlopen(req, timeout=120) as res:
            status_code = res.status
            data = json.loads(res.read().decode("utf-8"))
    except HTTPError as e:
        status_code = e.code
        data = json.loads(e.read().decode("utf-8"))

    if status_code == 200 and "text" in data:
        print("Transcript:", data["text"])
    else:
        print("Error:", data.get("message") or data.get("error") or status_code)


if __name__ == "__main__":
    audio_path = sys.argv[1] if len(sys.argv) > 1 else "recording.wav"
    transcribe(audio_path)
