import telebot
from code import bot
from flask import Flask, request
from code.models import app
from telebot import types
from telebot.types import (
    InlineKeyboardButton, InlineKeyboardMarkup
)
from code.db_utils import (
    isinDataBase, add_User, change_City, get_City, change_Unit,
    get_Unit, get_Coords, change_County,
    change_State, change_Coords
)
from code.utils import (
    getSticker, print_location
)
from code.config import (
    TOKEN, commands, messages
)
from code.forecast import (
    get_data
)
from code.geo import (
    city_to_coord, coord_to_city
)



def check_City(chat_id, city_name, mess_succ, mess_erros, func):
    try:
        coords = city_to_coord(city_name)
        country, state, city_name = coord_to_city(coords)

        _ = get_data(coords, get_Unit(chat_id))
        change_City(chat_id, city_name)
        change_State(chat_id, state)
        change_County(chat_id, country)
        change_Coords(chat_id, coords)
        bot.send_message(chat_id, messages['check_add_City'],
                         reply_markup=main_forcast_markup())
        bot.send_message(chat_id, "Your current location is\n"
                         + print_location(country, state, city_name))
    except:
        question(chat_id, messages['check_add_City_error'], func)


def check_update_City(message):
    chat_id = message.chat.id
    check_City(chat_id, message.text, messages['check_update_City'],
               messages['check_update_City_error'], 'check_update_City')


def check_add_City(message):
    chat_id = message.chat.id
    check_City(chat_id, message.text, messages['check_add_City'],
               messages['check_add_City_error'], 'check_add_City')


def question(chat_id, message, callback):
    markup = types.ForceReply()
    city = bot.send_message(chat_id, message,
                            reply_markup=markup)
    bot.register_next_step_handler(city, callback)


def main_forcast_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Get Weather Forecast')
    itembtn2 = types.KeyboardButton('Settings')
    markup.add(itembtn1, itembtn2)
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    if not isinDataBase(chat_id):
        add_User(chat_id)
        bot.send_message(chat_id, messages['first_hello'])

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           one_time_keyboard=True)
        itembtn1 = types.KeyboardButton('Get Started')
        markup.add(itembtn1)
        bot.send_sticker(chat_id, getSticker('hello_again.webp'))
        bot.send_message(chat_id, messages['get_started'],
                         reply_markup=markup)

    else:
        bot.send_message(chat_id, messages['hello_again'],
                         reply_markup=main_forcast_markup())
        bot.send_sticker(chat_id, getSticker('hello.webp'))


@bot.message_handler(commands=['home'])
def send_help(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Home, sweet home)',
                     reply_markup=main_forcast_markup())


@bot.message_handler(commands=['help'])
def send_help(message):
    chat_id = message.chat.id
    help_text = messages['help_message']
    for comm, text in commands.items():
        help_text += '/' + comm + ': '
        help_text += text + '\n'
    bot.send_message(chat_id, help_text)


@bot.message_handler(func=lambda message: message.text == 'Get Started')
def get_started(message):
    chat_id = message.chat.id

    if get_City(chat_id) is None:
        question(chat_id, 'Please enter your city', check_add_City)
    else:
        bot.send_message(chat_id, 'You already started)')


@bot.message_handler(func=lambda message: message.text == 'Get Weather Forecast')
def show_main_forecast(message):
    chat_id = message.chat.id
    try:
        text = 'Here is your forecast:\n'
        coords = get_Coords(chat_id)
        data = get_data(coords, get_Unit(chat_id))
        for key, value in data.items():
            text += key + ": " + str(value) + '\n'
        bot.send_message(chat_id, text)
    except AttributeError:
        if isinDataBase(message.chat.id):
            bot.send_message(chat_id, messages['something_wrong'])
        else:
            bot.send_message(chat_id, messages['get_started_again'])
            add_User(chat_id)
            get_started(message)


@bot.message_handler(func=lambda message: message.text == 'Account Settings')
def show_account_settings(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Change City')
    itembtn2 = types.KeyboardButton('Change Degree Unit')
    itembtn3 = types.KeyboardButton('Go Home')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(chat_id, "Choose what do you want", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Change City')
def change_user_city(message):
    chat_id = message.chat.id
    question(chat_id, 'Please enter your city', check_add_City)


@bot.message_handler(func=lambda message: message.text == 'Change Degree Unit')
def change_user_unit(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Celsius", callback_data="celsius"),
               InlineKeyboardButton("Kelvin", callback_data="kelvin"))
    bot.send_message(message.chat.id, "Which one?", reply_markup=markup)


@bot.message_handler(content_types=['location'])
def handle_location(message):
    chat_id = message.chat.id
    try:
        coords = str(message.location.latitude) + " " + \
            str(message.location.longitude)
        country, state, city_name = coord_to_city(coords)

        _ = get_data(coords, get_Unit(chat_id))
        change_City(chat_id, city_name)
        change_State(chat_id, state)
        change_County(chat_id, country)
        change_Coords(chat_id, coords)
        bot.send_message(chat_id, messages['check_add_City'],
                         reply_markup=main_forcast_markup())
        bot.send_message(chat_id, "Your current location is\n"
                         + print_location(country, state, city_name))
    except:
        bot.send_message(
            chat_id, "Something went wrong please resend your location")


@bot.message_handler(func=lambda message: message.text == 'Go Home')
def go_home(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Here you go)",
                     reply_markup=main_forcast_markup())


@bot.message_handler(func=lambda message: message.text == 'Settings')
@bot.message_handler(commands=['settings'])
def goto_settings(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Account Settings')
    itembtn2 = types.KeyboardButton('General Settings')
    itembtn3 = types.KeyboardButton('Go Home')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(chat_id, "Choose what do you want", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def change_unit_callback(call):
    chat_id = call.message.chat.id
    if call.data == "celsius":
        change_Unit(chat_id, "celsius")
    if call.data == "kelvin":
        change_Unit(chat_id, "kelvin")
    bot.edit_message_text(messages['degree_unit_upgrade'],
                          chat_id, call.message.message_id)


@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://fierce-inlet-68297.herokuapp.com/' + TOKEN)
    return "!", 200


