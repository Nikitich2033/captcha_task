import cv2
import numpy as np

# Загрузка изображения
im = cv2.imread('captcha_imgs/captcha_0.jpg')
assert im is not None, "Файл не может быть прочитан."

image = cv2.GaussianBlur(im, (3, 3), 0)
ret, image = cv2.threshold(image, 90, 255, cv2.THRESH_BINARY)

image = cv2.dilate(image, np.ones((1, 3), np.uint8))
image = cv2.erode(image, np.ones((2, 2), np.uint8))

im = image
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

# Применение порогового значения
_, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY_INV)

# Применение морфологических операций
kernel = np.ones((3, 3), np.uint8)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# Найти контуры
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

img_counter = 0  # инициализация счетчика изображений

# Перебор найденных контуров
for i, contour in enumerate(contours):
    # Получение ограничивающего прямоугольника для каждого контура
    x, y, w, h = cv2.boundingRect(contour)

    # Добавление отступа вокруг ограничивающего прямоугольника
    padding = 5
    x = max(0, x - padding)
    y = max(0, y - padding)
    w = min(im.shape[1], x + w + padding) - x
    h = min(im.shape[0], y + h + padding) - y

    # Проверка, что ширина значительно больше высоты (это означает, что, скорее всего, есть более одной цифры)
    if w > 1.5 * h:
        # Если так, разделите ROI на две части
        roi1 = imgray[y:y + h, x:x + w // 2]
        roi2 = imgray[y:y + h, x + w // 2:x + w]
        
        # Сохранение каждого ROI в отдельное изображение
        cv2.imwrite(f'digit_{img_counter}.png', roi1)
        img_counter += 1
        cv2.imwrite(f'digit_{img_counter}.png', roi2)
        img_counter += 1
    else:
        # Извлечение ROI
        roi = imgray[y:y + h, x:x + w]

        # Сохранение ROI в качестве изображения
        cv2.imwrite(f'digit_{img_counter}.png', roi)
        img_counter += 1
