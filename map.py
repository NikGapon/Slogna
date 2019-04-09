import requests
import sys
import math
import pygame.image

coord_to_geo_x = 0.0000428
coord_to_geo_y = 0.0000428


class Map:

    def __init__(self):
        self.lat = 55.729738
        self.lon = 37.664777
        self.zoom = 10
        self.type = "map"
        self.map = None
        self.show_index = False

        self.search_result = None
        self.use_postal_code = False

    def ll(self):
        return "{0},{1}".format(self.lon, self.lat)

    def set(self, **kwargs):
        for key in kwargs.keys():
            if key == 'lat':
                self.lat = kwargs[key]
            elif key == 'lon':
                self.lon = kwargs[key]
            elif key == 'zoom':
                self.zoom = kwargs[key]
            elif key == 'type':
                self.type = kwargs[key]
            elif key == 'search_result':
                self.search_result = kwargs[key]
                if self.search_result is not None:
                    self.lon, self.lat = self.search_result.get_coords()
            elif key == 'show_index':
                self.show_index = kwargs[key]
        self._update_map()

    def get_map(self):
        if self.map is None:
            self._update_map()
        return self.map

    def _update_map(self):
        try:
            map_request = "http://static-maps.yandex.ru/1.x/"
            if self.search_result is None:
                map_params = {
                    "ll": self.ll(),
                    "z": self.zoom,
                    "l": self.type,
                    "size": "600,450"
                }
            else:
                map_params = {
                    "ll": self.ll(),
                    "z": self.zoom,
                    "l": self.type,
                    "size": "600,450",
                    "pt": "{0},{1},pm2dgl".format(self.lon, self.lat)
                }
            response = requests.get(map_request, params=map_params)

            if not response:
                print("Ошибка выполнения запроса:")
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)
        except Exception:
            print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
            sys.exit(1)

        map_file = "map.png"
        try:
            with open(map_file, "wb") as file:
                file.write(response.content)
        except IOError as ex:
            print("Ошибка записи временного файла:", ex)
            sys.exit(2)
        self.map = pygame.image.load(map_file)

    def screen_to_geo(self, pos):
        dy = 225 - pos[1]
        dx = pos[0] - 300
        lx = self.lon + dx * coord_to_geo_x * math.pow(2, 15 - self.zoom)
        ly = self.lat + dy * coord_to_geo_y * math.cos(math.radians(self.lat)) * math.pow(2, 15 - self.zoom)
        return lx, ly


class RequestResult:

    def __init__(self, request):
        geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode={}&format=json".format(request)
        try:
            response = requests.get(geocoder_request)
            if response:
                json_response = response.json()
                self.toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                toponym_address = self.toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
                try:
                    self.postal_code = self.toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
                except KeyError:
                    self.postal_code = ''
                toponym_coodrinates = self.toponym["Point"]["pos"]
                self.lon, self.lat = [float(x) for x in toponym_coodrinates.split()]
                self.address = toponym_address
            else:
                print("Ошибка выполнения запроса:")
                print(geocoder_request)
                print("Http статус:", response.status_code, "(", response.reason, ")")
        except:
            print("Запрос не удалось выполнить. Проверьте подключение к сети Интернет.")

    def get_coords(self):
        return self.lon, self.lat
