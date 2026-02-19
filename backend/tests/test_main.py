import pytest
import json
import io

def test_upload_flow(client, mock_gemini, mock_sarvam):
    # Setup mocks
    mock_gemini["extract"].return_value = json.dumps({"clauses": [{"category": "L", "risk_level": "low", "text": "...", "summary": "..."}]})
    mock_gemini["risk"].return_value = json.dumps({"hidden_risks": [], "warnings": []})
    
    # We need to mock proscons agent as well (it's called in build_graph)
    with patch("app.agents.proscons_agent.gemini_chat") as mock_pc:
        mock_pc.return_value = json.dumps({"pros": [], "cons": []})
        
        mock_gemini["summary"].return_value = json.dumps({
            "fairness_score": 5,
            "final_summary": "Test Summary",
            "key_takeaways": [],
            "recommendation": "None"
        })
        
        # Create a dummy file for upload
        file_content = b"PDF dummy content"
        file = (io.BytesIO(file_content), "test.pdf")
        
        # Mock the parser to avoid real pdfplumber call
        with patch("app.services.parser.extract_text") as mock_parser:
            mock_parser.return_value = "Extracted text content"
            
            response = client.post("/upload", files={"file": file})
            
            assert response.status_code == 200
            data = response.json()
            assert data["final_summary"] == "Test Summary"
            assert "audio_url" in data

from unittest.mock import patch
