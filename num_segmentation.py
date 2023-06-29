import cv2
import numpy as np

# Load the image
im = cv2.imread('captcha.jpg')
assert im is not None, "File could not be read. Please check with os.path.exists()"

# Convert to grayscale
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

# Apply thresholding
_, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY_INV)

# Apply morphological operations
kernel = np.ones((3,3),np.uint8)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# Find contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterate through each contour found
for i, contour in enumerate(contours):
    # Get bounding box for each contour
    x, y, w, h = cv2.boundingRect(contour)

    # Add padding around the bounding box
    padding = 5
    x = max(0, x - padding)
    y = max(0, y - padding)
    w = min(im.shape[1], x + w + padding) - x
    h = min(im.shape[0], y + h + padding) - y

    # Extract ROI
    roi = imgray[y:y+h, x:x+w]

    # Save each ROI as a separate image
    cv2.imwrite(f'digit_{i}.png', roi)
