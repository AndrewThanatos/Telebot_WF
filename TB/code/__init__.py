import telebot
from flask import Flask
from code.config import TOKEN

app = Flask(__name__)
bot = telebot.TeleBot(TOKEN)

import code.main
