from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

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
        for i in range(1, 6):
            driver.get('https://www.kinopoisk.ru/lists/movies/top250/?page=' + str(i))
            movies = driver.find_elements(By.CLASS_NAME, 'styles_root__ti07r')
            for m in movies:
                title = m.find_element(By.CLASS_NAME, 'styles_mainTitle__IFQyZ').text
                year = m.find_element(By.CLASS_NAME, 'desktop-list-main-info_secondaryText__M_aus').text.split(', ')
                if len(year) == 2:
                    year = int(year[0])
                else:
                    year = int(year[1])
                country = m.find_element(By.CLASS_NAME, 'desktop-list-main-info_truncatedText__IMQRP').text.split(' •')[0]
                movies_list.append({'title': title, 'year': year, 'country': country})
    except Exception as e:
        print(e)
    driver.close()
    return movies_list