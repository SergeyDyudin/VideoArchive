""" pip3 install Pillow
    pip3 install pytesseract
    pip3 install pdf2image
    sudo apt-get install tesseract-ocr

    Скачать, установить и прописать в PATH popller и tesseract
"""

from PIL import Image
import pytesseract
from pdf2image import convert_from_path

PDF_file = r"C:\Install\test.pdf"  # исходник PDF


""" Преобразование PDF в JPEG
"""

pages = convert_from_path(PDF_file, 500)  # Хранить все страницы PDF в переменной
image_counter = 1  # Счетчик для хранения изображений каждой страницы PDF для изображения

# Перебирать все страницы, хранящиеся выше
for page in pages:
    filename = "page_" + str(image_counter) + ".jpg"  # Объявление имени файла для каждой страницы PDF как JPG
    page.save(filename, 'JPEG')  # Сохранить изображение страницы в системе
    image_counter = image_counter + 1

""" Распознавание текста по изображениям с помощью Tesseract OCR
"""

filelimit = image_counter - 1  # Переменная, чтобы получить общее количество страниц
outfile = "out_text12.txt"  # выходной файл с результатом


f = open(outfile, "a", encoding='utf8')  # Открытие в режиме добавления
for i in range(1, filelimit + 1):  # Итерировать от 1 до общего количества страниц
    filename = "page_" + str(i) + ".jpg"  # Установить имя файла откуда будет распознавание текста
    text = str(((pytesseract.image_to_string(Image.open(filename),'rus+eng'))))  # Распознать текст как строку в изображении
    text = text.replace('-\n', '')  # удаляем знаки переноса строки, если они есть
    text += '\n' * 5 + '=' * 150 + '\n' * 5
    f.write(text)
f.close()