import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import MagicMock, patch

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_gemini():
    with patch("app.agents.extract_agent.gemini_chat") as mock_extract, \
         patch("app.agents.risk_agent.gemini_chat") as mock_risk, \
         patch("app.agents.proscons_agent.gemini_chat") as mock_proscons, \
         patch("app.agents.summary_agent.gemini_chat") as mock_summary:
        
        yield {
            "extract": mock_extract,
            "risk": mock_risk,
            "proscons": mock_proscons,
            "summary": mock_summary
        }

@pytest.fixture
def mock_sarvam():
    with patch("app.agents.tts_agent.sarvam_tts") as mock:
        yield mock
