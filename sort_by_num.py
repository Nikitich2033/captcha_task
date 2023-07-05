import cv2
import os
import pytesseract
import shutil

# Specify the path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Directory containing the images
dir_name = "single_digits"

# Directory to save the digits
digits_dir = "sorted_by_num"

# List all files in directory
files = os.listdir(dir_name)

# Loop over the files
for file in files:
    # Construct full file path
    file_path = os.path.join(dir_name, file)
    
    # Read the image
    img = cv2.imread(file_path)
    
    # Perform OCR with data output
    data = pytesseract.image_to_data(img, config='--psm 10 -c tessedit_char_whitelist=0123456789', output_type=pytesseract.Output.DICT)

    # Iterate over each detected character
    for i in range(len(data['text'])):
        # Get the recognized character
        digit = data['text'][i].strip()
        
        # Skip empty strings and non-digit characters
        if digit == '' or not digit.isdigit():
            continue
        
        # Get the confidence level
        confidence = int(data['conf'][i])
        
        # Check if confidence level is above 60
        if confidence > 85 and len(digit) == 1:
            # Create the digits directory if it doesn't exist
            if not os.path.exists(digits_dir):
                os.makedirs(digits_dir)
            
            # Create the digit-specific directory if it doesn't exist
            digit_dir = os.path.join(digits_dir, digit)
            if not os.path.exists(digit_dir):
                os.makedirs(digit_dir)
            
            # Save the image to the appropriate folder
            filename = os.path.splitext(file)[0] + f"_digit{i}.jpg"
            save_path = os.path.join(digit_dir, filename)
            cv2.imwrite(save_path, img)

            # Print the digit and confidence level
            print(f"Saved digit {digit} from file {file} with confidence {confidence}")
