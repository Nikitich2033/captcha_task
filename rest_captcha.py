from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/api/captcha/solve', methods=['POST'])
def solve_captcha():
    try:
        # Получение данных из запроса
        data = request.json
        image_data = data['image']
        
        # Декодирование изображения из base64 и создание объекта изображения
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        
        # Распознавание текста на изображении (здесь должен быть ваш код распознавания)
        # Ниже приведен заглушечный код, который возвращает base64 представление изображения вместо распознанного текста
        recognized_text = image_data
        
        # Возврат распознанного текста в формате JSON
        return jsonify({'text': recognized_text})
    
    except Exception as e:
        # Обработка ошибок
        print('Error:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run()
