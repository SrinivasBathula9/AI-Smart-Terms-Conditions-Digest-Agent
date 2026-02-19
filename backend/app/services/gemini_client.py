from dotenv import load_dotenv
import google.generativeai as genai
import os

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

# Select the most appropriate key, prioritizing GOOGLE_API_KEY as it's the standard for Gemini
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE API KEY")
genai.configure(api_key=api_key)

MODEL = "gemini-3-flash-preview"


def gemini_chat(prompt: str) -> str:
    try:
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"DEBUG: Gemini API Error: {str(e)}")
        raise e


def clean_json_response(text: str) -> str:
    """Extracts JSON content from potentially markdown-wrapped text."""
    text = text.strip()
    if "```json" in text:
        text = text.split("```json")[-1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[-1].split("```")[0]
    return text.strip()
