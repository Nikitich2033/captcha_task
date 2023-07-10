from tensorflow.keras.models import load_model
import cv2
import numpy as np
from flask import Flask, request, jsonify
import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)

mnist_model = load_model("mnist_model.h5")  

def segment_img(input_img):
    # Преобразование изображения PIL в массив NumPy
    image_array = np.array(input_img)
    
    # Обработка изображения
    # Преобразование в оттенки серого
    img = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    
    # Адаптивная бинаризация
    th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 17, 2)

    # Оцу-бинаризация с гауссовым размытием
    blur = cv2.GaussianBlur(th, (5, 5), 0)
    _, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    kernel = np.ones((3, 3), np.uint8)

    dilation = cv2.dilate(th3, kernel, iterations=1)


    # Получение отдельных символов
    x, y, w, h = 22, 10, 20, 38
    segments = []
    for i in range(6):
        # Сохранение каждого символа в отдельное изображение
        digit = dilation[y:y + h, x:x + w]

        # Добавление 8 пикселей белой рамки
        digit = cv2.copyMakeBorder(digit, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=[255, 255, 255])

        # Преобразование символа в объект PIL Image
        digit_pil = Image.fromarray(digit)

        # Добавление символа в список сегментов
        segments.append(digit_pil)

        x += w

    return segments


@app.route('/api/captcha/solve', methods=['POST'])
def solve_captcha():
    try:
        # Получение данных изображения из запроса
        data = request.json
        image_data = data['image']
        
        # Декодирование изображения из base64 и создание объекта Image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        
        # Сегментация изображения
        segmented_images = segment_img(image)
        
        recognized_text = ""
        for segment in segmented_images:
            # Предобработка сегмента
            # Преобразование изображения PIL в массив NumPy
            segment = np.array(segment)
            segment = cv2.resize(segment, (28, 28))
            segment = np.invert(np.array([segment]))
            
            # Предсказание цифры с использованием предварительно обученной модели Keras MNIST
            digit = mnist_model.predict(segment)
            
            # Добавление распознанной цифры к распознанному тексту
            recognized_text += str(np.argmax(digit))
        
        # Возврат распознанного текста в качестве ответа
        return jsonify({'Recognised digits': recognized_text})
    
    except Exception as e:
        # Обработка ошибок
        print('Error:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run()
