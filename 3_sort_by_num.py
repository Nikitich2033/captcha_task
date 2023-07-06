import cv2
import os
import pytesseract
import shutil

# Укажите путь к Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Директория, содержащая изображения
dir_name = "single_digits"

# Директория для сохранения цифр
digits_dir = "sorted_by_num"

# Список всех файлов в директории
files = os.listdir(dir_name)

# Цикл по файлам
for file in files:
    # Полный путь к файлу
    file_path = os.path.join(dir_name, file)
    
    # Загрузка изображения
    img = cv2.imread(file_path)
    
    # Выполнение OCR с выводом данных
    data = pytesseract.image_to_data(img, config='--psm 10 -c tessedit_char_whitelist=0123456789', output_type=pytesseract.Output.DICT)

    # Перебор каждого распознанного символа
    for i in range(len(data['text'])):
        # Получение распознанного символа
        digit = data['text'][i].strip()
        
        # Пропуск пустых строк и символов, не являющихся цифрами
        if digit == '' or not digit.isdigit():
            continue
        
        # Получение уровня уверенности
        confidence = int(data['conf'][i])
        
        # Проверка, что уровень уверенности выше 85 и символ состоит из одной цифры
        if confidence > 85 and len(digit) == 1:
            # Создание директории для цифр, если она не существует
            if not os.path.exists(digits_dir):
                os.makedirs(digits_dir)
            
            # Создание директории для конкретной цифры, если она не существует
            digit_dir = os.path.join(digits_dir, digit)
            if not os.path.exists(digit_dir):
                os.makedirs(digit_dir)
            
            # Сохранение изображения в соответствующую папку
            filename = os.path.splitext(file)[0] + f"_digit{i}.jpg"
            save_path = os.path.join(digit_dir, filename)
            cv2.imwrite(save_path, img)

            # Вывод распознанной цифры и уровня уверенности
            print(f"Сохранена цифра {digit} из файла {file} с уровнем уверенности {confidence}")
