from pathlib import Path
from pypdf import PdfReader


def load_pdf(file_path: str) -> str:
    """Extract all text from a PDF file.

    Args:
        file_path: Path to the PDF file.

    Returns:
        All text content from the PDF as a single string.

    Raises:
        FileNotFoundError: If the PDF file doesn't exist.
    """
    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text