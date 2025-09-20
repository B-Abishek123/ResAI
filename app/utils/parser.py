# app/utils/parser.py
import io
import re
from typing import Optional
import sys
print(f"🐍 Script is running with this Python interpreter: {sys.executable}")
# pdfplumber for PDF parsing (no fitz)
try:
    import pdfplumber
except Exception:
    pdfplumber = None

# python-docx for docx parsing
# from docx import Document


def _clean_text(text: str) -> str:
    """Basic whitespace normalization and strip."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def parse_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF bytes using pdfplumber."""
    if pdfplumber is None:
        raise RuntimeError("pdfplumber is not installed")
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return _clean_text("\n".join(text_parts))


def parse_txt(file_bytes: bytes) -> str:
    """Decode txt bytes with multiple codecs as fallback."""
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            return _clean_text(file_bytes.decode(enc))
        except Exception:
            continue
    return _clean_text(file_bytes.decode("utf-8", errors="ignore"))


def parse_resume(file_bytes: bytes, filename: Optional[str] = None) -> str:
    """
    Generic resume/JD parser.
    - Uses extension if available (pdf/docx/txt)
    - Falls back: pdf -> docx -> txt
    """
    ext = (filename or "").lower().split('.')[-1]
    try:
        if ext == "pdf":
            return parse_pdf(file_bytes)
        if ext in ("txt", "md"):
            return parse_txt(file_bytes)

        # unknown extension: try best-effort
        try:
            return parse_pdf(file_bytes)
        except Exception:
            pass
        try:
            #return parse_docx(file_bytes)
            pass
        except Exception:
            pass
        return parse_txt(file_bytes)

    except Exception as e:
        # ultimate fallback: try decode and return trimmed text
        try:
            raw = file_bytes.decode("utf-8", errors="ignore")
        except Exception:
            raw = str(file_bytes)
        return _clean_text(raw)
