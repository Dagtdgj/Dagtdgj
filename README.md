import telebot
from datetime import datetime, timedelta

bot = telebot.TeleBot('P.S. тут мой API токен, но я удалил его из кода тк это конфеденциальная тема')

users = {}


@bot.message_handler(commands=["start"])
def start_command(message):
    bot.send_message(message.chat.id, """👋Привет! Я - бот-модератор.

🦾Я могу выдавать мут (/mute), кикать пользователя из чата (сообщества) (/ban), а так же выдавать топ - пользователей за сегодня (/top) (данная функция является BETA, поэтому может не работать)  P.S. все команды можно посмотреть в /help

    👀Что бы я мог это делать, тебе нужно добавить меня в чат (сообщество), назначить администратором и проверить, что бы у меня был доступ к чату и нужным функциям.

    доп. информация/все команды - /help""")


@bot.message_handler(commands=["help"])
def start(m, res=False):
    bot.send_message(m.chat.id, """вот, что на данный момент я умею:

    /mute - выдавать мут пользователю на 1 час (3600 сек)
    /ban - кикать человека из чата
    /top - выдавать топ - пользователей за сегодня (данная функция является BETA, поэтому может не работать)
    /new_update - Здесь будет список новых обновлений бота, который обязательно будет дополнятся, а так же список того, что скоро будет обновлено в боте.

    что бы воспользоваться командами, вы должны ответить на сообщение пользователя, которого хотите забанить или же выдать мут.""")


@bot.message_handler(commands=["idea"])
def start(m, res=False):
    bot.send_message(m.chat.id, """Приветствую! Вы попали в раздел "идея". Мы создали нашего нового телеграм-бота, в котором вы можете предложить идею для нашего Бота-модератора! Вы можете предложить новые команды и их функции, что то поменять, и т.п.. 

    Ждем ваших идей в нашем телеграм-боте!  @boostDlog_bot""")


@bot.message_handler(commands=['top'])
def top_users(message):
    chat_id = message.chat.id
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    top_users = []
    for user_id, message_count in users.items():
        user = bot.get_chat_member(chat_id, user_id)
        if user.status not in ['creator', 'administrator', 'bot']:
            user_messages = bot.get_chat_history(chat_id, limit=1000, user_id=user_id)
            count_today = sum(1 for m in user_messages if m.date.date() == today.date())
            count_yesterday = sum(1 for m in user_messages if m.date.date() == yesterday.date())
            top_users.append((user.user.first_name, count_today, count_yesterday))
    top_users = sorted(top_users, key=lambda x: x[1], reverse=True)[:3]
    if top_users:
        message_text = 'Топ-3 пользователей за сегодня:\n'
        for i, user_data in enumerate(top_users):
            message_text += f"{i + 1}. {user_data[0]} - {user_data[1]} сообщений\n"
        bot.send_message(chat_id, message_text)
    else:
        bot.send_message(chat_id, 'На сегодня нет данных о сообщениях пользователей')


@bot.message_handler(commands=["new_update"])
def handle_start(message):
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id,
                     f"""Привет, {user_name}! Ты попал(а) в раздел 'новые обновления'. Здесь будет список новых обновлений бота, который обязательно будет дополнятся, а так же список того, что скоро будет обновлено в боте!


Вышедшие обновления:         

1. Наш новый Телеграм-бот для предложений/идей для нашего бота-модератора    -   @boostDlog_bot 

Скоро:

1. Новая база данных для улучшаемой производительности бота и устранения ошибок + хранение данных команды /top

1.1. Финальная версия команды /top

2. Устранение бага команд, которые действуют на бота (этого не должно быть)""")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.reply_to_message:
        if message.text == '/ban':
            if message.reply_to_message.from_user.id == bot.get_me().id:
                bot.reply_to(message, "Нельзя использовать команды на самом боте")
            elif message.reply_to_message.from_user.id == message.from_user.id:
                bot.reply_to(message, "Нельзя использовать команду на себе")
            else:
                # Perform ban logic here
                # Send confirmation message with buttons
                keyboard = telebot.types.InlineKeyboardMarkup()
                confirm_button = telebot.types.InlineKeyboardButton(text="Продолжить", callback_data="ban_confirm")
                cancel_button = telebot.types.InlineKeyboardButton(text="Отмена", callback_data="ban_cancel")
                keyboard.add(confirm_button, cancel_button)
                bot.reply_to(message, "Вы уверены, что хотите забанить пользователя?", reply_markup=keyboard)
        elif message.text == '/mute':
            if message.reply_to_message.from_user.id == bot.get_me().id:
                bot.reply_to(message, "Нельзя использовать команды на самом боте")
            elif message.reply_to_message.from_user.id == message.from_user.id:
                bot.reply_to(message, "Нельзя использовать команду на себе")
            else:
                # Perform mute logic here
                # Send confirmation message with buttons
                keyboard = telebot.types.InlineKeyboardMarkup()
                confirm_button = telebot.types.InlineKeyboardButton(text="Продолжить", callback_data="mute_confirm")
                cancel_button = telebot.types.InlineKeyboardButton(text="Отмена", callback_data="mute_cancel")
                keyboard.add(confirm_button, cancel_button)
                bot.reply_to(message, "Вы уверены, что хотите выдать мут пользователю?", reply_markup=keyboard)

                @bot.message_handler(commands=['mute'])
                def mute_user(message):
                    chat_id = message.chat.id
                    if message.reply_to_message:
                        user_id = message.reply_to_message.from_user.id
                        bot.restrict_chat_member(chat_id, user_id, until_date=3600)  # на 1 час
                    else:
                        bot.reply_to(message, "Вы должны ответить на сообщение пользователя, которого хотите замутить.")

                @bot.message_handler(commands=['ban'])
                def ban_user(message):
                    chat_id = message.chat.id
                    if message.reply_to_message:
                        user_id = message.reply_to_message.from_user.id
                        bot.kick_chat_member(chat_id, user_id)
                    else:
                        bot.reply_to(message, "Вы должны ответить на сообщение пользователя, которого хотите забанить.")


try:
    bot.polling()
except telebot.apihelper.ApiTelegramException as e:
    print(f"An error occurred while polling the bot: {str(e)}")
