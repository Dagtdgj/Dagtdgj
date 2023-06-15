import telebot
from datetime import datetime, timedelta

bot = telebot.TeleBot('5974483976:AAEaC2vsU_Rl9GpbQ0Tp-7t2rlBA1z3NnLM')

users = {}

@bot.message_handler(commands=["start"])
def start_command(message):
    bot.send_message(message.chat.id, """👋Привет! Я - бот-модератор.

🦾Я могу выдавать мут (/mute), кикать пользователя из чата (сообщества) (/ban), а так же выдавать топ - пользователей за сегодня (/top) (данная функция является BETA, поэтому может не работать)

    👀Что бы я мог это делать, тебе нужно добавить меня в чат (сообщество), назначить администратором и проверить, что бы у меня был доступ к чату и нужным функциям.

    доп. информация - /help""")

@bot.message_handler(commands=["help"])
def start(m, res=False):
    bot.send_message(m.chat.id, """вот, что на данный момент я умею:
    /mute - выдавать мут пользователю на 1 час (3600 сек)
    /ban - кикать человека из чата
    /top - выдавать топ - пользователей за сегодня (данная функция является BETA, поэтому может не работать)

    что бы воспользоваться командами, вы должны ответить на сообщение пользователя, которого хотите забанить или же выдать мут.
    ненужная информация - /dop""")

@ bot.message_handler(commands=["dop"])
def dop(m, res=False):
    bot.send_message(m.chat.id, """Привет, человек! Если ты написал эту команду, скорее всего тебе либо интересно что она выдает, либо ты пришел немного почитать про меня)

На самом деле я был написан на языке - Python. Если так интересно, то вот мой код - https://github.com/Dagtdgj/Dagtdgj

Мой код на самом деле довольно длинный, но очень простой. Он написан в 107 строчек кода. Что бы написать такого бота, достаточно знать базовые знания Python, не больше)

Я надеюсь эта информация дала вам хоть какие-то новые знания. Меня будут дорабатывать и добавлять новые команды/функции, а так я только BETA - версия.

Приятно было пообщаться, до новых встреч!""")


@bot.message_handler(commands=['mute'])
def mute_user(message):
    chat_id = message.chat.id
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bot.restrict_chat_member(chat_id, user_id, until_date=3600) # на 1 час
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

# обработчик события нового пользователя в чате@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for member in message.new_chat_members:
        bot.send_message(message.chat.id, f"Привет, {member.first_name}! Добро пожаловать в чат!\nПросим вас представиться в чате, т.к. кто-то вас знает, а кто-то даже не имеет понятия кто в чате)\nблагодарю за понимание :)")

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
            message_text += f"{i+1}. {user_data[0]} - {user_data[1]} сообщений\n"
        bot.send_message(chat_id, message_text)
    else:
        bot.send_message(chat_id, 'На сегодня нет данных о сообщениях пользователей')

        # получаем информацию о чате
        chat_info = bot.get_chat(chat_id='CHAT_ID')

        # получаем список администраторов чата
        admins = bot.get_chat_administrators(chat_id='CHAT_ID')

        # получаем идентификатор пользователя, отправившего команду
        user_id = update.message.from_user.id

        # проверяем, является ли пользователь администратором чата
        is_admin = False
        for admin in admins:
            if admin.user.id == user_id:
                is_admin = True
                break

        # если пользователь не является администратором чата, отправляем ему сообщение
        if not is_admin:
            bot.send_message(chat_id=user_id, text='Вы не являетесь администратором этого чата.')


bot.polling()
