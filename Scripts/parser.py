from bs4 import BeautifulSoup
import os

url = 'C:/Users/Kenobi/Desktop/Avengers.Endgame.html'

with open(url, encoding="utf8") as file:
    text = file.read()
# print(text)

soup = BeautifulSoup(text)
#director = soup.find('td', {'itemprop': 'director'}).find('a').text
all_movie_info = soup.find_all('div', {'class': 'movie-info__table-container'}) #.find('a').text
results = {}
for info in all_movie_info:

    """Получаем основные данные о фильме
    """
    items = info.find('table', {'class': 'info'}).find_all('tr')  # Берем только таблицу INFO о фильме
    for item in items:
        i = item.find('td')
        if i.text == 'год':
            """results.append({
                'year': i.nextSibling.nextSibling.text
            })"""
            year = i.nextSibling.nextSibling.text
            results['year'] = year.strip()
        if i.text == 'страна':
            country = i.nextSibling.nextSibling.text
            results['country'] = country.strip()
            """results.append({
                'country': country
            })"""
        if i.text == 'режиссер':
            director = i.nextSibling.text
            results['director'] = director.strip()
        if i.text == 'жанр':
            jenre = i.nextSibling.find('a').text
            results['jenre'] = jenre.strip()
        if i.text == 'время':
            time = i.nextSibling.text
            results['time'] = time.strip()

    """ Получаем актеров фильма
    """
    items = info.find('div', {'id': 'actorList'}).find('ul').find_all('a')
    actors = {}
    for i, item in enumerate(items):
        actors[i] = item.text

"""Получаем оценки фильма
"""
kinopoisk = soup.find('div', {'class': "block_2"}).find('div', {'class': 'div1'}).text
imdb = soup.find('div', {'class': "block_2"}).find('div', {'class': 'div1'}).nextSibling.nextSibling.text
kinopoisk = kinopoisk.strip().split('\n')[0]
imdb = imdb.strip().split()[1]
results['kinopoisk'] = kinopoisk
results['imdb'] = imdb

print(results)
print(actors)
print(kinopoisk, imdb, sep='\n')
# print(year, country, director, jenre, time, sep='\n')

