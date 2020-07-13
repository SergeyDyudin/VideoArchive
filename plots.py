import matplotlib.pyplot as plt
# import matplotlib.patches as patches
import pandas as pd
# import numpy
# import random
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
        col = [s for c, s in res]
        plt.subplots(figsize=(15, 10), facecolor='white', dpi=80)
        plt.title("Страны, с количеством фильмов > 20", fontsize=16)  # заголовок
        plt.xlabel("Страны", fontsize=14, color='blue')  # ось абсцисс
        plt.ylabel("Количество", fontsize=14)  # ось ординат
        # Отображение количества над каждым столбцом
        for i, s in enumerate(col):
            plt.text(i, s+5, round(s, 1), horizontalalignment='center')
        # Наклон надписей по оси Х
        plt.xticks(range(len(country)), labels=country, rotation=60, horizontalalignment='right', fontsize=12)
        # plt.grid()      # включение отображение сетки
        plt.vlines(country, ymin=0, ymax=col, color='firebrick', alpha=0.7, linewidth=40)
        plt.legend()  # для вывода label
        # plt.show()

        df = pd.DataFrame(res, columns=['Страна', 'Количество'])
        print(df)
        df.plot(kind='bar', x='Страна', y='Количество')
        plt.show()


if __name__ == '__main__':
    g = Graph()
    g.country_films_20()

# l1 = numpy.random.randint(0, 100, size=20)
# l2 = numpy.random.randint(0, 100, size=20)
# l3 = [(l + random.randint(-10, 10)) for l in l2]
# country = []
# col = []
# for i in res:
#     country.append(i[0])
#     col.append(i[1])
# print(sorted(l1), l2, sep='\n')
# plt.plot(sorted(l1), l2, label='sorted l1 and l2')
# plt.plot(sorted(l1), l3, 'r--', label='sorted l1 and l3')
# plt.legend()  # для вывода label

# np.arange(start, stop, step) - целочисленный массив "с" "по" c "шагом". Аргументы start и step можно опускать.
# np.random.random() - случайное число < 1
# np.random.random(3) - список из трех случайных элементов < 1
# np.random.random((2,3)) - список из двух списков по 3 элемента < 1 (двухмерный массив - 2 строки, 3 столбца)
# np.random.random_integers(0, 3, 10) - целочисленный массив
# >>> array([2, 2, 3, 3, 1, 1, 0, 2, 3, 2])
# np.random.randint(0, 3, (2, 10))
# >>> array([[0, 1, 2, 0, 0, 0, 1, 1, 1, 2],
#           [0, 0, 2, 2, 2, 0, 1, 2, 2, 1]])
# np.random.shuffle(a) - перемешать список "a"
