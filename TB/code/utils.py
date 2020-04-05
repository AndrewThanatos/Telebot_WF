def getSticker(name):
    path = 'code/static/stickers/'
    return open(path+name, 'rb').read()


def print_location(country, state, city):
    text = ''
    if country != 'Unknow':
        text += 'Country: ' + country + '\n'
    if state != 'Unknow':
        text += 'State: ' + state + '\n'
    if city != 'Unknow':
        text += 'City/Villige: ' + city + '\n'
    return text
