import os
import shutil
import psutil
import openpyxl
import xlrd

"""Класс для фильмов
"""


class Film:
    def __init__(self):
        pass

    def write_films_xlsx(self, name, season=None, jenre=None, year=None):
        """Запись в файл Films.xlsx Сериал-Сезон или Фильм-Жанр-Год
           write_films_xlsx(name_name, s, spl[0], spl[1])
        """
        wb = openpyxl.load_workbook(filename='C:/install/Films.xlsx')
        ws = wb.active
        rb = xlrd.open_workbook(r'C:\install\Films.xlsx')
        sheet = rb.sheet_by_index(0)
        ws["A" + str(sheet.nrows + 1)] = name
        if season: ws["B" + str(sheet.nrows + 1)] = 'Сезон ' + str(season)
        if jenre: ws["B" + str(sheet.nrows + 1)] = jenre
        if year: ws["C" + str(sheet.nrows + 1)] = year
        wb.save(r'C:\install\Films.xlsx')
        return True


"""Класс для сериалов
"""


class Serial(Film):
    def __init__(self):
        Film.__init__(self)
        self.season = 1


if __name__ == "__main__":
    arc_disk = input('Введите букву диска с архивом: ').upper() + ':'
    chief_disk = input('Введите букву диска для записи шефу: ').upper() + ':'
    serv_disk = input('Введите букву диска для записи на видеосервер: ').upper() + ':'
