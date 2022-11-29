import telebot
import requests


def get_exchange():
    pass


bot = telebot.TeleBot('5759812289:AAGyL0rOvMsYfLxDcky5uvmACI8x9TnVJAU')

@bot.message_handler(commands=['start'])
def start(message):
    mess = f'<b>Привет, мигрант {message.from_user.first_name}!</b> Добро пожаловать в страну!'
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == 'Hello':
        bot.send_message(message.chat.id, 'И тебе привет!', parse_mode='html')
    elif message.text.lower() == 'места':
        bot.send_message(message.chat.id, 'В твоем городе есть такие достопримечательности:', parse_mode='html')
    elif message.text.lower() == 'english':
        bot.send_message(message.chat.id, 'Word of day is ', parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Извини, насяльника, моя твоя ни панимать', parse_mode='html')

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
