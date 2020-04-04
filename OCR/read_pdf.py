import PyPDF2
# from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import re

PDF_file = r"C:\Install\test.pdf"  # исходник PDF

""" Сохраняем отдельно pdf-лист с Товарной Накладной
"""
file = PyPDF2.PdfFileReader(PDF_file)
page_3 = file.getPage(2).rotateClockwise(90)  # Получаем нужную страницу и сразу её переворачиваем
out_file = PyPDF2.PdfFileWriter()
out_file.addPage(page_3)
out = open(r"C:\Install\page_3.pdf", "wb")
out_file.write(out)
out.close()

""" Конвертируем лист в JPEG
"""
# Ниже 600 dpi проблемы с распознаванием части текста, если файл был перевернут программно
page = convert_from_path(r"C:\Install\page_3.pdf", 600)
page[0].save(r"C:\Install\page_3.jpg", 'JPEG')

# """ Переворачиваем JPEG-лист в читаемое положение
# """
# jpeg_page = Image.open(r"C:\Install\page_3.jpg").rotate(270, expand=1)
# jpeg_page.save(r"C:\Install\page_3_rotate.jpg")

""" Распознаем и записываем txt текст
"""
outfile = r"C:\Install\out_text.txt"
f = open(outfile, "w", encoding='utf8')
text = str(pytesseract.image_to_string(r"C:\Install\page_3.jpg", 'rus+eng'))
text = text.replace('-\n', '')


""" Режем на строки и убираем лишний текст
"""
strings = re.split("\n", text)
list_str = []
for string in strings:
    result = re.search('Унифицированная форма', string)
    if result:
        continue
    result = re.search('Форма по ОКУД', string)
    if result:
        start_str = result.start()
        string = string[0:start_str]
    result = re.search('по ОКПО', string)
    if result:
        start_str = result.start()
        string = string[0:start_str]
    result = re.search('Вид деятельности по ОКДП', string)
    if result:
        start_str = result.start()
        string = string[0:start_str]
    list_str.append(string)
    result = re.search('ТОВАРНАЯ НАКЛАДНАЯ', string)
    if result:
        break

text = '\n'.join(list_str)
text = re.sub('\n[\s]*\n*', '\n', text)  # Удаляем лишние пустые строки
f.write(text)
f.close()