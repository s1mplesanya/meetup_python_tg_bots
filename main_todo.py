import telebot
from telebot import types

from config import token

# Замените 'token' (файл config.py) на реальный токен вашего бота
bot = telebot.TeleBot(token)

# Замените ID себя (его можно узнать когда задаешь вопрос, он написан в | |, он же message.from_user.id)
myUserId = 123456789

# Словарь для хранения вопросов
questions = {}

# Клавиатура с главным меню
main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
item_ask_question = types.KeyboardButton("Задать вопрос ❓")
item_about_us = types.KeyboardButton("Обо мне 👨‍💻")
main_menu.add(item_ask_question)
main_menu.add(item_about_us)

# Клавиатура с кнопкой ответить
answer_markup = types.InlineKeyboardMarkup()
item_answer = types.InlineKeyboardButton("Ответить", callback_data='answer')
answer_markup.add(item_answer)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! 👋", reply_markup=main_menu)

# Обработчик всего текста, который мы вводим в бота
@bot.message_handler(content_types='text')
def main_menu_handler(message):
    user_id = message.chat.id
    if message.text == "Задать вопрос ❓":
        bot.send_message(user_id, "Введите ваш вопрос 🤷‍♂️", reply_markup=types.ReplyKeyboardRemove()) # reply_markup=types.ReplyKeyboardRemove() - удаляет reply клавиатуру (в нашем случае это mainMenu)
        bot.register_next_step_handler(message, save_question)
    elif message.text == "Обо мне 👨‍💻":
        # выведите какую-нибудь информацию о себе   
        pass
    else:
        # это условие отвечает за то, чтобы наш бот просто повторял за нами, если он не нашел такого пункта меню
        bot.send_message(user_id, message.text, reply_markup=main_menu, parse_mode="Markdown")



# Обработчик ввода вопроса, сохранение его в словарь и отправка этого вопроса myUserId
def save_question(message):
    user_id = message.from_user.id
    question_text = message.text.strip()
    if question_text != "":
        questions[str(user_id)] = question_text
        # отправьте здесь сообщение самому себе и myUserId (ему обязательно отправить сообщение с текстом '|{message.chat.id}|', 
        # иначе наш обработчик не найдет id пользователя), оформите сообщение как хотите 
        # также добавить в сообщение user_id reply_markup с главным меню
        # P.S. parse_mode="Markdown" добавляет возможность редактирования текста. К примеру "*Ваш вопрос успешно отправлен!*" - делает текст жирным, _text_ - курсив

    else:
        bot.send_message(user_id, "Вы не можете отправить пустой вопрос ❌", reply_markup=main_menu, parse_mode="Markdown")


# Обработчик кнопки "Ответить"
@bot.callback_query_handler(func=lambda call: call.data == 'answer')
def answer_question(call):
    user_id = call.from_user.id
    message_text = call.message.text
    question_sender_id = message_text.split('|')[1].split('|')[0]

    if user_id == myUserId:
        if question_sender_id in questions:
            # создайте переменную msg с сообщением пользователю user_id о просьбе ввести ответ на вопрос
            # создайте register_next_step_handler с сообщением msg и функцией inputAnswer, передайте также туда question_sender_id
            pass # pass нужно просто для заполнения условия "пустотой", его можно убрать
        else:
            bot.send_message(user_id, "На этот вопрос уже ответили 🙅‍♂️", parse_mode="Markdown")
    else:
        bot.send_message(user_id, "У вас нет доступа к ответам на вопросы.", parse_mode="Markdown")


      
def inputAnswer(message, question_sender_id):
    answerText = message.text.strip()
    user_id = message.chat.id

    # отправьте сообщение user_id об успешно отправке
    # отправьте сообщение int(question_sender_id) о том, что на его вопрос ответил {message.from_user.first_name} и желательно не забыть отправить ответ {answerText}

    questions.pop(question_sender_id) # удаляет id пользователя, который задавал вопрос, из словаря


def main():
    print("Бот запущен. Нажмите Control+Z для завершения")

    # добавьте запуск бота

if __name__ == "__main__":
    main()