import fitz

def extract_text_from_pdf(files):
    text = ''
    for file in files:
        docs = fitz.open(file)
        for page in  docs:
            text += page.get_text()

    return text.split()