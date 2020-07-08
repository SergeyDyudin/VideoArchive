import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy
import random
from db import DataBase


class Graph:
    """Класс для рисования графиков по данным базы postgresql
    """
    def __init__(self):
        self.db = DataBase()

    def country_films_20(self):
        req = """SELECT countries.country, count(films_countries.country_id) AS col
                FROM films_countries, countries
                WHERE films_countries.country_id=countries.id
                GROUP BY countries.country
                HAVING  count(films_countries.country_id)>20;"""
        res = self.db.request(req)
        # print(res)
        country = [c for c, s in res]
        sum = [s for c, s in res]
        # print(country, sum, sep='\n')
        plt.subplots(figsize=(16, 10), facecolor='white', dpi=80)
        plt.title("Страны, с количеством фильмов > 20", fontsize=16)  # заголовок
        plt.xlabel("Страны", fontsize=14, color='blue')  # ось абсцисс
        plt.ylabel("Количество", fontsize=14)  # ось ординат
        # Отображение количества над каждым столбцом
        for i, s in enumerate(sum):
            plt.text(i, s+5, round(s, 1), horizontalalignment='center')
        # Наклон надписей по оси Х
        plt.xticks(range(len(country)), labels=country, rotation=60, horizontalalignment='right', fontsize=12)
        # plt.grid()      # включение отображение сетки
        plt.vlines(country, ymin=0, ymax=sum, color='firebrick', alpha=0.7, linewidth=40)
        plt.show()

if __name__=='__main__':
    g = Graph()
    g.country_films_20()
# l1 = numpy.random.randint(0, 100, size=20)
# l2 = numpy.random.randint(0, 100, size=20)
# l3 = [(l + random.randint(-10, 10)) for l in l2]
# country = []
# sum = []
# for i in res:
#     country.append(i[0])
#     sum.append(i[1])
# print(sorted(l1), l2, sep='\n')
# plt.plot(sorted(l1), l2, label='sorted l1 and l2')
# plt.plot(sorted(l1), l3, 'r--', label='sorted l1 and l3')
# plt.legend()  # для вывода label