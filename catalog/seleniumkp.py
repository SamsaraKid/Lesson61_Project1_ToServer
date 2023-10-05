from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
monthes = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

# функции для скачивания базы фильмов из кинопоиска

def driverprepare():
    print('Загружаем драйвер...')
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    print('Драйвер загружен')
    return driver


def getmovies():
    driver = driverprepare()
    movies_list = []
    print('Ищем фильмы...')
    try:
        for i in range(1, 2): #6
            driver.get('https://www.kinopoisk.ru/lists/movies/top250/?page=' + str(i))
            for n in range(1, 2): #51
                movies = driver.find_elements(By.CLASS_NAME, 'styles_root__ti07r')
                m = movies[n]
                movie_title = m.find_element(By.CLASS_NAME, 'styles_mainTitle__IFQyZ')
                title = movie_title.text
                year = m.find_element(By.CLASS_NAME, 'desktop-list-main-info_secondaryText__M_aus').text.split(', ')
                if len(year) == 2:
                    year = int(year[0])
                else:
                    year = int(year[1])
                info = m.find_element(By.CLASS_NAME, 'desktop-list-main-info_truncatedText__IMQRP').text.split(' • ')
                country = info[0]
                genre = info[1].split('  ')[0]
                director = info[1].split(': ')[1]
                rating = m.find_element(By.CLASS_NAME, 'styles_kinopoiskValueBlock__qhRaI').text

                #переход на страницу фильма
                movie_title.click()
                summary = driver.find_element(By.CLASS_NAME, 'styles_synopsisSection__nJoAj').text
                ager_all = driver.find_elements(By.CLASS_NAME, 'styles_rootHighContrast__Bevle')
                if len(ager_all) > 1:
                    ager = ager_all[1].text
                else:
                    ager = ager_all[0].text
                poster = driver.find_element(By.CLASS_NAME, 'film-poster').get_attribute('src')

                # поиск актёров
                actors = []
                i = 0
                while True:
                    actor_li = driver.find_elements(By.CLASS_NAME, 'styles_list___ufg4')[0].find_elements(By.TAG_NAME,'li')
                    actor_li[i].find_element(By.TAG_NAME, 'a').click()
                    time.sleep(1)
                    name = driver.find_element(By.CLASS_NAME, 'styles_primaryName__2Zu1T').text
                    actor_fname = name[0:name.index(' ')]
                    actor_lname = name[name.index(' ')+1:]
                    info = driver.find_elements(By.CLASS_NAME, 'styles_rowDark__ucbcz')
                    actor_country = ''
                    actor_born = ''
                    for info_string in info:
                        if info_string.text.split('\n')[0] == 'Дата рождения':
                            born_date = info_string.text.split(' • ')[0].split('\n')[1]
                            born_year = str(born_date.split(', ')[-1])
                            born_month = str(monthes.index(born_date.split(', ')[0].split(' ')[1]) + 1)
                            if len(born_month) == 1:
                                born_month = '0' + born_month
                            born_day = str(born_date.split(' ')[0])
                            if len(born_day) == 1:
                                born_day = '0' + born_day
                            actor_born = '-'.join([born_year, born_month, born_day])
                        if info_string.text.split('\n')[0] == 'Место рождения':
                            actor_country = info_string.text.split(', ')[-1]
                    actors.append({'fname': actor_fname, 'lname': actor_lname, 'country': actor_country, 'born': actor_born})
                    driver.back()
                    time.sleep(1)
                    i += 1
                    if i == len(actor_li):
                        break
                driver.back()
                movies_list.append({'title': title,
                                    'year': year,
                                    'country': country,
                                    'genre': genre,
                                    'director': director,
                                    'rating': rating,
                                    'summary': summary,
                                    'ager': ager,
                                    'poster': poster,
                                    'actors': actors})
                print(movies_list[-1]['title'], '\t\t\t', movies_list[-1]['actors'])
    except Exception as e:
        print(e)
    driver.close()
    return movies_list

a = getmovies()
# for i in a:
#     print(i['title'], '\t\t\t', i['ager'])