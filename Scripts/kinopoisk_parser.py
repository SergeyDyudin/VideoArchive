from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import openpyxl


class ProxyManager:
    """
    Класс для получения списка доступных прокси с портами и его обновления
    """
    def __init__(self):
        self._current_proxy_index = 1
        self._proxy_list = []
        self._get_proxy_list()
        self._current_proxy = f'http://{self._proxy_list[0]}'
        self._current_proxy_s = f'https://{self._proxy_list[0]}'

    def get_proxies(self):
        """proxy_ip_with_port = self._proxy_list[self._current_proxy_index]
        self._current_proxy = f'http://{proxy_ip_with_port}'
        self._current_proxy_s = f'https://{proxy_ip_with_port}'"""
        proxies = {
            "http": self._current_proxy,
            "https": self._current_proxy_s
        }

        return proxies

    def update_proxy(self):
        self._current_proxy_index += 1
        if self._current_proxy_index == len(self._proxy_list):
            print("Proxies are ended")
            print("Try get alternative proxy")
            proxy_ip_with_port = self._get_another_proxy()
            print("Proxy updated to " + proxy_ip_with_port)

            self._current_proxy = f'http://{proxy_ip_with_port}'
            self._current_proxy_s = f'https://{proxy_ip_with_port}'
            self._proxy_list = []
            self._proxy_list.insert(0, proxy_ip_with_port)
            self._current_proxy_index = 0
            return self._current_proxy

        proxy_ip_with_port = self._proxy_list[self._current_proxy_index]

        print("Proxy updated to " + proxy_ip_with_port)

        self._current_proxy = f'http://{proxy_ip_with_port}'
        self._current_proxy_s = f'https://{proxy_ip_with_port}'
        return self._current_proxy

    @staticmethod
    def _get_another_proxy():
        proxy_response = requests.get("https://api.getproxylist.com/proxy?protocol[]=http", headers={
            'Content-Type': 'application/json'
        }).json()

        ip = proxy_response['ip']
        port = proxy_response['port']
        proxy = f'{ip}:{port}'

        return proxy

    def _get_proxy_list(self):
        proxy_response = requests.get("http://www.freeproxy-list.ru/api/proxy?anonymity=false&token=demo")
        # proxy_response = requests.get("http://api.foxtools.ru/v2/Proxy.txt?cp=UTF-8&lang=Auto&type=\
        # HTTPS&anonymity=None&available=Yes&free=Yes&page=1")

        self._proxy_list = proxy_response.text.split("\n")


