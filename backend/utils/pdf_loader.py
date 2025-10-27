from PyPDF2 import PdfReader


def load_pdf_text(file_path: str) -> str:
    reader = PdfReader(file_path)
    texts = []
    for page in reader.pages:
        txt = page.extract_text()
        if txt:
            texts.append(txt)
    return "\n".join(texts)