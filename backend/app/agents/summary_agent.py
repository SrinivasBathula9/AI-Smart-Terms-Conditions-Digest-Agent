from app.services.gemini_client import gemini_chat, clean_json_response
import json


def generate_summary(state):
    clauses = state["clauses"]
    risks = state["risks"]
    pros_cons = state["pros_cons"]

    prompt = f"""
Create a final digest.

Return strict JSON:
{{
 "fairness_score": 1-10,
 "final_summary": "",
 "key_takeaways": [],
 "recommendation": ""
}}

Clauses:
{clauses}

Risks:
{risks}

Pros/Cons:
{pros_cons}
"""

    response = gemini_chat(prompt)

    try:
        clean_json = clean_json_response(response)
        data = json.loads(clean_json)
    except Exception as e:
        print(f"ERROR in generate_summary parsing: {str(e)}")
        data = {
            "fairness_score": 5,
            "final_summary": response,
            "key_takeaways": [],
            "recommendation": ""
        }

    state["summary"] = data
    return state
