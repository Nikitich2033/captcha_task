# import cv2
# import os
# import pytesseract
# import numpy as np 

# # Specify the path to tesseract 
# pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# def process_captcha(image_path):
#     # 1. Convert image to grayscale
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # 2. Threshold the image to reveal the digits
#     _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

#     # 3. Find contours in the image
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  
#     # cv2.imshow("1", np.array(thresh))
#     # cv2.waitKey(0)

#     image_digits = []
#     for idx, contour in enumerate(contours):
#         # 4. Get the bounding box of contour
#         x, y, w, h = cv2.boundingRect(contour)
        
#         # Filter small contours based on area
#         area = cv2.contourArea(contour)
#         if area > 50:
#             print("Area >50")
#             # Get ROI of the contour
#             roi = gray[y:y+h, x:x+w]
#             cv2.imshow("1", np.array(roi))
#             cv2.waitKey(0)
#             # Recognize digit using pytesseract
#             digit = pytesseract.image_to_string(roi, config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
#             print(f"Len of digit: {len(digit)}")
#             # If the recognized digit length is 1, save it to corresponding folder
#             if len(digit) == 1:
#                 print("Found digit")
#                 # Create the directory if it doesn't exist
#                 os.makedirs(f'digits/{digit}', exist_ok=True)
                
#                 # Save each ROI (digit image) to the corresponding directory
#                 cv2.imwrite(f'digits/{digit}/digit_{idx}.png', roi)
#                 image_digits.append(roi)

#     return image_digits

# process_captcha('46.png')

import cv2,numpy,pytesseract
def getNumber(image):

    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Otsu Tresholding automatically find best threshold value
    _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    
    # invert the image if the text is white and background is black
    count_white = numpy.sum(binary_image > 0)
    count_black = numpy.sum(binary_image == 0)
    if count_black > count_white:
        binary_image = 255 - binary_image
        
    # padding
    final_image = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    txt = pytesseract.image_to_string(
        final_image, config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
    
    print(len(txt))

    return txt

image = cv2.imread("46.png")
getNumber(cv2.imread("test.png"))