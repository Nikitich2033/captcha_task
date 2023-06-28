import cv2
import numpy as np

# Загрузка изображения
image = cv2.imread('captcha.jpg')

# Конвертация изображения в оттенки серого
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Применение пороговой функции
_, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

# Применение морфологической операции дилатация
kernel = np.ones((2,2),np.uint8)
dilated = cv2.dilate(thresh, kernel, iterations = 1)

# Нахождение контуров на изображении
contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

digit_images = []

# Для каждого контура
for contour in contours:
    # Нахождение прямоугольника, описывающего контур
    x, y, w, h = cv2.boundingRect(contour)

    # Выделение ROI (region of interest)
    roi = gray[y:y+h, x:x+w]

    # Сохранение ROI в список
    digit_images.append(roi)

# Сохранение полученных изображений
for i, digit_image in enumerate(digit_images):
    cv2.imwrite(f'digit_{i}.jpg', digit_image)
