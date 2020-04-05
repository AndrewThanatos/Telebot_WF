from geopy.geocoders import Nominatim

locator = Nominatim(user_agent="myGeocoder")


def coord_to_city(coordinates):
    location = locator.reverse(coordinates, language='en')
    data = location.raw['address']
    country = data.get('country')
    state = data.get('state')

    if data.get('city') is not None:
        place = data.get('city')
    elif data.get('villige') is not None:
        place = data.get('villige')
    elif data.get('town') is not None:
        place = data.get('town')
    else:
        place = "Unknow"

    if country is None:
        country = "Unknow"
    if state is None:
        state = "Unknow"

    return (country, state, place)


def city_to_coord(name):
    location = locator.geocode(name)
    return "{} {}".format(location.latitude, location.longitude)


# coord = city_to_coord('Rivne')
# print(coord_to_city(coord), sep='\n')
