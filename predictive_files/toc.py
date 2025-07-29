import fitz  
import pytesseract
from PIL import Image
import os



def extract_text_from_pdf(files):
    """Extract text from a PDF file."""
    text = ''
    for file in files:
        docs = fitz.open(file)
        for page in  docs:
            text += page.get_text()

    return text.split()

def extract_text_from_image(images):
    """Extract text from an image using OCR."""
    image = Image.open(images)
    text = pytesseract.image_to_string(image)
    return text.strip()

def llm(text):
    """Placeholder function for LLM processing. Replace with actual logic."""
    prompt = f"Process this academic content:\n{text}"
    result = llm(prompt)
    return result

def save_in_txt(text , filename):
    """Save processed text to a .txt file."""
    with open(filename , 'w' , encoding='uft8') as f:
        f.write(text)



def extract_text_from_file4(file_path):
    """Processes a file (PDF or image), extracts text using OCR or PDF parsing,
    checks for a valid code 'C109513(022)', and if valid, processes it with LLM
    and saves the final text into 'toc.txt'.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext in ['.jpg', '.jpeg', '.png', '.bmp']:
        text = extract_text_from_image(file_path)
    else:
        raise ValueError("unsupportated file brother")
    
    if "C109513(022)" not in text:
        print("'C109513(022)' not found in the document. Skipping save.")
        return None
    
    processed_text = llm(text)

    save_in_txt(processed_text, 'toc.txt')
    print("Text saved ")
    return processed_text