""" pip3 install PIL
    pip3 install pytesseract
    pip3 install pdf2image
    sudo apt-get install tesseract-ocr
"""

# Импорт библиотек

from PIL import Image

import pytesseract

import sys

from pdf2image import convert_from_path

import os

# Путь в PDF

PDF_file = r"C:\Install\test.pdf"


"""
Часть № 1: Преобразование
PDF
в
изображения
"""


# Хранить все страницы PDF в переменной

pages = convert_from_path(PDF_file, 500)

# Счетчик для хранения изображений каждой страницы PDF для изображения

image_counter = 1

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

    # Сохранить изображение страницы в системе

    page.save(filename, 'JPEG')

    # Увеличить счетчик для обновления имени файла

    image_counter = image_counter + 1


"""
Часть № 2 - Распознавание
текста
по
изображениям
с
помощью
OCR
"""

# Переменная, чтобы получить общее количество страниц

filelimit = image_counter - 1

# Создание текстового файла для записи вывода

outfile = "out_text.txt"

# Откройте файл в режиме добавления, чтобы
# Все содержимое всех изображений добавляется в один файл

f = open(outfile, "a")

# Итерировать от 1 до общего количества страниц

for i in range(1, filelimit + 1):
    # Установить имя файла для распознавания текста из

    # Опять же, эти файлы будут:

    # page_1.jpg

    # page_2.jpg

    # ....

    # page_n.jpg

    filename = "page_" + str(i) + ".jpg"

    # Распознать текст как строку в изображении, используя pytesserct

    text = str(((pytesseract.image_to_string(Image.open(filename)))))

    # Распознанный текст хранится в переменном тексте

    # Любая обработка строки может быть применена к тексту

    # Здесь было выполнено базовое форматирование:

    # Во многих PDF-файлах, в конце строки, если слово не может

    # быть написанным полностью, добавляется дефис.

    # Остальное слово написано в следующей строке

    # Например: это пример текста этого слова здесь GeeksF-

    # orGeeks - половина на первой строке, оставшаяся на следующей.

    # Чтобы удалить это, мы заменяем каждый '- / n' на ''.

    text = text.replace('-\n', '')

    # Наконец, запишите обработанный текст в файл.

    f.write(text)

# Закройте файл после написания всего текста.
f.close()