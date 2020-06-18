import psycopg2
from psycopg2 import sql
import openpyxl

data_file = r'C:\install\Films.xlsx'


class DataBase:
    """Класс для работы с базой данных
    """

    def __init__(self, conn_file):
        with open(conn_file) as file:
            db_name = file.readline().rstrip()
            db_user = file.readline().rstrip()
            db_password = file.readline().rstrip()
            db_host = file.readline().rstrip()
        print(f'db = {db_name}', f'user = {db_user}', f'pass = {db_password}', f'host = {db_host}', sep='\n')
        try:
            self.conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host)
            self.cur = self.conn.cursor()
            print('***Соединение с базой установлено.***')
        except Exception as err:
            print(err)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print('Error!', exc_type, exc_val)
        self.cur.close()
        self.conn.close()
        print('***Соединение с базой закрыто.***')

    @staticmethod
    def _find_column(sheet, name):
        """
        Поиск номера столбца по имени.

        :param sheet: рабочий лист в xlsx
        :param name: имя столбца для поиска его номера
        :return: номер столбца
        """
        for cell in sheet[1]:
            if cell.value == name:
                return cell.col_idx

    def get_data(self, num_str=None):
        """Получение словаря с данными для заполнения базы данных из файла Films.xlsx.

        :param num_str: номер строки в Films.xlsx
        :return: result
        """
        result = {}
        try:
            wb = openpyxl.load_workbook(filename=data_file)
            ws = wb.active
            if not num_str:
                num_str = ws.max_row
            result['name'] = ws.cell(row=num_str, column=self._find_column(ws, 'Name')).value
            result['type'] = ws.cell(row=num_str, column=self._find_column(ws, 'Type')).value
            result['season'] = ws.cell(row=num_str, column=self._find_column(ws, 'Season')).value
            result['year'] = str(ws.cell(row=num_str, column=self._find_column(ws, 'Year')).value)
            result['genre'] = ws.cell(row=num_str, column=self._find_column(ws, 'Genre')).value
            result['id_kinopoisk'] = ws.cell(row=num_str, column=self._find_column(ws, 'Kinopoisk ID')).value
            result['imdb'] = ws.cell(row=num_str, column=self._find_column(ws, 'IMDB')).value
            result['kinopoisk'] = ws.cell(row=num_str, column=self._find_column(ws, 'Kinopoisk')).value
            result['country'] = ws.cell(row=num_str, column=self._find_column(ws, 'Country')).value
            result['time'] = ws.cell(row=num_str, column=self._find_column(ws, 'Time')).value
            result['director'] = ws.cell(row=num_str, column=self._find_column(ws, 'Director')).value
            result['actors'] = ws.cell(row=num_str, column=self._find_column(ws, 'Actors')).value
            if result['season']: result['season'] = result['season'].lower()
        finally:
            wb.close()
        return result

    def query(self, request=None):
        """Выполнение и коммит запроса.

        :param request: запрос
        :return:
        """
        data = self.get_data(7)
        request = """
                    INSERT INTO {table} ({field}) 
                    VALUES (LOWER(%s)) 
                    ON CONFLICT ({field}) DO UPDATE SET {field}=LOWER(Excluded.{field}) 
                    Returning id;
                    """
        try:
            # Заполнение таблицы years и получение id_years
            # self.cur.execute('INSERT INTO years (year) VALUES (%(year)s);', data)
            self.cur.execute(sql.SQL(request).format(table=sql.Identifier('years'),
                                                     field=sql.Identifier('year')), (data['year'],))
            id_years = self.cur.fetchone()[0]
            # Заполнение таблицы genres и получение id_genres
            self.cur.execute(sql.SQL(request).format(table=sql.Identifier('genres'),
                                                     field=sql.Identifier('genre')), (data['genre'],))
            id_genres = self.cur.fetchone()[0]
            # Заполнение таблицы types и получение id_types
            self.cur.execute("""
                    INSERT INTO types (type, season) 
                    VALUES (LOWER(%(type)s), LOWER(%(season)s)) 
                    ON CONFLICT (season) DO UPDATE SET season=LOWER(Excluded.season)
                    Returning id;
                    """, data)
            id_types = self.cur.fetchone()[0]
            # # Заполнение таблицы films и получение id_films
            self.cur.execute("""
                                INSERT INTO films (name, id_types, id_genres, id_years, time, kinopoisk_id, 
                                kinopoisk, imdb) 
                                VALUES (%(name)s, %(id_types)s, %(id_genres)s, %(id_years)s, %(time)s, %(kinopoisk_id)s,
                                %(kinopoisk)s, %(imdb)s) 
                                Returning id;
                                """, {'name': data['name'], 'id_types': id_types, 'id_genres': id_genres,
                                      'id_years': id_years, 'time': data['time'], 'kinopoisk_id': data['id_kinopoisk'],
                                      'kinopoisk': data['kinopoisk'], 'imdb': data['imdb']})
            id_films = self.cur.fetchone()[0]
        except Exception as err:
            print('Error! ', err)
            self.conn.rollback()
        else:
            print('Запрос выполнен. Делается коммит.')
            print(f'ID years = {id_years}')
            print(f'ID genres = {id_genres}')
            print(f'ID types = {id_types}')
            print(f'ID films = {id_films}')
            self.conn.commit()
        # print(self.cur.fetchall())

    def close(self):
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    # connect_file = r'C:\install\dbauth.txt'
    connect_file = 'dbauth.txt'
    with DataBase(connect_file) as base:
        # print(base.get_data(13))
        base.query()
