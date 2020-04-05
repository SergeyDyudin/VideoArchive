from Scripts.kinopoisk_parser import KinopoiskParser
import openpyxl
import time

"""name_film = input('Введите имя фильма: ')
name_film = name_film.lower()
year_film = input('Введите год: ')
film = KinopoiskParser(name=name_film, year=year_film)
film.find_film_id()
data = film.get_from_kinopoisk()"""
# data = KinopoiskParser().get_from_file('C:/Users/Kenobi/Desktop/Нокдаун.html')
# print(data)

wb = openpyxl.load_workbook(filename='C:/install/Films.xlsx')
ws = wb.active
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    name_film = row[0].value.lower()
    year_film = str(row[4].value)
    film = KinopoiskParser(name=name_film, year=year_film)
    id = film.find_film_id()
    if not id:
        time.sleep(20)
        continue
    data = film.get_from_kinopoisk()
    if (row[0].value == data['film_name'].replace(':','.')) and (row[4].value == int(data['year'])):
        try:
            row[3].value = data["jenre"]
        except KeyError:
            print('Нет значения жанр')
        try:
            row[5].value = data["id_kinopoisk"]
        except KeyError:
            print('Нет значения id_kinopoisk')
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
            actors = ''
            for key, value in data['actors'].items():
                actors += value + ", "
            row[11].value = actors[:-2]
        except KeyError:
            print('Нет значения Actors')
    print(f'Получены и записаны данные для {name_film}')
    wb.save(r'C:\install\Films.xlsx')
    time.sleep(20)  # задержка между запросами, чтобы не банил Кинопоиск
wb.save(r'C:\install\Films.xlsx')
wb.close()
