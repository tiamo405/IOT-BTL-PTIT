# -*- coding: utf-8 -*-

import os
import sys
root = os.getcwd()
pwd = os.path.dirname(os.path.realpath("bot_tele"))
sys.path.insert(0, root)
import telebot
cwd = os.getcwd()
sys.path.append(os.path.abspath(os.path.dirname(cwd)))
sys.path.insert(0, cwd)
import config

from sensor.api import mocua, dongcua
USER_CHAT_ID = config.USER_CHAT_ID
BOT_TOKEN = config.BOT_TOKEN
tb = telebot.TeleBot(BOT_TOKEN)

class MyBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        # chạy lệnh khi nhận đc mess như trong commands
        @self.bot.message_handler(commands=['start', 'hello'])
        def send_welcome(message):
            self.send_welcome_message(message)
        # chạy lệnh khi nhận đc mess như trong commands
        @self.bot.message_handler(commands=['mocua', 'open'])
        def open(message):
            self.mo_cua(message)
        # chạy lệnh khi nhận đc mess như trong commands
        @self.bot.message_handler(commands=['dongcua', 'close'])
        def close(message):
            self.dong_cua(message)

    # gửi thông báo kèm hình ảnh
    def send_notification(self, text, path_image, chat_id = USER_CHAT_ID):
        with open(path_image, 'rb') as photo:
            self.bot.send_photo(chat_id, photo)
        self.bot.send_message(chat_id, text)

    # test mesage
    def send_welcome_message(self, message):
        self.bot.reply_to(message, "Hello, how are you doing?")
    
    # lệnh đóng mở chửa
    def mo_cua(self, message):
        noti = mocua()
        self.bot.reply_to(message, noti)
    def dong_cua(self, message):
        noti = dongcua()
        self.bot.reply_to(message, noti)
    
    # cái này để ghi nhận sự kiện hay sao ý, quên rùi
    def start_polling(self):
        self.bot.polling(none_stop=True)


# Chạy bot
if __name__ == "__main__":
    mybot = MyBot(token= BOT_TOKEN)
    mybot.start_polling()    