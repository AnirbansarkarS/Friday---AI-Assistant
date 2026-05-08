"""
Extracts raw text from PDF and plain-text files.
"""

from PyPDF2 import PdfReader


def load_pdf(path: str) -> str:
    """Extract text from all pages of a PDF file."""
    try:
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF '{path}': {e}")


def load_txt(path: str) -> str:
    """Read a plain-text or markdown file."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception as e:
        raise Exception(f"Error reading text file '{path}': {e}")
