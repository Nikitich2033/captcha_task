import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import os

# URL главной страницы
base_url = "http://services.fms.gov.ru/info-service.htm?sid=2000"

# Количество изображений для загрузки
num_images = 400

# Создайте директорию для изображений, если она еще не существует
os.makedirs('captcha_imgs', exist_ok=True)

# Получить список уже сохраненных изображений
saved_images = len(os.listdir('captcha_imgs'))

# Цикл для загрузки каждого изображения
while saved_images < num_images:
# Создать новую сессию для каждой загрузки изображения
    with requests.Session() as session:
        
        # Отправить GET-запрос на главную страницу
        response = session.get(base_url)

        # Создать объект BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Найти изображение капчи по id
        captcha_image = soup.find('img', {'id': 'captcha_image'})

        # Если изображение найдено
        if captcha_image:
            # Получить абсолютный URL изображения
            image_url = urljoin(base_url, captcha_image['src'])

            # Отправить GET-запрос к изображению
            image_response = session.get(image_url)

            # Сохранить изображение с новым именем, увеличивая счетчик сохраненных изображений
            with open(f'captcha_imgs/captcha_{saved_images}.jpg', 'wb') as f:
                f.write(image_response.content)

            # Увеличиваем счетчик сохраненных изображений
            saved_images += 1
        else:
            print("Изображение капчи не найдено")

    # Подождите секунду перед следующим запросом
    time.sleep(1)
