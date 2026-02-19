from app.services.gemini_client import gemini_chat, clean_json_response
import json


def generate_pros_cons(state):
    clauses = state["clauses"]

    prompt = f"""
Based on these clauses, generate pros and cons.

Return strict JSON:
{{
 "pros": [],
 "cons": []
}}

Clauses:
{clauses}
"""

    response = gemini_chat(prompt)

    try:
        clean_json = clean_json_response(response)
        data = json.loads(clean_json)
    except Exception as e:
        print(f"ERROR in generate_pros_cons parsing: {str(e)}")
        data = {"pros": [], "cons": []}

    state["pros_cons"] = data
    return state
