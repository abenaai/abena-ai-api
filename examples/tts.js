// Abena AI — Text-to-Speech example (Node.js 18+ or the browser).
// No API key needed (uses the free tier).
//
// Run in Node:  node tts.js

const API = "https://abena.mobobi.com/playground/api/v1/tts/synthesize/";

async function synthesize(text, voice = "akua_eng", speed = 1.0, apiKey = null) {
  const headers = { "Content-Type": "application/json" };
  if (apiKey) headers["Authorization"] = `Bearer ${apiKey}`;

  const res = await fetch(API, {
    method: "POST",
    headers,
    body: JSON.stringify({ text, voice, speed }),
  });
  const data = await res.json();

  if (!res.ok || data.status !== "success") {
    throw new Error(data.message || data.error || `HTTP ${res.status}`);
  }
  return data; // { audio_base64, duration_seconds, mime_type, ... }
}

// --- Browser: play it directly ---
// const data = await synthesize("Hello!", "akua_eng");
// new Audio("data:audio/wav;base64," + data.audio_base64).play();

// --- Node.js: save it to a file ---
if (typeof window === "undefined") {
  const fs = require("fs");
  synthesize("Akwaaba, wo ho te sen?", "abena_twi")
    .then((data) => {
      fs.writeFileSync("speech.wav", Buffer.from(data.audio_base64, "base64"));
      console.log(`Saved speech.wav (${data.duration_seconds}s of audio)`);
    })
    .catch((err) => console.error("Error:", err.message));
}
