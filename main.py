import telebot
from telebot import types
import os



token = ""
bot = telebot.TeleBot(token)

name = ''
surname = ''
age = 0


@bot.message_handler(commands=['button']) #Обработчик команды  button
def button_message(message): 
    """Функция создаёт клавиатуру и кнопки"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # Клавиатура
    item1 = types.KeyboardButton("Регистрация") # Кнопка 1
    item2 = types.KeyboardButton("👁️Глаза👁️") # Кнопка 2
    markup.add(item1, item2)                # Добавление кноопок на клавиатуру
    bot.send_message(message.chat.id,'Выберите функцию',reply_markup=markup)

@bot.message_handler(content_types=['text']) # Обработчик текста (любого)
def start(message):
    if message.text == 'Регистрация' or message.text == "/reg":
        form_reg(message)# Вызов функции form_reg с аргументом message
    elif message.text == '👁️Глаза👁️':
        send = bot.send_message(message.from_user.id, 'Присылайте свои фото...')
        bot.register_next_step_handler(send, download_photo) # Функция ждёт событие от пользователя, после чего запускает download_photo
    elif message.text == '/help':
        bot.send_message(message.from_user.id, 'Команды: \n/reg - Регистрация\n/button - Кнопки\n')
    else:
        bot.send_message(message.from_user.id, 'Привет 🤖✋\nДля помощи пиши команду: /help')

#@bot.message_handler(content_types=['photo']) # Обработчик фото
def download_photo(message): 
    """Функция скачивает фото на комп"""
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)          # Подготавливаем файл на скачивание
    downloaded_file = bot.download_file(file_info.file_path)                         # Скачиваем сам файл в переменную downloaded_file 
    src = './img/' + message.photo[1].file_id + '.jpg' # Относительный путь и имя фото
    with open(src, 'wb') as file:   # Функция open() открывает файл, на запись байтов и присваем в переменную file
                                    # Оператор with даёт возможность не закрывать самому файл после записи
        file.write(downloaded_file) # Записываем файл в путь который указали
    bot.reply_to(message, "Фото добавлено") # Сообщение, что загрузка OK
        

def form_reg(message):
    bot.send_message(message.from_user.id, "Как тебя зовут?")
    bot.register_next_step_handler(message, get_name )

def get_name(message): 
    """Функция получения имени"""
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname, )

def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id,'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    global age
    age = message.text
    # Нужно дописать исключение, если пользователь введёт не цифру, а букву!!!
    bot.send_message(message.from_user.id, "Имя: "+name+"\nФамилия: "+surname+"\nВозвраст: "+age)
    # Дальше можно записать данные (name, surname, age и т.д.) в БД

bot.polling(none_stop=True, interval=0)
