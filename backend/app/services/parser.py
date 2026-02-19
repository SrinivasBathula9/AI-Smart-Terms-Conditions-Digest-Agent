import pdfplumber
from docx import Document
from bs4 import BeautifulSoup
import io


def extract_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def extract_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])


def extract_txt(file):
    return file.read().decode("utf-8")


def extract_html(file):
    content = file.read().decode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    return soup.get_text(separator="\n")


def extract_text(upload_file):
    filename = upload_file.filename.lower()

    file_bytes = upload_file.file.read()
    file_stream = io.BytesIO(file_bytes)

    if filename.endswith(".pdf"):
        return extract_pdf(file_stream)

    elif filename.endswith(".docx"):
        return extract_docx(file_stream)

    elif filename.endswith(".txt"):
        return extract_txt(file_stream)

    elif filename.endswith(".html"):
        return extract_html(file_stream)

    else:
        raise ValueError("Unsupported file format")
