from pytesseract import pytesseract
from PIL.Image import Image





def image_to_text_digit(img:Image) -> str:
    pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    return pytesseract.image_to_string(img, config='-c tessedit_char_whitelist=0123456789-,')

def image_to_text_fr(img:Image) -> str:
    pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    return pytesseract.image_to_string(img, config='-c tessedit_char_whitelist= abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123469âêîûéèàï-,-É')
