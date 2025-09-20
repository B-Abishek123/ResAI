import fitz  # PyMuPDF
import docx

def parse_pdf(file_bytes):
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def parse_docx(file_bytes):
    doc = docx.Document(file_bytes)
    return " ".join([p.text for p in doc.paragraphs])

def parse_resume(file_bytes):
    try:
        return parse_pdf(file_bytes)
    except:
        return parse_docx(file_bytes)

def parse_jd(file_bytes):
    return file_bytes.decode("utf-8")  # assuming JD is plain text
