from Scripts.kinopoisk_parser import KinopoiskParser
import openpyxl

'''id_film = input('Введите ID: ')
data = KinopoiskParser(id_film).get_from_kinopoisk()'''
data = KinopoiskParser().get_from_file('C:/Users/Kenobi/Desktop/Нокдаун.html')
print(data)

wb = openpyxl.load_workbook(filename='C:/install/Films.xlsx')
ws = wb.active
for row in ws.iter_rows(1, ws.max_row+1):
    if (row[0].value == data['film_name']) and(row[4].value == int(data['year'])):
        try:
            row[3].value = data["jenre"]
        except KeyError:
            print('Нет значения жанр')
        try:
            row[6].value = data["imdb"]
        except KeyError:
            print('Нет значения IMDB')
        try:
            row[7].value = data["kinopoisk"]
        except KeyError:
            print('Нет значения Kinopoisk')
        try:
            row[8].value = data["country"]
        except KeyError:
            print('Нет значения country')
        try:
            row[9].value = data["time"]
        except KeyError:
            print('Нет значения Time')
        try:
            row[10].value = data["director"]
        except KeyError:
            print('Нет значения Director')
        try:
            actors=''
            for key, value in data['actors'].items():
                actors += value + ", "
            row[11].value = actors[:-2]
        except KeyError:
            print('Нет значения Actors')
wb.save(r'C:\install\Films.xlsx')
wb.close()