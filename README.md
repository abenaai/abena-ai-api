
# Abena AI API

African‑language **Text‑to‑Speech** (speech from text) and **Speech Recognition** (text from speech), over plain HTTP.

Use it from a website, a phone app, a server, or just your terminal — **no special library required**.

> 🟢 **Start free:** no account or API key is required. TTS API: 15 character-metered credits for guests or standard API accounts. Speech Recognition API: 10 guest or 15 signed-in transcriptions. [Check current allowances](https://abena.mobobi.com/playground/sdk/rate-limits/).

- 🌍 Live playground: <https://abena.mobobi.com/playground/tts/>
- 🎙️ Speech Recognition playground: <https://abena.mobobi.com/playground/asr/>
- 📖 Full docs: <https://abena.mobobi.com/playground/sdk/docs/>

---

## Base URL

```
https://abena.mobobi.com/playground/api/v1
```

> ℹ️ **The first request to a voice can take longer while it loads.** Response time depends on text length, voice quality and current demand. Respect `Retry-After` when the service is busy.

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
| `voice` | yes      | A voice ID, e.g. `akua_eng`, `abena_twi_high`, `kobby_gpe_high` — see [Voices](#tts-voices). |
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

> 🗣️ **Twi tip:** start with `abena_twi_medium`, the recommended natural Twi voice. Choose Abena, Ama or Yaa in Medium or High quality. Write natural Twi, including `ɛ`, `ɔ`, numbers and acronyms; do not substitute letters or supply pronunciation symbols.

### TTS Voices

Fetch the live list any time: `GET /tts/voices.json`. Older short IDs and playground model IDs like `akua`, `en-ng-chioma`, `en-ng-chioma-whispering`, `swahili`, and `nigerian_pidgin_s` are still accepted as aliases, but new integrations should use the language-suffixed IDs below. For Twi, choose an explicit Medium, High or Lite ID from the table.

| Voice ID   | Name     | Language                  | Country  | Gender |
|------------|----------|---------------------------|----------|--------|
| `abena_twi_medium` | Abena Medium · Recommended | Twi (Akan) 🇬🇭 | Ghana | Female |
| `abena_twi_high` | Abena High | Twi (Akan) 🇬🇭 | Ghana | Female |
| `ama_twi_medium` | Ama Medium | Twi (Akan) 🇬🇭 | Ghana | Female |
| `ama_twi_high` | Ama High | Twi (Akan) 🇬🇭 | Ghana | Female |
| `yaa_twi_medium` | Yaa Medium | Twi (Akan) 🇬🇭 | Ghana | Female |
| `yaa_twi_high` | Yaa High | Twi (Akan) 🇬🇭 | Ghana | Female |
| `abena_twi_lite` | Abena Lite | Twi (Akan, lighter voice) 🇬🇭 | Ghana | Female |
| `kofi_twi_medium` | Kofi Medium | Twi (Akan) 🇬🇭 | Ghana | Male |
| `kofi_twi_high` | Kofi High | Twi (Akan) 🇬🇭 | Ghana | Male |
| `kobby_gpe_lite` | Kobby Lite · Fast | Ghanaian Pidgin English 🇬🇭 | Ghana | Male |
| `kobby_gpe_medium` | Kobby Medium | Ghanaian Pidgin English 🇬🇭 | Ghana | Male |
| `kobby_gpe_high` | Kobby High | Ghanaian Pidgin English 🇬🇭 | Ghana | Male |
| `akua_eng`     | Akua Lite · Fast | English (Ghanaian accent) 🇬🇭| Ghana | Female |
| `kwabena_eng`  | Kwabena Lite · Fast | English (Ghanaian accent) 🇬🇭| Ghana | Male |
| `akua_eng_medium` | Akua Medium | English (Ghanaian accent) 🇬🇭 | Ghana | Female |
| `akua_eng_high` | Akua High | English (Ghanaian accent) 🇬🇭 | Ghana | Female |
| `kwabena_eng_medium` | Kwabena Medium | English (Ghanaian accent) 🇬🇭 | Ghana | Male |
| `kwabena_eng_high` | Kwabena High | English (Ghanaian accent) 🇬🇭 | Ghana | Male |
| `chioma_eng`   | Chioma   | English (Nigerian accent, energetic) | Nigeria | Female |
| `chioma_whispering_eng` | Chioma | English (Nigerian accent, whispering) | Nigeria | Female |
| `mawuli_ewe`   | Mawuli   | Ewe                       | Ghana    | Male   |
| `james_pcm_lite` | James Lite · Fast | Nigerian Pidgin English | Nigeria | Male |
| `james_pcm_medium` | James Medium | Nigerian Pidgin English | Nigeria | Male |
| `james_pcm_high` | James High | Nigerian Pidgin English | Nigeria | Male |
| `amani_swh`    | Amani    | Swahili                   | Kenya    | Female |
| `abubakar_hau` | Abubakar | Hausa                     | Nigeria  | Male   |
| `folami_yor`   | Folami   | Yoruba                    | Nigeria  | Female |

---

### Abena, Ama and Yaa: Female Akan Twi

Each voice offers **Medium** (recommended balance) and **High** quality. Choose
the speaker and tier through `voice`; a separate `quality` field does not select it.
Requests retain the chosen voice/tier rather than silently changing to Lite.
On HTTP 503, wait for `Retry-After` before retrying.

`abena_twi_lite` remains available in the API and speech playground for lightweight
speech. New Web Studio podcasts and drama use Medium or High instead of Lite.
Existing High IDs remain valid; the additional voices do not change request or
response fields. Voice IDs and quality are recorded in the normal usage dashboard;
historical records are not relabelled.

### Kofi: Male Akan Twi

- `kofi_twi_medium`: the balanced-quality voice.
- `kofi_twi_high`: the highest-quality voice.

Kofi has no Lite version. Send normal Akan Twi text, including `ɛ` and `ɔ`;
the server handles pronunciation internally. Keep these
letters in your displayed text. Choose the tier through `voice`, not a separate
`quality` field. Requested tiers are not silently replaced with another voice;
on HTTP 503, wait for `Retry-After` before retrying.

### Ghana English Voice Tiers

Akua (female) and Kwabena (male) each offer:

- **Lite · Fast**: existing fast voices, using the unchanged IDs `akua_eng` and `kwabena_eng`.
- **Medium**: balanced quality, using `akua_eng_medium` and `kwabena_eng_medium`.
- **High**: highest quality, using `akua_eng_high` and `kwabena_eng_high`.

Choose the tier through `voice`, not a separate `quality` field. Existing aliases,
including `gh-eng-accent-medium_v3` and `gh-eng-accent-male-medium_v3`, still select
the original Lite voices; their historical names do not select the new Medium tier.
Requested Medium/High voices are never silently downgraded. On HTTP 503, respect
`Retry-After` and retry. The live voices endpoint lists installed options only.

### Ghana Pidgin Voice Tiers

**Lite · Fast** labels identify the existing fast voices. This is a
display-name change, not a new API identifier: keep using the IDs in the table.

- `kobby_gpe_lite`: the existing lightweight voice, displayed as **Kobby Lite · Fast**.
- `kobby_gpe_medium`: the compressed neural voice.
- `kobby_gpe_high`: the full-precision neural voice.

The legacy IDs `kobby_gpe`, `kobby`, and `gpe-medium_v1` still select **Lite**.
Despite its historical filename, `gpe-medium_v1` does not select the new Medium voice.
Responses and new inference logs use the explicit tier ID and a `quality` value
of `lite`, `medium`, or `high`. Existing historical logs are not rewritten.
Select a tier through `voice`; sending a separate `quality` field does not change it.
Requested tiers are never silently downgraded. On HTTP 503, wait for `Retry-After`
before retrying. Use natural Ghana Pidgin text; no Twi letter placeholders are needed.

### Nigerian Pidgin Voice Tiers

- `james_pcm_lite`: the existing lightweight voice, displayed as **James Lite · Fast**.
- `james_pcm_medium`: the conservatively compressed neural voice.
- `james_pcm_high`: the full-precision neural voice.

The legacy IDs `james_pcm`, `james`, `nigerian_pidgin_p`, and `nigerian_pidgin_s`
still select **Lite**. New responses and inference logs identify the explicit tier;
historical records stay unchanged. Choose through `voice`, not a separate `quality`
field. Requested tiers are never silently downgraded; on HTTP 503, wait for
`Retry-After` before retrying. Write natural Nigerian Pidgin; neural voices apply
the training text normalizer, including `₦` to "naira". Twi placeholders are not used.

## Speech Recognition

Send an audio file, get the text back. Upload the file as a form field named `audio_file` (`multipart/form-data`).

**Endpoint**

```
POST /asr/transcribe/
```

**Form fields**

| Field            | Required | Description |
|------------------|----------|-------------|
| `audio_file`     | yes      | Your audio file, up to **25 MB**. Twi and Pidgin High: 60 seconds. Ghanaian English and Ghana Pidgin Lite: 120 seconds. |
| `language`       | no       | `twi-en` (recommended), `twi-only`, `en`, `gpe`, `gpe-high`, or `pcm`. Default `twi-en`. |
| `reference_text` | no       | If you know the correct text, include it to also get accuracy/WER scores. |

Supported audio formats: WAV/PCM, MP3, M4A/AAC, FLAC, OGG, and other common formats. For predictable batch evaluations, use mono 16-bit PCM WAV at 16 kHz; files already in that format are used directly. Other valid files are normalized before transcription.

**Response (JSON)**

```json
{
  "text": "Mepɛ sɛ mede sika kɔ ma Kwame",
  "transcription": "Mepɛ sɛ mede sika kɔ ma Kwame",
  "language": "twi-en",
  "duration_seconds": 3.2,
  "credits_remaining": 9,
  "credit_limit": 10
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
| `twi-only` | Akan Twi (No English) 🇬🇭 | Ghana |
| `en`  | English (Ghanaian accent) 🇬🇭 | Ghana |
| `gpe` | Ghanaian Pidgin English · Lite 🇬🇭 | Ghana |
| `gpe-high` | Ghanaian Pidgin English · High 🇬🇭 | Ghana |
| `pcm` | Nigerian Pidgin English · High 🇳🇬 | Nigeria |

Use `twi-en` for Twi, English, and Twi-English code-switching. Choose `twi-only` only when the entire recording is spoken in Twi; English words may be missed. A `twi-only` response includes a short reminder in the `notice` field.

Use `gpe-high` for Ghanaian Pidgin or `pcm` for Nigerian Pidgin, including speech
that switches into English. Both use the same High recognition model. Existing
`gpe` and `pidgin` requests keep using Ghana Pidgin Lite; there is no Nigerian
Pidgin Lite option. The accepted `pcm-high` alias returns the canonical `pcm` code.
These High modes share Twi's bounded processing queue and the same ASR credit
allowance, not separate credits or extra parallel capacity. Busy responses include
a retry delay; respect it rather than sending duplicate requests.

---

## Errors & Limits

Errors return JSON with a helpful `message` (TTS) or `error` (ASR) field.

Free REST callers without an API key are limited to **20 requests per minute and
100 per hour per IP address**, in addition to their credit allowance. These rate
windows do not replenish credits. Respect `Retry-After` on HTTP 429; do not retry
in a tight loop. API-key rate ceilings remain 120/minute and 1,200/hour, subject
to credits and shared capacity; they are not a throughput guarantee.

The no-sign-in ASR allowance is **10 credits** in both the API and Playground;
ordinary signed-in ASR users currently receive **15 through the API** or **20 in the Playground**. These are configurable
allowances, not per-language grants or a promise of daily resets. Special grants
retain their own limits; use each response's credit fields as the authority.

The **TTS Playground** currently has a separate **20-credit lifetime trial**.
Past usage counts; the allowance does not refill monthly. Visitors sharing a
network may share the trial. Purchased credits and administrator grants are separate.

After the speech trial, [add prepaid credits](https://abena.mobobi.com/playground/credits/)
or [use Abena AI free on Android](https://play.google.com/store/apps/details?id=com.mobobi.abena).
Authenticated TTS uses the free allowance first, then purchased credit automatically.
No activation header is required, and your payment method is never charged automatically.
A request with insufficient combined credit returns HTTP 402. Guest TTS preserves its
existing HTTP 401 with `reason: free_allowance_exhausted`. Both return JSON links, not a
redirect that would send your input or API key to a payment provider. Speech
recognition remains free within its existing limits; TTS credits do not extend them.

**Both free and prepaid speech** are metered per normalized character (letters, spaces and punctuation):
0.02 credits for Lite, 0.04 for Medium and 0.06 for High. Credit packs are one-time
purchases in Ghana cedis; there is no subscription or expiry. See the
[credit page](https://abena.mobobi.com/playground/credits/) for current pack prices.

To use free and purchased credits on `POST /tts/synthesize/`, send your usual
text, voice and optional speed with your API key. The API limit remains 500
characters per request; Speech Playground remains 280. A request can use the
last fraction of free credit and charge only the remainder to purchased credit.
Failed generation returns both portions. Old usage and purchased balances are
not recalculated. ASR and Studio pricing are unchanged by TTS character metering.

For authenticated retries, include a unique `Idempotency-Key` for each new
generation (1–128 letters, digits, dots, underscores, colons or hyphens). Reuse
the same key and identical input for retries, including initially free requests.
Follow `Retry-After` while pending. You can also reuse a returned `billing_quote`
with the identical input. Do not start a new key when an outcome is unknown.
Guest requests do not support paid fallback or durable idempotent retries.

Responses expose `X-Free-Credits-Remaining` and, on the purchased/durable route,
`X-Purchased-Credits-Remaining`, `free_credits_used` and `purchased_credits_used`.
Without a key, each successful new request consumes its own character cost.

The older explicit purchased-only quote flow remains supported:

1. Authenticate with your API key and add `X-Abena-Use-Credits: confirmed`. Send
   the usual text, voice and optional speed. The first response is HTTP 402
   with `error: credit_confirmation_required`, the price in `quote.credits`,
   `can_afford`, and a signed `billing_quote`. No speech has been generated or charged.
2. After approving the price, resend the **same input and headers** with
   `billing_quote` added to the JSON body. On success, read `audio_base64`
   and `purchased_credits_used`.
3. If the status is pending, respect `Retry-After` and reuse the same quote
   and input. Do not request a fresh quote for an already confirmed job.

The public [Web Studio](https://abena.mobobi.com/playground/video-studio/) also
accepts these credits. Studio shows its price before you confirm. A short result
can cost less; a longer result cannot cost more than the displayed price. Failed
generations return reserved credits. Confirmed prepaid text-to-speech requests
take priority over waiting free speech requests. This does not interrupt active
work, guarantee an immediate start, or change speech-recognition limits.

Save the audio returned with your request. Optional dashboard audio copies share
a **5 GiB storage cap** and **5 GiB minimum free-disk reserve**. If either limit is
reached, normal API synthesis/transcription still returns its result, but a saved
audio copy may be unavailable. Older save-to-URL endpoints may return HTTP 503
without charging a credit. Existing expiry policies are unchanged; the dashboard
is not a permanent audio archive.

| Status      | Meaning            | What to do |
|-------------|--------------------|------------|
| `200`       | Success            | Use the result. |
| `400`       | Bad request        | Check fields (missing `text`, unknown `voice`, `speed` out of range). |
| `401`       | Authentication failed | Check the API key, or omit it to use the no-sign-in allowance. |
| `402`       | Credits used       | For TTS, [add credits](https://abena.mobobi.com/playground/credits/) or use the free mobile app. For ASR, check the remaining free allowance; buying credits does not extend it. |
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

