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
from bot_tele.utils import horoscope, time_sleeps
from get_api.get_answer_simsimi import get_answer_simsimi
from get_api.xsmb import xsmb
from logs.logs import setup_logger 

# logger = setup_logger('logs.log')
simsimi_log = setup_logger("simsimi.log")
xsmb_log = setup_logger('xsmb_log.log')
# tuvi_log = setup_logger('tuvi.log')

BOT_TOKEN = config.BOT_TOKEN
tb = telebot.TeleBot(BOT_TOKEN)

@tb.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    tb.reply_to(message, "Hello, how are you doing?")

#-------------------------
# xem bói tử vi cung hoàng đạo  + ngày
@tb.message_handler(commands=['horoscope', 'tuvi', 'Tuvi', 'Horoscope'])
def sign_handler(message):
    text = "What's your zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
    sent_msg = tb.send_message(message.chat.id, text, parse_mode="Markdown")
    tb.register_next_step_handler(sent_msg, day_handler)

def day_handler(message):
    sign = message.text
    text = "What day do you want to know?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date in format YYYY-MM-DD."
    sent_msg = tb.send_message(
        message.chat.id, text, parse_mode="Markdown")
    tb.register_next_step_handler(
        sent_msg, horoscope.fetch_horoscope, sign.capitalize())
    


#----------------------------
# chat voi simsimi
@tb.message_handler(commands=['simsimi', 'sim'])
def start_simsimi(message) :
    quess = ' '.join(map(str, (message.text.split()[1:])))
    answer = get_answer_simsimi(quess)
    tb.send_message(message.chat.id, answer.json()['message'])
    simsimi_log.info('Quess: {}'.format(quess))
    simsimi_log.info('Answer: {}'.format(answer.json()['message']))



#-----------------------------------------------
# AI MidJourney
@tb.message_handler(commands=['draw'])
def aiMidJourney(message) :
    tb.send_message(message.chat.id, 'oke')


#--------------------------------------
# Sleep
@tb.message_handler(commands=['sleep', 'Sleep'])
def Sleep(message) :
    hours, minutes, meridiems =  time_sleeps.sleep_times()
    txt = time_sleeps.message_sleep_now(hours= hours, minutes= minutes, meridiems= meridiems)
    tb.reply_to(message, txt)

#---------------------------------------
# xsmb
@tb.message_handler(commands=['xsmb'])
def sign_handler(message):
    text = xsmb()
    tb.send_message(message.chat.id, text)
    xsmb_log.info(text)

# Handles all sent documents and audio files
@tb.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    tb.reply_to(message.chat.id, 'gui file del gi day')


@tb.message_handler(func=lambda msg: True)
def echo_all(message):
    tb.reply_to(message, 'Tôi không hiểu câu lệnh của bạn.')


# def main():
tb.infinity_polling()
