import os
import requests
import base64
from dotenv import load_dotenv

# Robustly find and load the .env file from the project root
def load_env_vars():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while current_dir != os.path.dirname(current_dir): # stop at root
        if ".env" in os.listdir(current_dir):
            load_dotenv(os.path.join(current_dir, ".env"), override=True)
            return True
        current_dir = os.path.dirname(current_dir)
    return False

load_env_vars()

def split_text(text: str, limit: int = 500):
    """
    Splits text into chunks of at most 'limit' characters, ideally at sentence boundaries.
    """
    if len(text) <= limit:
        return [text]
    
    chunks = []
    while text:
        if len(text) <= limit:
            chunks.append(text)
            break
            
        # Try to find last sentence end within limit
        split_at = -1
        for punct in [". ", "? ", "! ", "\n"]:
            pos = text.rfind(punct, 0, limit)
            if pos > split_at:
                split_at = pos + len(punct)
        
        # Fallback to space if no sentence boundary
        if split_at == -1:
            split_at = text.rfind(" ", 0, limit)
            
        # Hard break if no space
        if split_at == -1:
            split_at = limit
            
        chunks.append(text[:split_at].strip())
        text = text[split_at:].strip()
    
    return chunks

def sarvam_tts(text: str, output_path: str, target_language_code: str = "en-IN", speaker: str = "anushka"):
    """
    Calls Sarvam AI TTS API to generate real audio.
    Handles text > 500 chars by splitting and concatenating response chunks.
    """
    api_key = os.getenv("SARVAM_API_KEY")
    if not api_key:
        print("DEBUG: SARVAM_API_KEY not found in environment")
        return None

    url = "https://api.sarvam.ai/text-to-speech"
    
    # Split text into chunks to respect per-string limit
    text_chunks = split_text(text, limit=480) # Safe margin
    
    payload = {
        "inputs": text_chunks,
        "target_language_code": target_language_code,
        "speaker": speaker,
        "model": "bulbul:v2"
    }
    
    headers = {
        "api-subscription-key": api_key,
        "Content-Type": "application/json"
    }

    print(f"DEBUG: Calling Sarvam TTS for {len(text)} chars in {len(text_chunks)} chunks...")
    try:
        combined_audio = b""
        
        # Sarvam API allows max 3 items in the 'inputs' list per request
        for i in range(0, len(text_chunks), 3):
            batch = text_chunks[i:i+3]
            print(f"DEBUG: Processing batch {i//3 + 1} ({len(batch)} chunks)...")
            
            payload = {
                "inputs": batch,
                "target_language_code": target_language_code,
                "speaker": speaker,
                "model": "bulbul:v2"
            }
            
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code != 200:
                print(f"DEBUG: Sarvam API Failed ({response.status_code}): {response.text}")
                response.raise_for_status()
            
            data = response.json()
            audios = data.get("audios", [])
            for audio_base64 in audios:
                if audio_base64:
                    combined_audio += base64.b64decode(audio_base64)

        if combined_audio:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(combined_audio)
            print(f"DEBUG: Successfully wrote {len(combined_audio)} bytes to {output_path}")
            return output_path
        else:
            print(f"DEBUG: No audio content in Sarvam response batching")
            return None
            
    except Exception as e:
        print(f"DEBUG: Exception in Sarvam TTS: {str(e)}")
        if os.path.exists(output_path):
            os.remove(output_path)
        return None
