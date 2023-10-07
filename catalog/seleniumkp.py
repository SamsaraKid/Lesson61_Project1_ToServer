import datetime
from .models import *
from random import choice

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
time_pause = 0.5
monthes = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

# функции для скачивания базы фильмов из кинопоиска

def driverprepare():
    print('Загружаем драйвер...')
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    print('Драйвер загружен')
    return driver


def addtodb(data):
    try:
        country = Country.objects.get(name=data['country'])
    except:
        country = Country.objects.create(name=data['country'])
    try:
        director = Director.objects.get(**data['director'])
    except:
        director = Director.objects.create(**data['director'])
    try:
        ager = AgeRate.objects.get(rate=data['ager'])
    except:
        ager = AgeRate.objects.create(rate=data['ager'])
    try:
        genre = Genre.objects.get(name=data['genre'])
    except:
        genre = Genre.objects.create(name=data['genre'])
    kino = Kino.objects.create(title=data['title'],
                            genre=genre,
                            rating=data['rating'],
                            country=country,
                            director=director,
                            summary=data['summary'],
                            year=data['year'],
                            ager=ager,
                            status=Status.objects.get(id=choice([1, 2, 3])),
                            poster=data['poster'])
    for actor in data['actors']:
        try:
            act = Actor.objects.get(fname=actor['fname'], lname=actor['lname'])
        except:
            act = Actor.objects.create(**actor)
        kino.actor.add(act)
        kino.save()


def isindb(title, year):
    print('Фильм', f'"{title}" ({year})')
    if Kino.objects.filter(title=title, year=year):
        print('Фильм есть в базе')
        return True
    else:
        print('Фильма нет в базе')
        return False


def getmovies():
    driver = driverprepare()
    print('Ищем фильмы...')
    try:
        for i in range(1, 6):
            driver.get('https://www.kinopoisk.ru/lists/movies/top250/?page=' + str(i))
            for n in range(0, 50):
                movies = driver.find_elements(By.CLASS_NAME, 'styles_root__ti07r')
                m = movies[n]
                movie_title = m.find_element(By.CLASS_NAME, 'styles_mainTitle__IFQyZ')
                title = movie_title.text
                year = m.find_element(By.CLASS_NAME, 'desktop-list-main-info_secondaryText__M_aus').text.split(', ')
                if len(year) == 2:
                    year = int(year[0])
                else:
                    year = int(year[1])
                if not isindb(title, year):
                    info = m.find_element(By.CLASS_NAME, 'desktop-list-main-info_truncatedText__IMQRP').text.split(' • ')
                    country = info[0]
                    genre = info[1].split('  ')[0]
                    director = {'fname': info[1].split(': ')[1].split(' ')[0], 'lname': info[1].split(': ')[1].split(' ')[1]}
                    rating = m.find_element(By.CLASS_NAME, 'styles_kinopoiskValueBlock__qhRaI').text
                    print(f'Первичные данные: {country}, {genre}, {director}, {rating}')

                    #переход на страницу фильма
                    movie_title.click()
                    time.sleep(time_pause)
                    summary = driver.find_element(By.CLASS_NAME, 'styles_synopsisSection__nJoAj').text
                    ager_all = driver.find_elements(By.CLASS_NAME, 'styles_rootHighContrast__Bevle')
                    if len(ager_all) > 1:
                        ager = ager_all[1].text
                    else:
                        ager = ager_all[0].text
                    poster = driver.find_element(By.CLASS_NAME, 'film-poster').get_attribute('src')
                    print('Получил остальные данные')

                    # поиск актёров
                    actors = []
                    i = 0
                    while True:
                        actor_li = driver.find_elements(By.CLASS_NAME, 'styles_list___ufg4')[0].find_elements(By.TAG_NAME,'li')
                        actor_li[i].find_element(By.TAG_NAME, 'a').click()
                        time.sleep(time_pause)
                        name = driver.find_element(By.CLASS_NAME, 'styles_primaryName__2Zu1T').text
                        try:
                            actor_fname = name[0:name.index(' ')]
                            actor_lname = name[name.index(' ')+1:]
                        except:
                            actor_fname = name
                            actor_lname = ''
                        info = driver.find_elements(By.CLASS_NAME, 'styles_rowDark__ucbcz')
                        actor_country = ''
                        actor_born = ''
                        for info_string in info:
                            if info_string.text.split('\n')[0] == 'Дата рождения' and info_string.text.split('\n')[1] != '—':
                                try:
                                    born_date = info_string.text.split(' • ')[0].split('\n')[1]
                                    born_year = int(born_date.split(', ')[-1])
                                    born_month = int(monthes.index(born_date.split(', ')[0].split(' ')[1]) + 1)
                                    born_day = int(born_date.split(' ')[0])
                                    actor_born = datetime.date(born_year, born_month, born_day)
                                except:
                                    pass
                            if info_string.text.split('\n')[0] == 'Место рождения'and info_string.text.split('\n')[1] != '—':
                                actor_country = info_string.text.split('\n')[1].split(', ')[-1]
                        actor = {'fname': actor_fname, 'lname': actor_lname}
                        if actor_country:
                            actor.update({'country': actor_country})
                        if actor_born:
                            actor.update({'born': actor_born})
                        print('Актёр: ', actor)
                        actors.append(actor)
                        driver.back()
                        time.sleep(time_pause)
                        i += 1
                        if i >= len(actor_li):
                            break

                    driver.back()
                    movie = {'title': title,
                            'year': year,
                            'country': country,
                            'genre': genre,
                            'director': director,
                            'rating': rating,
                            'summary': summary,
                            'ager': ager,
                            'poster': poster,
                            'actors': actors}
                    addtodb(movie)
                    print(f'Добавил "{title}" в базу')
    except Exception as e:
        print(e)
    driver.close()
