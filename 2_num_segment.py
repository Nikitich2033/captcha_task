import cv2
import numpy as np
import os

# Подготовка директории для сохранения
os.makedirs("single_digits", exist_ok=True)

# Получение списка всех файлов с изображениями в папке captcha_imgs
captcha_dir = "captcha_imgs"
image_files = os.listdir(captcha_dir)

# Перебор каждого файла с изображением
for image_file in image_files:
    # Загрузка изображения и преобразование в оттенки серого
    image_path = os.path.join(captcha_dir, image_file)
    img = cv2.imread(image_path, 0)

    # Обработка изображения
    # Преобразование из RGB в оттенки серого
    # Адаптивная бинаризация
    th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 17, 2)

    # Оцу-бинаризация
    ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Оцу-бинаризация с гауссовым размытием
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    kernel = np.ones((3,3), np.uint8)

    dilation = cv2.dilate(th3, kernel, iterations=1)

    erosion = cv2.erode(dilation, kernel, iterations=1)

    kernel = np.ones((3,1), np.uint8)
    dilation = cv2.dilate(erosion, kernel, iterations=1)

    # Получение отдельных букв
    x, y, w, h = 22, 10, 20, 38
    for i in range(6):
        # Получение ограничивающего прямоугольника

        # Сохранение каждого символа в отдельное изображение
        # Измените dilation на img, если вы хотите сохранить оригинальный цвет
        digit = dilation[y:y+h, x:x+w]

        # Добавление 5 пикселей белой рамки
        digit = cv2.copyMakeBorder(digit, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=[255, 255, 255])

        # Сохранение изображения символа
        output_path = os.path.join("single_digits", f"{image_file}_{i}.png")
        cv2.imwrite(output_path, digit)

        x += w

