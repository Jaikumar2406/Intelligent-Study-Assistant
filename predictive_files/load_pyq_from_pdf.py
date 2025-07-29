import fitz 
import re
from collections import Counter, defaultdict
from transformers import pipeline
from update import text_extracter_pdf


def load_pyqs_from_pdf(pdf_path):
    text = text_extracter_pdf(pdf_path)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    pyqs = defaultdict(list)
    current_unit = None
    for line in lines:
        m = re.match(r'^(Unit\s+\d+)\s*[:\-]?', line, re.IGNORECASE)
        if m:
            current_unit = m.group(1)
        elif current_unit:
            pyqs[current_unit].append(line)
    return pyqs