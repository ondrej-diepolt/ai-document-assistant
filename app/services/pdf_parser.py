import fitz  # PyMuPDF


def extract_pages(data: bytes) -> list[str]:
    with fitz.open(stream=data, filetype="pdf") as document:
        return [page.get_text() for page in document]


def extract_text_from_pdf(data: bytes) -> str:
    return "\n".join(extract_pages(data))