import telebot
from telebot import types

from config import token

# Замените 'token' (файл config.py) на реальный токен вашего бота и 'myUserId'
bot = telebot.TeleBot(token)

# Замените ID себя (его можно узнать когда задаешь вопрос, он написан в скобочках)
myUserId = 654953623

# Словарь для хранения вопросов
questions = {}

# Клавиатура с главным меню
main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
item_ask_question = types.KeyboardButton("Задать вопрос ❓")
item_about_us = types.KeyboardButton("О мне 👨‍💻")
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
    elif message.text == "О мне 👨‍💻":
        # выведите какую-нибудь информацию о себе
        bot.send_message(user_id, "Меня зовут *Александр*\nЯ студент 3️⃣ курса *факультета информационных технологий* 👨‍💻\n", reply_markup=main_menu, parse_mode="Markdown")

        add_information = "Для интересующихся, дополнительную информацию можно найти здесь:\n\
🤖 [Курс написания ботов](https://mastergroosha.github.io/telegram-tutorial/docs/lesson_01/)\n\
👾 [Ссылка на код данного бота](https://github.com/s1mplesanya/meetup_python_tg_bots)"
        bot.send_message(user_id, add_information, reply_markup=main_menu, parse_mode="Markdown")


# Обработчик ввода вопроса, сохранение его в словарь и отправка этого вопроса myUserId
def save_question(message):
    user_id = message.from_user.id
    question_text = message.text.strip()
    if question_text != "":
        questions[str(user_id)] = question_text
        # отправьте здесь сообщение самому себе и myUserId (ему обязательно отправить сообщение с параметром '|{message.chat.id}|', 
        # иначе наш обработчик не найдет id пользователя), оформите его как хотите 
        # также добавить в сообщение user_id reply_markup с главным меню
        # P.S. parse_mode="Markdown" добавляет возможность редактирования текста. К примеру "*Ваш вопрос успешно отправлен!*" - делает текст жирным, _text_ - курсив

        bot.send_message(user_id, "*Ваш вопрос успешно отправлен! ✅*", reply_markup=main_menu, parse_mode="Markdown")
        bot.send_message(myUserId, f"👤 {message.from_user.first_name} (@{message.from_user.username}) |{message.chat.id}| задал вопрос:\n\n{message.text}", reply_markup=answer_markup, parse_mode="Markdown")

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

            msg = bot.send_message(user_id, 'Введите ваш ответ 💌', parse_mode="Markdown")
            bot.register_next_step_handler(msg, inputAnswer, question_sender_id)
        else:
            bot.send_message(user_id, "На этот вопрос уже ответили 🙅‍♂️", parse_mode="Markdown")
    else:
        bot.send_message(user_id, "У вас нет доступа к ответам на вопросы.", parse_mode="Markdown")


      
def inputAnswer(message, question_sender_id):
    answerText = message.text.strip()
    user_id = message.chat.id

    # отправьте сообщение user_id об успешно отправке
    # отправьте сообщение int(question_sender_id) о том, что на его вопрос ответил {message.from_user.first_name} и желательно не забыть отправить ответ {answerText}

    bot.send_message(user_id, "*Ваш ответ успешно отправлен! ✅*", parse_mode="Markdown")
    bot.send_message(int(question_sender_id), f"👤 {message.from_user.first_name} (@{message.from_user.username}) ответил на ваш вопрос:\n\n{answerText}", parse_mode="Markdown")

    questions.pop(question_sender_id) # удаляет id пользователя, который задавал вопрос, из словаря


def main():
    print("Бот запущен. Нажмите Control+Z для завершения")

    # добавьте запуск бота
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()