class KinopoiskParser:
    """Класс ищет данные фильма по названию и году либо на сайте Кинопоиска, либо на сохраненной локально странице
    """
    def __init__(self, id=None, name=None, year=None):
        self.id_film = id
        self.name_film = name
        self.year = year
        self.result = {}
        self.browser = None

    @staticmethod
    def get_info(content):
        # text = self.read_from_file()  # Получаем данные из файла
        soup = BeautifulSoup(content, features="html.parser")
        results = {}
        actors = {}
        results['film_name'] = soup.find('span', {'class': 'moviename-title-wrapper'}).text
        all_movie_info = soup.find_all('div', {'class': 'movie-info__table-container'})  # .find('a').text
        for info in all_movie_info:
            """Получаем основные данные о фильме
            """
            items = info.find('table', {'class': 'info'}).find_all('tr')  # Берем только таблицу INFO о фильме
            for item in items:
                i = item.find('td')
                if i.text == 'год':
                    year = i.nextSibling.nextSibling.text
                    results['year'] = year.strip()
                if i.text == 'страна':
                    country = i.nextSibling.nextSibling.text
                    results['country'] = country.strip()
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
            items = soup.find('div', {'id': 'actorList'}).find('ul').find_all('a')
            # items = info.find('div', {'id': 'actorList'}).find('ul').find_all('a')
            for i, item in enumerate(items):
                actors[i] = item.text
        try:
            actors.popitem()  # Удаляем актера "...". Во всех фильмах многоточие в конце списка
        except KeyError:
            print('Список актеров пуст!')
        results['actors'] = actors

        """Получаем оценки фильма
        """
        try:
            kinopoisk = soup.find('div', {'class': "block_2"}).find('div', {'class': 'div1'}).text
            imdb = soup.find('div', {'class': "block_2"}).find('div', {'class': 'div1'}).nextSibling.nextSibling.text
            kinopoisk = kinopoisk.strip().split('\n')[0]
            imdb = imdb.strip().split()[1]
            results['kinopoisk'] = kinopoisk
            results['imdb'] = imdb
        except AttributeError:
            print('Оценок у фильма еще нет')
        return results

    def find_film_id(self):
        """ Получаем страницу поиска по названию и ищем подходящий фильм
            https://www.kinopoisk.ru/index.php?kp_query=мстители
        """
        url = f"https://www.kinopoisk.ru/index.php?kp_query={self.name_film}"
        # get = requests.get(url)  # Request банит
        """Запросы через Selenium
        """
        browser = webdriver.Firefox(firefox_profile=r'C:\Users\video\AppData\Roaming\Mozilla\Firefox\Profiles\h3qugs8n.Kinopisk')
        # browser.firefox_profile.profile_dir = r'C:\Users\video\AppData\Roaming\Mozilla\Firefox\Profiles\h3qugs8n.Kinopisk'
        browser.get(url)
        wait = WebDriverWait(browser, 10)
        time.sleep(10)
        get = browser.page_source
        browser.close()
        # content = get.content
        soup = BeautifulSoup(get, features="html.parser")
        results = soup.find_all('p', {'class': 'name'})
        for result in results:
            try:
                year = result.find('span', {'class': 'year'}).text
            except:
                break
            if '-' in year:
                continue
            """ else:
                year = int(year)"""
            name = result.find('a').text
            name = name.replace(':', '.')
            if (self.name_film == name.lower()) and (self.year == year):
                self.id_film = result.find('a')['data-id']
                return True
        if not self.id_film:
            print('Фильм не найден')
            return False

    def get_from_file(self, url=None):
        """Получение soup из сохраненной странички, а не запроса
        """
        # url = 'C:/Users/Kenobi/Desktop/Avengers.Endgame.html'
        if not url:
            url = input('Введите путь к файлу html: ')
        with open(url, encoding="utf8") as file:
            text = file.read()
        self.result = self.get_info(text)
        return self.result

    def get_from_kinopoisk_with_id(self):
        """Получение soup из запроса к сайту Кинопоиска.
           Должен быть уже известен self.id_film.
           Ищем его через find_film_id() по названию
        """
        url = f'https://www.kinopoisk.ru/film/{self.id_film}'
        """ Смена прокси для запроса
        """
        # response = requests.Session()
        """response.headers.update({
            'Accept': '* / *',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q =0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Cookie': 'yandexuid=5009534201542819529;\
                    i=T1rnooU7wago5S31vAb4g8YMVDvo7XHznxzBGSkLiENlGRVCL0IvKKpjxDkw8jh1XJUW2Uw0BSQWx2KmELPrMPfKsQg =;\
                    yp=;\
                    skid=1457655041577010993;\
                    _ym_uid=1577011031672446783;\
                    _ym_d=1577011031;\
                    mda=0;\
                    yuidss=5009534201542819529;\
                    ymex=1899219516.\
                    yrts\
                    .1583859516;\
                    ys=c_chck\
                    .3759072711;\
                    device_id="b1290f93c20836c0905ee5cb5d347e9c2da593b45";\
                    active-browser-timestamp=1585838003098',
            'Host': 'mc.yandex.ru',
            'Referer': f'http://www.kinopoisk.ru/film/{self.id_film}',
            'Sec-Fetch-Dest': 'script',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        })"""

        """proxy_manager = ProxyManager()
        for _ in range(len(proxy_manager._proxy_list)):
            try:
                get = response.get(url, proxies=proxy_manager.get_proxies(), timeout=1)
                text = get.text
                break
            except BaseException:
                proxy_manager.update_proxy()
                continue"""

        # get = requests.get(url)
        # text = get.text

        """Запросы через Selenium
        """
        browser = webdriver.Firefox()
        browser.get(url)
        wait = WebDriverWait(browser, 10)
        time.sleep(10)
        get = browser.page_source
        browser.close()
        # content = get.content  # .decode(get.encoding)
        '''if 'captcha' in content:
            raise ValueError('Kinopoisk block this IP. Too many requests')'''
        self.result = self.get_info(get)
        self.result['id_kinopoisk'] = self.id_film
        return self.result

    """Методы для поиска через Selenium
    """
    def open_selenium(self):
        """Запуск Selenium-браузера(Firefox) и переход на сайт Кинопоиска
        """
        url = 'https://www.kinopoisk.ru/'
        self.browser = webdriver.Firefox()  # firefox_profile=r'C:\Users\video\AppData\Roaming\Mozilla\Firefox\Profiles\h3qugs8n.Kinopisk')
        self.browser.get(url)

    def find_on_kinopoisk(self, name_film, year):
        wb = openpyxl.load_workbook(filename='C:/install/Films.xlsx')
        ws = wb.active
        self.name_film = name_film
        self.year_film = year
        self.name_film = str(self.name_film).lower()
        self.year_film = str(self.year_film)
        # запуск поиска на сайте
        search_form = self.browser.find_element_by_name('kp_query')
        search_form.clear()
        search_form.send_keys(self.name_film)
        search_form.submit()
        time.sleep(6)
        WebDriverWait(self.browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'name')))
        # получение и обход результатов поиска
        results = self.browser.find_elements_by_class_name('name')
        for result in results:
            try:
                year = result.find_element_by_class_name('year').text
            except:
                year = ''
                continue
            if '-' in year:
                continue
            """ else:
                year = int(year)"""
            name = result.find_element_by_tag_name('a').text
            # В таблице во всех названиях ':' заменено на '.', т.к. названия файлов не позволяют ставить ':'
            name = name.replace(':', '.')
            # в названиях на Кинопоиске иногда попадаются специальные символы многоточия, которые дают False в сравнении имен
            name = name.replace(chr(8230), '...')
            self.name_film = self.name_film.replace(chr(8230), '...')
            # в названиях на Кинопоиске иногда попадаются символ неразрывного пробела, который дает False в сравнении имен
            name = name.replace(chr(160), chr(32))
            if (self.name_film == name.lower()) and (self.year_film == year):
                result.find_element_by_tag_name('a').click()
                break




if __name__ == '__main__':
    identificator = input('Введите ID фильма: ')
    film = KinopoiskParser(identificator)
    # results = film.get_from_file()
    output = film.get_from_kinopoisk_with_id()
    print(output)
