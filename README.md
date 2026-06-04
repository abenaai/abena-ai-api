# Abena AI API

African‑language **Text‑to‑Speech** (speech from text) and **Speech Recognition** (text from speech), over plain HTTP.

Use it from a website, a phone app, a server, or just your terminal — **no special library required**.

> 🟢 **Start free:** you get **100 requests with no account and no API key**. Just send a request and it works.

- 🌍 Live playground: <https://abena.mobobi.com/playground/tts/>
- 📖 Full docs: <https://abena.mobobi.com/playground/sdk/docs/>

---

## Base URL

```
https://abena.mobobi.com/playground/api/v1
```

## Authentication

For the **free tier** you don't need anything — just send the request.

When you have an API key (from your [dashboard](https://abena.mobobi.com/playground/sdk/dashboard/)), send it one of these ways:

```
Authorization: Bearer YOUR_API_KEY      # recommended
X-API-Key: YOUR_API_KEY
?api_key=YOUR_API_KEY                    # query string, handy for quick tests
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
| `voice` | yes      | A voice ID, e.g. `akua_eng`, `abena_twi`, `kobby_gpe` — see [Voices](#tts-voices). |
| `speed` | no       | `1.0` normal, `0.5` slowest, `2.0` fastest. Default `1.0`. |

**Response (JSON)**

```json
{
  "status": "success",
  "audio_base64": "UklGRiQ...",
  "duration_seconds": 2.91,
  "mime_type": "audio/wav"
}
```

**Example (curl)** — saves `speech.wav`, no API key needed:

```bash
curl -s -X POST https://abena.mobobi.com/playground/api/v1/tts/synthesize/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Akwaaba, wo ho te sen?", "voice": "abena_twi", "speed": 1.0}' \
  | python3 -c "import sys,json,base64; open('speech.wav','wb').write(base64.b64decode(json.load(sys.stdin)['audio_base64'])); print('Saved speech.wav')"
```

> 🗣️ **Twi tip (voice `abena_twi`):** write naturally and use commas to break long ideas into short phrases. The voice reads phrase‑by‑phrase, which sounds far more natural for podcasts and long text.

### TTS Voices

Fetch the live list any time: `GET /tts/voices.json`. Older short IDs like `akua`, `abena`, and `kobby` are still accepted as aliases, but new integrations should use the language-suffixed IDs below.

| Voice ID   | Name     | Language                  | Country  | Gender |
|------------|----------|---------------------------|----------|--------|
| `abena_twi`    | Abena    | Twi (Akan) 🇬🇭            | Ghana    | Female |
| `kobby_gpe`    | Kobby    | Ghanaian Pidgin English 🇬🇭| Ghana    | Male   |
| `akua_eng`     | Akua     | English (Ghanaian accent) 🇬🇭| Ghana | Female |
| `mawuli_ewe`   | Mawuli   | Ewe                       | Ghana    | Male   |
| `james_pcm`    | James    | Nigerian Pidgin English   | Nigeria  | Male   |
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
| `audio_file`     | yes      | Your audio file (e.g. `.wav`, MP3, M4A). Up to **2 minutes** (120 seconds), 8 MB max. |
| `language`       | no       | `en` (English) or `gpe` (Ghanaian Pidgin). Default `en`. |
| `reference_text` | no       | If you know the correct text, include it to also get accuracy/WER scores. |

**Response (JSON)**

```json
{
  "text": "hello how are you",
  "transcription": "hello how are you",
  "language": "en",
  "confidence": 85.0,
  "duration_seconds": 3.2
}
```

**Example (curl)**

```bash
curl -X POST https://abena.mobobi.com/playground/api/v1/asr/transcribe/ \
  -F "audio_file=@recording.wav" \
  -F "language=en"
```

### ASR Languages

Fetch the live list any time: `GET /asr/voices.json`

| Code  | Language                | Country |
|-------|-------------------------|---------|
| `en`  | English (US)            | United States |
| `gpe` | Ghanaian Pidgin English 🇬🇭| Ghana |

> 🔜 More languages, including **Akan Twi** speech recognition, are coming soon.

---

## Errors & Limits

Errors return JSON with a helpful `message` (TTS) or `error` (ASR) field.

| Status      | Meaning            | What to do |
|-------------|--------------------|------------|
| `200`       | Success            | Use the result. |
| `400`       | Bad request        | Check fields (missing `text`, unknown `voice`, `speed` out of range). |
| `401`       | Free limit reached | You've used your 100 free requests — [get an API key](https://abena.mobobi.com/playground/sdk/dashboard/). |
| `413`       | Too large          | Shorten text (500 chars) or audio (120 s / 8 MB). |
| `429`       | Too many requests  | Slow down and retry shortly. |
| `500`/`503` | Server issue       | Retry shortly; contact support if it persists. |

---

## Examples

Runnable examples live in [`examples/`](examples/):

- [`examples/index.html`](examples/index.html) — a complete web page. Open it in any browser; no install, no key.
- [`examples/tts.py`](examples/tts.py) — Python text‑to‑speech.
- [`examples/asr.py`](examples/asr.py) — Python speech recognition.
- [`examples/tts.js`](examples/tts.js) — Node.js / browser text‑to‑speech.

### Quick browser snippet

```javascript
const res = await fetch(
  "https://abena.mobobi.com/playground/api/v1/tts/synthesize/",
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: "Hello!", voice: "akua_eng" })
  }
);
const data = await res.json();
new Audio("data:audio/wav;base64," + data.audio_base64).play();
```

---

## License

[MIT](LICENSE)
