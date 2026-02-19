from app.services.sarvam_client import sarvam_tts
from app.services.gemini_client import gemini_chat

LANG_MAP = {
    "hi-IN": "Hindi",
    "ta-IN": "Tamil",
    "te-IN": "Telugu",
    "kn-IN": "Kannada",
    "ml-IN": "Malayalam",
    "mr-IN": "Marathi",
    "gu-IN": "Gujarati",
    "bn-IN": "Bengali"
}

def generate_audio(state):
    text = state["summary"]["final_summary"]
    language_code = state.get("language_code", "en-IN")
    speaker = state.get("speaker", "anushka")
    path = "audio/summary.mp3"

    # Translate if target language is not English
    if language_code != "en-IN" and language_code in LANG_MAP:
        target_lang = LANG_MAP[language_code]
        print(f"DEBUG: Translating summary to {target_lang}...")
        translation_prompt = f"Translate the following legal summary into {target_lang}. Keep the tone professional and natural for audio reading:\n\n{text}"
        try:
            translated_text = gemini_chat(translation_prompt)
            print(f"DEBUG: Translation successful. Input chars: {len(text)}, Output chars: {len(translated_text)}")
            text = translated_text
        except Exception as e:
            print(f"DEBUG: Translation failed, falling back to English: {str(e)}")

    sarvam_tts(text, path, target_language_code=language_code, speaker=speaker)

    state["audio_path"] = path
    return state
