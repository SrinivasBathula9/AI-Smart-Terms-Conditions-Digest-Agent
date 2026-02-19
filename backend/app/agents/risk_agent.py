from app.services.gemini_client import gemini_chat, clean_json_response
import json


def analyze_risk(state):
    clauses = state["clauses"]

    prompt = f"""
Analyze these clauses and identify:

1. Hidden risks
2. Penalties
3. User disadvantages

Return strict JSON:
{{
  "hidden_risks": [],
  "warnings": []
}}

Clauses:
{clauses}
"""

    response = gemini_chat(prompt)

    try:
        clean_json = clean_json_response(response)
        data = json.loads(clean_json)
    except Exception as e:
        print(f"ERROR in analyze_risk parsing: {str(e)}")
        data = {"hidden_risks": [], "warnings": []}

    state["risks"] = data
    return state
