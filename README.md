# Abena AI API

African‑language **Text‑to‑Speech** (speech from text) and **Speech Recognition** (text from speech), over plain HTTP.

Use it from a website, a phone app, a server, or just your terminal — **no special library required**.

> 🟢 **Start free:** no account or API key is required. Speech Recognition includes 20 free transcriptions; other free API endpoints include up to 30 requests. Sign in for 50 free Speech Recognition transcriptions.

- 🌍 Live playground: <https://abena.mobobi.com/playground/tts/>
- 🎙️ Speech Recognition playground: <https://abena.mobobi.com/playground/asr/>
- 📖 Full docs: <https://abena.mobobi.com/playground/sdk/docs/>

---

## Base URL

```
https://abena.mobobi.com/playground/api/v1
```

> ℹ️ **First request to a voice may take ~10–15 seconds.** The first time a voice is used, its model is loaded and prepared on our server (offline). After that the same voice responds in about a second.

---

## Text‑to‑Speech

Send text + a voice, get audio back. The audio comes as a **Base64‑encoded WAV** inside JSON, which is easy to use from any language and from the browser.

**Endpoint**

```
POST /tts/synthesize/
```

**Request body (JSON)**

| Field   | Required | Description |
|---------|----------|-------------|
| `text`  | yes      | Text to speak (up to 500 characters). |
| `voice` | yes      | A voice ID, e.g. `akua_eng`, `abena_twi_high`, `kobby_gpe` — see [Voices](#tts-voices). |
| `speed` | no       | `1.0` normal, `0.5` slowest, `2.0` fastest. Default `1.0`. |

**Response (JSON)**

```json
{
  "status": "success",
  "voice": "abena_twi_high",
  "audio_base64": "UklGRiQ...",
  "duration_seconds": 2.91,
  "mime_type": "audio/wav",
  "quality": "high"
}
```

`abena_twi_high` always uses the High voice. If the voice service is temporarily at capacity, retry after the interval returned by the API.

**Example (curl)** — saves `speech.wav`, no API key needed:

```bash
curl -s -X POST https://abena.mobobi.com/playground/api/v1/tts/synthesize/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Akwaaba, wo ho te sen?", "voice": "abena_twi_high", "speed": 1.0}' \
  | python3 -c "import sys,json,base64; open('speech.wav','wb').write(base64.b64decode(json.load(sys.stdin)['audio_base64'])); print('Saved speech.wav')"
```

> 🗣️ **Twi tip:** use `abena_twi_high` for the newer, more natural single-speaker Twi voice. Use `abena_twi_lite` when you want the lighter voice, which can sound clearer on some short phrases. For longer Twi text, write naturally and use commas to break long ideas into short phrases.

### TTS Voices

Fetch the live list any time: `GET /tts/voices.json`. Older short IDs and playground model IDs like `akua`, `en-ng-chioma`, `en-ng-chioma-whispering`, `swahili`, and `nigerian_pidgin_s` are still accepted as aliases, but new integrations should use the language-suffixed IDs below. The old Twi ID `abena_twi` has been replaced by explicit High and Lite options.

| Voice ID   | Name     | Language                  | Country  | Gender |
|------------|----------|---------------------------|----------|--------|
| `abena_twi_high` | Abena High | Twi (Akan, newer natural voice) 🇬🇭 | Ghana | Female |
| `abena_twi_lite` | Abena Lite | Twi (Akan, lighter voice) 🇬🇭 | Ghana | Female |
| `kobby_gpe`    | Kobby    | Ghanaian Pidgin English 🇬🇭| Ghana    | Male   |
| `akua_eng`     | Akua     | English (Ghanaian accent) 🇬🇭| Ghana | Female |
| `kwabena_eng`  | Kwabena  | English (Ghanaian accent) 🇬🇭| Ghana | Male |
| `chioma_eng`   | Chioma   | English (Nigerian accent, energetic) | Nigeria | Female |
| `chioma_whispering_eng` | Chioma | English (Nigerian accent, whispering) | Nigeria | Female |
| `mawuli_ewe`   | Mawuli   | Ewe                       | Ghana    | Male   |
| `james_pcm`    | James    | Nigerian Pidgin English   | Nigeria  | Male   |
| `amani_swh`    | Amani    | Swahili                   | Kenya    | Female |
| `abubakar_hau` | Abubakar | Hausa                     | Nigeria  | Male   |
| `folami_yor`   | Folami   | Yoruba                    | Nigeria  | Female |

---

## Speech Recognition

Send an audio file, get the text back. Upload the file as a form field named `audio_file` (`multipart/form-data`).

**Endpoint**

```
POST /asr/transcribe/
```

**Form fields**

| Field            | Required | Description |
|------------------|----------|-------------|
| `audio_file`     | yes      | Your audio file, up to **25 MB**. Twi: 60 seconds. Ghanaian English/Pidgin: 120 seconds. |
| `language`       | no       | `twi-en` (recommended Twi), `twi-pure`, `en`, or `gpe`. Default `en`. |
| `reference_text` | no       | If you know the correct text, include it to also get accuracy/WER scores. |

Supported audio formats: WAV/PCM, MP3, M4A/AAC, FLAC, OGG, and other common formats. For predictable batch evaluations, use mono 16-bit PCM WAV at 16 kHz; files already in that format are used directly. Other valid files are normalized before transcription.

**Response (JSON)**

```json
{
  "text": "Mepɛ sɛ mede sika kɔma Kwame",
  "transcription": "Mepɛ sɛ mede sika kɔma Kwame",
  "language": "twi-en",
  "duration_seconds": 3.2,
  "credits_remaining": 19,
  "credit_limit": 20
}
```

**Example (curl)**

```bash
curl -X POST https://abena.mobobi.com/playground/api/v1/asr/transcribe/ \
  -F "audio_file=@recording.wav" \
  -F "language=twi-en"
```

### ASR Languages

Fetch the live list any time: `GET /asr/voices.json`

| Code  | Language                | Country |
|-------|-------------------------|---------|
| `twi-en` | Akan Twi + English (Recommended) 🇬🇭 | Ghana |
| `twi-pure` | Akan Twi (Pure) 🇬🇭 | Ghana |
| `en`  | English (Ghanaian accent) 🇬🇭 | Ghana |
| `gpe` | Ghanaian Pidgin English 🇬🇭| Ghana |

Use `twi-en` for most Twi recordings, especially speech that includes English words. Use `twi-pure` only for recordings spoken entirely in Twi. Pure Twi responses include a short reminder in the `notice` field.

---

## Errors & Limits

Errors return JSON with a helpful `message` (TTS) or `error` (ASR) field.

| Status      | Meaning            | What to do |
|-------------|--------------------|------------|
| `200`       | Success            | Use the result. |
| `400`       | Bad request        | Check fields (missing `text`, unknown `voice`, `speed` out of range). |
| `401`       | Authentication failed | Check the API key, or omit it to use the no-sign-in allowance. |
| `402`       | Credits used       | [Sign in](https://abena.mobobi.com/playground/sdk/dashboard/) for more free ASR credits or to manage your API allowance. |
| `413`       | Too large          | Shorten text (500 chars) or use audio no larger than 25 MB. |
| `429`       | Too many requests  | Slow down and retry shortly. |
| `500`       | Server issue       | Retry shortly; contact support if it persists. |
| `503`       | At capacity        | Wait for the `Retry-After` interval, then retry the same request. |

---

## Examples

Runnable examples live in [`examples/`](examples/):

- [`examples/index.html`](examples/index.html) — a complete web page. Open it in any browser; no install, no key.
- [`examples/tts.py`](examples/tts.py) — Python text‑to‑speech.
- [`examples/asr.py`](examples/asr.py) — Python speech recognition.
- [`examples/tts.js`](examples/tts.js) — Node.js / browser text‑to‑speech.

## Use From Any Language

The API is plain HTTP + JSON, so any language that can make a web request can use it. The examples below work with the free tier and do not require an API key.

### JavaScript

```javascript
const res = await fetch(
  "https://abena.mobobi.com/playground/api/v1/tts/synthesize/",
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      text: "Hello!",
      voice: "akua_eng",
      speed: 1.0
    })
  }
);

const data = await res.json();
new Audio("data:audio/wav;base64," + data.audio_base64).play();
```

### Python Text-to-Speech

Uses Python's built-in HTTP client, so there is no extra package to install.

```python
import base64, json
from urllib.request import Request, urlopen

payload = json.dumps({
    "text": "Akwaaba, wo ho te sen?",
    "voice": "abena_twi_high",
    "speed": 1.0
}).encode("utf-8")

req = Request(
    "https://abena.mobobi.com/playground/api/v1/tts/synthesize/",
    data=payload,
    headers={"Content-Type": "application/json", "Accept": "application/json"},
    method="POST",
)

with urlopen(req, timeout=120) as res:
    data = json.loads(res.read().decode("utf-8"))

with open("speech.wav", "wb") as f:
    f.write(base64.b64decode(data["audio_base64"]))

print("Saved speech.wav")
```

### Python Speech Recognition

```python
import json, mimetypes, uuid
from pathlib import Path
from urllib.request import Request, urlopen

audio_path = Path("recording.wav")
boundary = "----abena-" + uuid.uuid4().hex
audio_bytes = audio_path.read_bytes()
content_type = mimetypes.guess_type(audio_path.name)[0] or "application/octet-stream"

body = (
    f"--{boundary}\r\n"
    'Content-Disposition: form-data; name="language"\r\n\r\n'
    "twi-en\r\n"
    f"--{boundary}\r\n"
    f'Content-Disposition: form-data; name="audio_file"; filename="{audio_path.name}"\r\n'
    f"Content-Type: {content_type}\r\n\r\n"
).encode("utf-8") + audio_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

req = Request(
    "https://abena.mobobi.com/playground/api/v1/asr/transcribe/",
    data=body,
    headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Accept": "application/json",
    },
    method="POST",
)
with urlopen(req, timeout=120) as res:
    data = json.loads(res.read().decode("utf-8"))
print(data["text"])
```

## API Keys (Optional)

You do not need an API key for the free tier examples above. Just send a request and it works.

When you are ready to build beyond the no-account allowance, create a free account from your [dashboard](https://abena.mobobi.com/playground/sdk/dashboard/) and send your key one of these ways:

```
Authorization: Bearer YOUR_API_KEY      # recommended
X-API-Key: YOUR_API_KEY
?api_key=YOUR_API_KEY                    # query string, handy for quick tests
```

---

## License

[MIT](LICENSE)
