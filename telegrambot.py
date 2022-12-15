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

class Exchange:
    def get_exchange_uz(self):
        self.url = 'https://bank.uz/currency'
        self.browser = Chrome('/home/smthwsmth/Desktop/chromedriver')
        self.browser.get(self.url)

        self.button = self.browser.find_element(By.CSS_SELECTOR, '#best_USD > div > div > div.organization-contacts > div.bc-inner-blocks-left > a')  #нажатие кнопки "Все банки"
        self.button.send_keys("\n") #send enter for links, buttons

        #browser.execute_script("arguments[0].click();", button)
        #the option above is the way to overcome error "Element is not clickable at point (X,Y)"
        self.info_buy = []
        self.info_sell = []
        self.bank_buy = self.browser.find_element(By.CLASS_NAME, 'bc-inner-block-left').find_elements(By.CLASS_NAME, 'bc-inner-block-left-texts  ')
        self.bank_sell = self.browser.find_element(By.CLASS_NAME, 'bc-inner-blocks-right').find_elements(By.CLASS_NAME, 'bc-inner-block-left-texts  ')
        for i in self.bank_buy:
            self.name_bank = i.find_element(By.CLASS_NAME, 'medium-text').text.strip()
            self.act_course = i.find_element(By.CLASS_NAME, 'green-date').text.strip()
            self.info_buy.append(f"{self.name_bank.ljust(5)}--->за 1$ ты получишь {self.act_course}")
        for i in self.bank_sell:
            self.name_bank = i.find_element(By.CLASS_NAME, 'medium-text').text.strip()
            self.act_course = i.find_element(By.CLASS_NAME, 'green-date').text.strip()
            self.info_sell.append(f"{self.name_bank.ljust(5)}--->{self.act_course} просят за 1$")

        return self.info_buy, self.info_sell


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
    
    keyboard = types.InlineKeyboardMarkup()
    key_full = types.InlineKeyboardButton(text='Курс всех банков', callback_data='all')
    key_main = types.InlineKeyboardButton(text='Только лучший курс', callback_data='part')
    keyboard.add(key_full, key_main)
    question = 'Отобразить информацию по всем банкам или только лучший курс?'
    bot.send_message(message.chat.id, question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    bot.send_message(call.message.chat.id, 'Подожди чуток, я наберу Бахтийара и узнаю курс валют. Не отключайся')
    currency = Exchange()    #make an instance of class
    currency_buy, currency_sell = currency.get_exchange_uz()
    if call.data == 'all':
        bot.send_message(call.message.chat.id, '<b>ПОКУПКА</b>', parse_mode='html')
        for i in currency_buy:
            bot.send_message(call.message.chat.id, i)
        bot.send_message(call.message.chat.id, '<b>ПРОДАЖА</b>', parse_mode='html')
        for i in currency_sell:
            bot.send_message(call.message.chat.id, i)
    elif call.data == 'part':
        bot.send_message(call.message.chat.id, '<b>ПОКУПКА</b>', parse_mode='html')
        for num, i in enumerate(currency_buy):
            if num < 5:
                bot.send_message(call.message.chat.id, i)
        bot.send_message(call.message.chat.id, '<b>ПРОДАЖА</b>', parse_mode='html')
        for num, i in enumerate(currency_sell):
            if num < 5:
                bot.send_message(call.message.chat.id, i)


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
