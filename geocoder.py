from io import BytesIO

import requests
from PIL import Image


def geocode(address):
    # Собираем запрос для геокодера.
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
        # Получаем первый топоним из ответа геокодера.
        features = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        return features if features else None


# Получаем координаты объекта по его адресу.
def get_coordinates(address):
    toponym = geocode(address)
    if not toponym:
        return (None, None)

    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Широта, преобразованная в плавающее число:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return float(toponym_longitude), float(toponym_lattitude)


# Находим ближайшие к заданной точке объекты заданного типа.
def search_all(adress_ll, span, object):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {
        "apikey": api_key,
        "text": object,
        "lang": "ru_RU",
        "ll": adress_ll,
        "spn": span,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)
    if not response:
        # ...
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()

    # Получаем найденные организации.
    organizations = json_response["features"]

    return organizations


# Поиск ближайшей организации по адресу
def search(adress_ll, span, object, k):
    orgs = search_all(adress_ll, span, object)
    if len(orgs):
        if len(orgs) > k:
            return orgs[:k]
        return orgs


def show_map(lon_lat, span, type, point=None):
    if point is None:
        map_params = {
            "ll": lon_lat,
            "spn": span,
            "l": type
        }
    else:
        map_params = {
            "l": type,
            "pt": point
        }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    Image.open(BytesIO(response.content)).show()
