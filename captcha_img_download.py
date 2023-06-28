import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL главной страницы
base_url = "http://services.fms.gov.ru/info-service.htm?sid=2000"

# Ссылка на изображение капчи
captcha_url = "http://services.fms.gov.ru/services/captcha.jpg"

# Создаем сессию
session = requests.Session()

# Отправляем GET запрос на главную страницу
response = session.get(base_url)

# Создаем объект BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Находим изображение капчи по id
captcha_image = soup.find('img', {'id': 'captcha_image'})

# Если изображение найдено
if captcha_image:
    # Получаем абсолютный URL изображения
    image_url = urljoin(base_url, captcha_image['src'])

    # Отправляем GET запрос к изображению
    image_response = session.get(image_url)

    # Сохраняем изображение
    with open('captcha.jpg', 'wb') as f:
        f.write(image_response.content)
