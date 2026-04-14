import pytesseract
from PIL import Image
import pdfplumber
from docx import Document

def read_image(file):
    img = Image.open(file)
    return pytesseract.image_to_string(img)

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def read_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def read_txt(file):
    return file.read().decode("utf-8")