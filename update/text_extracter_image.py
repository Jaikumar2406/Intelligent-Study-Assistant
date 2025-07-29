from PIL import Image
import pytesseract
import os

def text_extracter_image(images):
    image = Image.open(images)
    text = pytesseract.image_to_string(image)
    return text.strip() 