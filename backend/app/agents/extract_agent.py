from app.services.gemini_client import gemini_chat, clean_json_response
import json


def extract_clauses(state):
    text = state["text"][:12000]

    prompt = f"""
You are a legal assistant AI.

Extract clauses from this terms document.

Return strict JSON:
{{
  "clauses": [
    {{
      "category": "",
      "risk_level": "low|medium|high",
      "text": "",
      "summary": ""
    }}
  ]
}}

Document:
{text}
"""

    response = gemini_chat(prompt)

    try:
        clean_json = clean_json_response(response)
        data = json.loads(clean_json)
    except Exception as e:
        print(f"ERROR in extract_clauses parsing: {str(e)}")
        data = {"clauses": []}

    state["clauses"] = data.get("clauses", [])
    return state
