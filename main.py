import pygame
import requests
import sys
import os

import math

from common.distance import lonlat_distance
from common.geocoder import geocode as reverse_geocode
from common.business import find_business

# Подобранные констатны для поведения карты.
LAT_STEP = 0.008  # Шаги при движении карты по широте и долготе
LON_STEP = 0.02
coord_to_geo_x = 0.0000428  # Пропорции пиксельных и географических координат.
coord_to_geo_y = 0.0000428
LINE_WIDTH = 250
LINE_HEIGHT = 30
LINE_X = 10
LINE_Y = 400
BTN_WIDTH = 30
text = ""
FPS = 60
map_image = None
point = None


def ll(x, y):
    return "{0},{1}".format(x, y)



# Параметры отображения карты:
# координаты, масштаб, найденные объекты и т.д.

class MapParams(object):
    # Параметры по умолчанию.
    def __init__(self):
        self.lat = 55.729738  # Координаты центра карты на старте.
        self.lon = 37.664777
        self.zoom = 10  # Масштаб карты на старте.
        self.type = "map"  # Тип карты на старте.

        self.search_result = None  # Найденный объект для отображения на карте.
        self.use_postal_code = False

    # Преобразование координат в параметр ll
    def ll(self):
        return ll(self.lon, self.lat)

    # Обновление параметров карты по нажатой клавише.
    def update(self, event):
        pass

    # Преобразование экранных координат в географические.
    def screen_to_geo(self, pos):
        dy = 225 - pos[1]
        dx = pos[0] - 300
        lx = self.lon + dx * coord_to_geo_x * math.pow(2, 15 - self.zoom)
        ly = self.lat + dy * coord_to_geo_y * math.cos(math.radians(self.lat)) * math.pow(2, 15 - self.zoom)
        return lx, ly

    # еще несколько функций


# Создание карты с соответствующими параметрами.
def load_map(mp):
    global map_image
    try:
        map_request = "http://static-maps.yandex.ru/1.x/?ll={}&z={}&l={}".format(mp.ll(), mp.zoom, mp.type)
        if point is not None:
            map_params = {
                # позиционируем карту центром на наш исходный адрес
                "ll": mp.ll(),
                "z": mp.zoom,
                "l": mp.type,
                "pt": "{0},{1},pm2dgl".format(*point)
            }
        else:
            map_params = {
                # позиционируем карту центром на наш исходный адрес
                "ll": mp.ll(),
                "z": mp.zoom,
                "l": mp.type
            }
        response = requests.get(map_request, params=map_params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
    except:
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    map_image = map_file


def check_keys(e, mp):
    global text
    if e.key == pygame.K_BACKSPACE:
        if text:
            text = text[:-1]
        return
    if e.key == pygame.K_KP_ENTER:
        search(mp)
        return
    text += e.unicode


def search(mp):
    global text, point
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode={}&format=json".format(text)

    # Выполняем запрос.
    response = None
    try:
        response = requests.get(geocoder_request)
        if response:
            # Преобразуем ответ в json-объект
            json_response = response.json()

            # Получаем первый топоним из ответа геокодера.
            # Согласно описанию ответа, он находится по следующему пути:
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            # Полный адрес топонима:
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            # Координаты центра топонима:
            toponym_coodrinates = toponym["Point"]["pos"]
            # Печатаем извлечённые из ответа поля:
            print(toponym_address, "имеет координаты:", toponym_coodrinates)
            print(type(toponym_coodrinates))
            mp.lon, mp.lat = [float(x) for x in toponym_coodrinates.split()]
            point = [float(x) for x in toponym_coodrinates.split()]
            load_map(mp)
        else:
            print("Ошибка выполнения запроса:")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
    except:
        print("Запрос не удалось выполнить. Проверьте подключение к сети Интернет.")


def main():
    global text
    # Инициализируем pygame
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    TEXT_FONT = pygame.font.Font(None, 25)
    clock = pygame.time.Clock()

    # Заводим объект, в котором будем хранить все параметры отрисовки карты.
    mp = MapParams()
    load_map(mp)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Выход из программы
                running = False
                break
            elif event.type == pygame.KEYUP:  # Обрабатываем различные нажатые клавиши.
                mp.update(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP and mp.zoom < 19 and mp.zoom > 0:
                    mp.zoom += 1
                elif event.key == pygame.K_PAGEDOWN and mp.zoom < 19 and mp.zoom > 0:
                    mp.zoom -= 1
                check_keys(event, mp)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if LINE_X + LINE_WIDTH <= event.pos[0] <= LINE_X + LINE_WIDTH + BTN_WIDTH \
                        and LINE_Y <= event.pos[1] <= LINE_Y + LINE_HEIGHT:
                    search(mp)
            # другие eventы
        # Загружаем карту, используя текущие параметры.

        # Рисуем картинку, загружаемую из только что созданного файла.
        screen.blit(pygame.image.load(map_image), (0, 0))

        pygame.draw.rect(screen, pygame.Color('white'), (
            LINE_X,
            LINE_Y,
            LINE_WIDTH,
            LINE_HEIGHT
        ), 0)

        if text:
            render = TEXT_FONT.render(text, 1, (0, 0, 0))
        else:
            render = TEXT_FONT.render("Поиск...", 1, pygame.Color('grey'))
        text_x = LINE_X + 5
        text_y = LINE_Y + (LINE_HEIGHT - render.get_height()) // 2
        screen.blit(render, (text_x, text_y))

        pygame.draw.rect(screen, pygame.Color('green'), (
            LINE_X + LINE_WIDTH,
            LINE_Y,
            BTN_WIDTH,
            LINE_HEIGHT
        ))

        # Переключаем экран и ждем закрытия окна.
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    # Удаляем за собой файл с изображением.


if __name__ == "__main__":
    main()
