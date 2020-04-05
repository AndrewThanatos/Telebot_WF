import requests
import json
from math import trunc

api_key = 'b1fbbf4bb415925e1aed8d1a09aaad0b'


def K_to_C(temp):
    return temp - 273


def get_data(coords, degree):
    lat, lon = coords.split()
    api_request = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
    req = requests.get(api_request)
    data = json.loads(req.text)
    weather = data['weather'][0]
    main = data['main']
    new_data = {
        'main': weather['main'],
        'description': weather['description'],
        'temp': trunc(int(main['temp'])),
        'feels_like': trunc(int(main['feels_like']))
    }
    if degree == 'celsius':
        new_data['temp'] = K_to_C(new_data['temp'])
        new_data['feels_like'] = K_to_C(new_data['feels_like'])
    return new_data

