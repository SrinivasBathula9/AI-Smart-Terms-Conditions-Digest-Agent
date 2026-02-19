import os
import google.generativeai as genai
from dotenv import load_dotenv

def load_env_vars():
    # Use absolute path of the current file to find root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while current_dir != os.path.dirname(current_dir): # stop at root
        if ".env" in os.listdir(current_dir):
            print(f"DEBUG: Found .env in {current_dir}")
            load_dotenv(os.path.join(current_dir, ".env"), override=True)
            return True
        current_dir = os.path.dirname(current_dir)
    return False

print("--- Diagnostics Start ---")
if load_env_vars():
    print("DEBUG: Successfully loaded .env")
else:
    print("DEBUG: Failed to find .env")

# Standardize names
google_key = os.getenv("GOOGLE_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")
google_space_key = os.getenv("GOOGLE API KEY")

print(f"GOOGLE_API_KEY: {google_key[:10]}..." if google_key else "GOOGLE_API_KEY: Not Set")
print(f"GEMINI_API_KEY: {gemini_key[:10]}..." if gemini_key else "GEMINI_API_KEY: Not Set")
print(f"GOOGLE API KEY: {google_space_key[:10]}..." if google_space_key else "GOOGLE API KEY: Not Set")

api_key = google_key or gemini_key or google_space_key

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        print("DEBUG: Attempting connection...")
        response = model.generate_content("Say 'OK'")
        print(f"SUCCESS: {response.text}")
    except Exception as e:
        print(f"FAILURE: {str(e)}")
else:
    print("FAILURE: No API key found in prioritized environment variables")
