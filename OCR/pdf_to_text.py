""" pip3 install PIL
    pip3 install pytesseract
    pip3 install pdf2image
    sudo apt-get install tesseract-ocr

    Прописать в PATH popller и tesseract
"""

from PIL import Image
import pytesseract
from pdf2image import convert_from_path

# Путь в PDF

PDF_file = r"C:\Install\test.pdf"


"""
Часть № 1: Преобразование PDF в изображения

"""

pages = convert_from_path(PDF_file, 500)  # Хранить все страницы PDF в переменной
image_counter = 1  # Счетчик для хранения изображений каждой страницы PDF для изображения

# Перебирать все страницы, хранящиеся выше
for page in pages:
    # Объявление имени файла для каждой страницы PDF как JPG
    # Для каждой страницы имя файла будет:
    # PDF page 1 -> page_1.jpg
    # PDF страница 2 -> page_2.jpg
    # PDF страница 3 -> page_3.jpg
    # ....
    # PDF page n -> page_n.jpg
    filename = "page_" + str(image_counter) + ".jpg"
    page.save(filename, 'JPEG')  # Сохранить изображение страницы в системе
    image_counter = image_counter + 1  # Увеличить счетчик для обновления имени файла

"""
Часть № 2 - Распознавание текста по изображениям с помощью OCR

"""

filelimit = image_counter - 1  # Переменная, чтобы получить общее количество страниц
outfile = "out_text.txt"  # Создание текстового файла для записи вывода

# Откройте файл в режиме добавления, чтобы
# Все содержимое всех изображений добавляется в один файл
f = open(outfile, "a", encoding='utf8')
for i in range(1, filelimit + 1):  # Итерировать от 1 до общего количества страниц
    # Установить имя файла для распознавания текста из
    # Опять же, эти файлы будут:
    # page_1.jpg
    # page_2.jpg
    # ....
    # page_n.jpg
    filename = "page_" + str(i) + ".jpg"
    text = str(((pytesseract.image_to_string(Image.open(filename),'rus+eng'))))  # Распознать текст как строку в изображении

    # Распознанный текст хранится в переменном тексте
    # Любая обработка строки может быть применена к тексту
    # Здесь было выполнено базовое форматирование:
    # Во многих PDF-файлах, в конце строки, если слово не может
    # быть написанным полностью, добавляется дефис.
    # Остальное слово написано в следующей строке
    # Чтобы удалить это, мы заменяем каждый '- / n' на ''.

    text = text.replace('-\n', '')
    f.write(text)  # Наконец, запишите обработанный текст в файл.
f.close()