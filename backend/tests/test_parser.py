import pytest
import os
from app.services.parser import extract_text
from unittest.mock import MagicMock

def test_extract_text_pdf():
    # Mocking parser since we don't want to rely on real files for basic tests
    # However, parser.py uses pdfplumber directly. 
    # Let's see if we can use a small real file or mock the library.
    # For now, let's mock the 'file' object passed to extract_text
    
    file_mock = MagicMock()
    file_mock.filename = "test.pdf"
    
    with patch("app.services.parser.pdfplumber.open") as mock_pdf:
        mock_pdf.return_value.__enter__.return_value.pages = [
            MagicMock(extract_text=lambda: "Test PDF Content")
        ]
        text = extract_text(file_mock)
        assert "Test PDF Content" in text

def test_extract_text_docx():
    file_mock = MagicMock()
    file_mock.filename = "test.docx"
    
    with patch("app.services.parser.Document") as mock_doc:
        mock_doc.return_value.paragraphs = [
            MagicMock(text="Test DOCX Content")
        ]
        text = extract_text(file_mock)
        assert "Test DOCX Content" in text

from unittest.mock import patch
