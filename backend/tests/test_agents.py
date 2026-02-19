import json
from app.agents.extract_agent import extract_clauses
from app.agents.risk_agent import analyze_risk
from app.agents.summary_agent import generate_summary

def test_extract_agent(mock_gemini):
    mock_gemini["extract"].return_value = json.dumps({
        "clauses": [{"category": "Data", "risk_level": "low", "text": "...", "summary": "..."}]
    })
    
    state = {"text": "Original document text"}
    result = extract_clauses(state)
    
    assert "clauses" in result
    assert result["clauses"][0]["category"] == "Data"

def test_risk_agent(mock_gemini):
    mock_gemini["risk"].return_value = json.dumps({
        "hidden_risks": ["Risk 1"],
        "warnings": ["Warning 1"]
    })
    
    state = {"clauses": []}
    result = analyze_risk(state)
    
    assert "risks" in result
    assert result["risks"]["hidden_risks"] == ["Risk 1"]

def test_summary_agent(mock_gemini):
    mock_gemini["summary"].return_value = json.dumps({
        "fairness_score": 8,
        "final_summary": "Summary text",
        "key_takeaways": ["T1"],
        "recommendation": "Rec"
    })
    
    state = {"clauses": [], "risks": {}, "pros_cons": {}}
    result = generate_summary(state)
    
    assert "summary" in result
    assert result["summary"]["fairness_score"] == 8
