import requests
import openpyxl
from pathlib import Path

def get_film_icon():
    file_xlsx = Path(__file__).parent.parent.joinpath('database').joinpath('Films.xlsx')

    wb = openpyxl.load_workbook(filename=file_xlsx)
    ws = wb.active
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        id_film = str(row[5].value)
        url = f'https://www.kinopoisk.ru/images/sm_film/{id_film}.jpg'
        req = requests.get(url)
        with open(f'/Users/sergeydyudin/Documents/PycharmProjects/films_site/main/static/main/img/icons/{id_film}_icon.jpg', 
            'wb') as icon_file:
            icon_file.write(req.content)
            print(f'Загружена иконка для фильма {id_film}')
    wb.close()

if __name__ == "__main__":
    get_film_icon()