import telebot
from telebot import types
import requests
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep


def get_exchange_uz():
    url = 'https://bank.uz/currency'
    browser = Chrome('/home/smthwsmth/Desktop/chromedriver')
    browser.get(url)

    button = browser.find_element(By.CSS_SELECTOR, '#best_USD > div > div > div.organization-contacts > div.bc-inner-blocks-left > a')  #нажатие кнопки "Все банки"
    button.send_keys("\n") #send enter for links, buttons

    #browser.execute_script("arguments[0].click();", button)
    #the option above is the way to overcome error "Element is not clickable at point (X,Y)"
    info_buy = []
    info_sell = []
    max_ljust = 0
    bank_buy = browser.find_element(By.CLASS_NAME, 'bc-inner-block-left').find_elements(By.CLASS_NAME, 'bc-inner-block-left-texts  ')
    bank_sell = browser.find_element(By.CLASS_NAME, 'bc-inner-blocks-right').find_elements(By.CLASS_NAME, 'bc-inner-block-left-texts  ')
    for i in bank_buy:
        name_bank = i.find_element(By.CLASS_NAME, 'medium-text').text.strip()
        act_course = i.find_element(By.CLASS_NAME, 'green-date').text.strip()
        info_buy.append(f"{name_bank.ljust(15)}----->{act_course}")
    for i in bank_sell:
        name_bank = i.find_element(By.CLASS_NAME, 'medium-text').text.strip()
        act_course = i.find_element(By.CLASS_NAME, 'green-date').text.strip()
        info_sell.append(f"{name_bank.ljust(15)}----->{act_course}")

    return info_buy, info_sell


bot = telebot.TeleBot('5759812289:AAGyL0rOvMsYfLxDcky5uvmACI8x9TnVJAU')

@bot.message_handler(commands=['start'])
def start(message):
    mess = f'<b>Привет, мигрант {message.from_user.first_name}!</b> Добро пожаловать в страну! Путешествовать сложно, а мигрировать ещё сложнее.\
        \nЯ буду тебе помогать на первых этапах. Считай, что я NPC в начале игры.\nВведи <b>/country</b> и выбери страну, куда ты прибыл.'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['country'])               
def website(message):
    markup  = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    country1 = types.KeyboardButton('Узбекистан')
    markup.add(country1)
    bot.send_message(message.chat.id, 'Список стран, в которых у меня есть связи и я охотно тебе помогу освоиться:',reply_markup=markup)


@bot.message_handler(commands=['currency'])
def act_currency(message):
    bot.send_message(message.chat.id, 'Подожди чуток, я наберу Бахтийара и узнаю курс валют. Не отключайся')
    currency_buy, currency_sell = get_exchange_uz()
    bot.send_message(message.chat.id, '<b>ПОКУПКА</b>', parse_mode='html')
    for i in currency_buy:
        bot.send_message(message.chat.id, i)
    bot.send_message(message.chat.id, '<b>ПРОДАЖА</b>', parse_mode='html')
    for i in currency_sell:
        bot.send_message(message.chat.id, i)

@bot.message_handler(commands=['best_curr'])
def act_currency(message):
    bot.send_message(message.chat.id, 'Подожди чуток, я наберу Бахтийара и узнаю курс валют. Не отключайся')
    currency_buy, currency_sell = get_exchange_uz()
    bot.send_message(message.chat.id, '<b>ПОКУПКА</b>', parse_mode='html')
    for num, i in enumerate(currency_buy):
        if num < 5:
            bot.send_message(message.chat.id, i)
    bot.send_message(message.chat.id, '<b>ПРОДАЖА</b>', parse_mode='html')
    for num, i in enumerate(currency_sell):
        if num < 5:
            bot.send_message(message.chat.id, i)

@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == 'Hello':
        bot.send_message(message.chat.id, 'И тебе привет!', parse_mode='html')
    elif message.text.lower() == 'места':
        bot.send_message(message.chat.id, 'В твоем городе есть такие достопримечательности:', parse_mode='html')
    elif message.text.lower() == 'english':
        bot.send_message(message.chat.id, 'Word of day is ', parse_mode='html')
    elif message.text.lower() == 'узбекистан':
        bot.send_message(message.chat.id, 'В этой стране я могу узнать для тебя: выгодный курс валют (/currency - информация по всем банкам, /best_curr - первые 5 банков)')
    else:
        bot.send_message(message.chat.id, 'Извини, насяльника, моя твоя ни панимать', parse_mode='html')

#@bot.message_handler(content_types=['website'])               отправляет кнопку с ссылкой
#def website(message):
#    markup  = types.InlineKeyboardMarkup()
#    markup.add(types.InlineKeyboardButton("Посетить веб-сайт", url="vk.com"))
#    bot.send_message(message.chat.id, 'Перейдите на сайт', reply_markup=markup)
#
#    bot.send_message(message.chat.id )
@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    bot.send_message(message.chat.id, 'Я не вижу изображение - для меня это набор двоичных последовательностей. Но как бы там ни было, порядок цифр красивый')

@bot.message_handler(content_types=['video'])
def get_user_video(message):
    bot.send_message(message.chat.id, 'Ты смеешься? Я все ещё программа и не могу смотреть видео. Пришли мне это в виде 0 и 1')

@bot.message_handler(content_types=['audio'])
def get_user_audio(message):
    bot.send_message(message.chat.id, 'Ха-ха. Аудио такое забавное, когда не понимаешь его')





bot.polling(non_stop=True)
