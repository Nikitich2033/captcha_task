import cv2
import numpy as np

# Load the image
im = cv2.imread('captcha_imgs/captcha_0.jpg')
assert im is not None, "File could not be read. Please check with os.path.exists()"

image = cv2.GaussianBlur(im, (3, 3),0)
ret, image = cv2.threshold(image, 90, 255, cv2.THRESH_BINARY)

image = cv2.dilate(image, np.ones((1, 3), np.uint8))
image = cv2.erode(image, np.ones((2,2), np.uint8))


im = image
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

# Apply thresholding
_, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY_INV)

# Apply morphological operations
kernel = np.ones((3,3),np.uint8)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# cv2.imshow("1", np.array(imgray))
# cv2.waitKey(0)

# Find contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# imgray = cv2.imread('captcha_0.jpg')
img_counter = 0 # initialize image counter

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

    # Check if width is significantly larger than height (this would mean there's probably more than one digit)
    if w > 1.5*h:
        # If so, split the ROI into two
        roi1 = imgray[y:y+h, x:x+w//2]
        roi2 = imgray[y:y+h, x+w//2:x+w]
        
        # Save each ROI as a separate image
        cv2.imwrite(f'digit_{img_counter}.png', roi1)
        img_counter += 1
        cv2.imwrite(f'digit_{img_counter}.png', roi2)
        img_counter += 1
    else:
    # Extract ROI
        roi = imgray[y:y+h, x:x+w]

        # Save the ROI as an image
        cv2.imwrite(f'digit_{img_counter}.png', roi)
        img_counter += 1
