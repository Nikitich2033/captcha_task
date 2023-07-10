import requests
import base64

# URL сервера
url = 'http://localhost:5000/api/captcha/solve'

# Чтение файла с изображением и кодирование в base64
with open('captcha_imgs/captcha_25.jpg', 'rb') as file:
    image_data = base64.b64encode(file.read()).decode('utf-8')

# Подготовка данных запроса
payload = {'image': image_data}

# Отправка POST-запроса
response = requests.post(url, json=payload)

# Проверка ответа
if response.status_code == 200:
    result = response.json()
    print('Распознанные цифры:', result['Recognised digits'])
else:
    print('Ошибка:', response.text)
