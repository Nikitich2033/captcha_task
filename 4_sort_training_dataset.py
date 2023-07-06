import os
import random
import shutil

# Директория, содержащая папку с цифрами
base_dir = "sorted_by_num"

# Директория для папок train и test
train_dir = os.path.join("sorted_training", "train")
test_dir = os.path.join("sorted_training", "test")

# Создание директорий train и test, если они не существуют
if not os.path.exists(train_dir):
    os.makedirs(train_dir)

if not os.path.exists(test_dir):
    os.makedirs(test_dir)

# Список подпапок в директории с цифрами
subfolders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

# Цикл по каждой подпапке
for subfolder in subfolders:
    # Создание соответствующей подпапки в директориях train и test
    train_subfolder = os.path.join(train_dir, subfolder)
    test_subfolder = os.path.join(test_dir, subfolder)

    if not os.path.exists(train_subfolder):
        os.makedirs(train_subfolder)

    if not os.path.exists(test_subfolder):
        os.makedirs(test_subfolder)

    # Список всех файлов в подпапке
    files = os.listdir(os.path.join(base_dir, subfolder))

    # Вычисление количества файлов для теста (25% от общего числа)
    num_test_files = int(len(files) * 0.25)

    # Случайный выбор файлов для папки test
    test_files = random.sample(files, num_test_files)

    # Копирование выбранных файлов в подпапку test
    for test_file in test_files:
        src_path = os.path.join(base_dir, subfolder, test_file)
        dst_path = os.path.join(test_subfolder, test_file)
        shutil.copy(src_path, dst_path)

    # Копирование оставшихся файлов в подпапку train
    for file in files:
        src_path = os.path.join(base_dir, subfolder, file)
        dst_path = os.path.join(train_subfolder, file)
        if file not in test_files:  # Пропуск файлов, уже скопированных в папку test
            shutil.copy(src_path, dst_path)
