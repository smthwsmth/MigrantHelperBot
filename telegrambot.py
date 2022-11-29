import telebot

bot = telebot.TeleBot('5759812289:AAGyL0rOvMsYfLxDcky5uvmACI8x9TnVJAU')

@bot.message_handler(commands=['start'])
def start(message):
    mess = f'<b>Привет, мигрант {message.from_user.first_name}!</b> Добро пожаловать в страну!'
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler()
def get_user_text(message):
    if message.text == 'Hello':
        bot.send_message(message.chat.id, 'И тебе привет!', parse_mode='html')
    elif message.text.lower() == 'места':
        bot.send_message(message.chat.id, 'В твоем городе есть такие достопримечательности:', parse_mode='html')
    elif message.text.lower() == 'english':
        bot.send_message(message.chat.id, 'Word of day is ', parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Извини, насяльника, моя твоя ни панимать', parse_mode='html')

  






bot.polling(non_stop=True)
