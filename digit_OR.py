import cv2
import os
import pytesseract

# Specify the path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Directory containing the images
dir_name = "output"

# List all files in directory
files = os.listdir(dir_name)

# Loop over the files
for file in files:
    # Construct full file path
    file_path = os.path.join(dir_name, file)
    
    # Read the image
    img = cv2.imread(file_path)
    
    # Perform OCR
    digit = pytesseract.image_to_string(img, config='--psm 10 -c tessedit_char_whitelist=0123456789')

    # Print the recognized digit
    print(f"File: {file}, recognized digit: {digit.strip()}")