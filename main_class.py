import os
import shutil
import psutil
import openpyxl
# import xlrd

"""Класс для фильмов
"""


class Film:
    def __init__(self, name, path, serv, chief):
        self.fullname = name
        self.path = path
        self.serv_disk = serv
        self.chief_disk = chief
        self.jenre = None
        self.year = None
        self.name = None
        self.short_name = None
        self.clear_name = None
        self.file_size = os.path.getsize(self.path + '\\' + self.fullname) / 1024 / 1024 / 1024  # размер файла

    def split_fullname(self):
        """Разбиваем полное название файла вида жанр_год_название.формат на части
        """
        self.jenre, self.year, self.name = self.fullname.split('_')
        self.clear_name = os.path.splitext(self.name)[0]

    def copy_to_servdisk(self):
        """Запись на серверный диск
        """
        self.check_subtitr_film()

        if (self.file_size < 10.0) and not self.check_subtitr_film():
            self.jenre = self.jenre.capitalize()  # Первый символ строки большой, остальные маленькие
            #self.copy_film(self.serv_disk + '/Фильмы/' + self.jenre)
            film_jenre = open(self.serv_disk + '/Фильмы/' + self.jenre + '/' + self.jenre + '.doc', 'a+')
            film_jenre.write(self.clear_name + '\t' + self.year + '\n')  # запись в файл жанров
            self.write_films_xlsx()  # запись в Excel

    '''def copy_film(self, destination):
        """Копирование файла
        """
        free = psutil.disk_usage(self.serv_disk).free / (1024 * 1024 * 1024)  # свободное место на диске
        if self.file_size < free:
            # если фильм помещается на диск и его размер меньше 9 ГБ
            if os.path.exists(self.serv_disk + '/Фильмы/' + self.jenre + '/' + self.name):
                continue  # если файл уже есть на диске, то пропускаем его /не отрабатывает для (1)
            if os.path.exists(destination) is False:
                os.makedirs(destination)  # создаем директорию Жанр к будущему файлу
            new_name = newname_for_copy(os.path.splitext(spl[2]))  # обрезаем имя для (1)
            if os.path.exists(destination + '/' + new_name):  # Если файл уже записан, то не копируем
                print(f" КОПИРОВАНИЕ НЕ УДАЛОСЬ. [{self.fullname} уже есть в данной директории]")
            else:
                z = shutil.copy(self.path + '/' + self.fullname, destination + '/' + new_name)
            print(self.path + '/' + self.fullname + ' СКОПИРОВАНО В ' + destination)
            new_name = os.path.splitext(new_name)[0]  # name.ext => name
    '''

    def copy_to_chiefdisk(self):
        """Запись на диск для шефа
        """
        pass

    def check_subtitr_film(self):
        """ Проверка на существование дубликата без субтитров и посторонних дорожек
        """
        self.split_fullname()
        self.short_name, ext = os.path.splitext(self.fullname)
        if (os.path.exists(self.path + '/' + self.short_name + '(1)' + ext)) or \
                (os.path.exists(self.path + '/' + self.short_name + ' (1)' + ext)):
            return True
        else:
            return False

    def write_films_xlsx(self, season=None):
        """Запись в файл Films.xlsx Сериал-Сезон или Фильм-Жанр-Год
           write_films_xlsx(name_name, s, self.jenre, spl[1])
        """
        wb = openpyxl.load_workbook(filename='C:/install/Films.xlsx')
        ws = wb.active
        # TODO: Проверить запись в Films.xlsx с использованием только модуля openpyxl.
        #
        # В версии с классами функция переработана без использования модуля xlrd для поиска макс.количества строк
        # rb = xlrd.open_workbook(r'C:\install\Films.xlsx')
        # sheet = rb.sheet_by_index(0)
        ws["A" + str(ws.max_row + 1)] = self.clear_name
        if season: ws["B" + str(ws.max_row)] = 'Сезон ' + str(season)
        if self.jenre: ws["B" + str(ws.max_row)] = self.jenre
        if self.year: ws["C" + str(ws.max_row)] = self.year
        wb.save(r'C:\install\Films.xlsx')
        return True


"""Класс для сериалов
"""


class Serial(Film):
    def __init__(self, name, path, serv, chief):
        Film.__init__(self, name, path, serv, chief)
        season = 1


def path_existence_check(path):
    """Проверка существования пути и смена рабочей директории
    """
    if os.path.exists(path):
        os.chdir(path)
        return True
    else:
        print(f'Пути {path} не существует')
        return False


if __name__ == "__main__":
    arc_disk = input('Введите букву диска с архивом: ').upper() + ':'
    chief_disk = input('Введите букву диска для записи шефу: ').upper() + ':'
    serv_disk = input('Введите букву диска для записи на видеосервер: ').upper() + ':'
    work_paths = (arc_disk + '/Convert', arc_disk + '/New')
    for work_path in work_paths:  # проверяем существуют ли указанные рабочие пути
        if path_existence_check(work_path):
            pass
        else:
            continue
        for adress, dirs, files in os.walk(work_path):
            if adress == work_path:  # если находимся в корне рабочего пути, то обрабатываем все фильмы
                for file in files:
                    film = Film(file, adress, serv_disk, chief_disk)
                    film.copy_to_servdisk()
