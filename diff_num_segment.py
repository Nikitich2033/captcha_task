import cv2
import numpy as np
import os

#Load image and convert to grey.
img = cv2.imread('captcha_imgs/captcha_65.jpg', 0)

# From RGB to BW
# Adaptive thresholding
th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 17, 2)

# Otsu thresholding
ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Otsu thresholding with Gaussian Blur
blur = cv2.GaussianBlur(img, (5, 5), 0)
ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

kernel = np.ones((3,3), np.uint8)

dilation = cv2.dilate(th3, kernel, iterations=1)

erosion = cv2.erode(dilation, kernel, iterations=1)

kernel = np.ones((3,1), np.uint8)
dilation = cv2.dilate(erosion, kernel, iterations=1)

# Prepare output directory
os.makedirs("output", exist_ok=True)

#Get the individual letters.
x, y, w, h = 22, 10, 20, 38
for  i in range(6):
    # # get the bounding rect
    # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # cv2.rectangle(dilation, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # save each character to a separate image
    digit = img[y:y+h, x:x+w]

    # Add 5-pixel white padding
    digit = cv2.copyMakeBorder(digit, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=[255, 255, 255])

    cv2.imwrite(f'output/char_{i}.png', digit)
    x += w