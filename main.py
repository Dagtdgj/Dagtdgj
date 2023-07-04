import telebot
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Установка уровня логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

bot = telebot.TeleBot('5974483976:AAEaC2vsU_Rl9GpbQ0Tp-7t2rlBA1z3NnLM')

users = {}
# Словарь для хранения информации о замуте пользователей
muted_users = {}




@bot.message_handler(commands=["start"])
def start_command(message):
    bot.send_message(message.chat.id, """👋Привет! Я - бот-модератор.

🦾Я могу выдавать мут (/mute), кикать пользователя из чата (сообщества) (/ban), а также выдавать топ-пользователей за сегодня (/top) (данная функция является BETA, поэтому может не работать). P.S. все команды можно посмотреть в /help

👀Чтобы я мог это делать, тебе нужно добавить меня в чат (сообщество), назначить администратором и проверить, чтобы у меня был доступ к чату и нужным функциям.

Дополнительная информация/все команды - /help""")


@bot.message_handler(commands=["help"])
def start(m, res=False):
    bot.send_message(m.chat.id, """вот, что на данный момент я умею:

    /mute - выдавать мут пользователю на 1 час (3600 сек)
    /ban - кикать человека из чата
    /top - выдавать топ - пользователей за сегодня (данная функция является BETA, поэтому может не работать)
    /new_update - Здесь будет список новых обновлений бота, который обязательно будет дополнятся, а так же список того, что скоро будет обновлено в боте.

    что бы воспользоваться командами, вы должны ответить на сообщение пользователя, которого хотите забанить или же выдать мут.""")


@bot.message_handler(commands=["new_update"])
def new_update_command(message):
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id, f"""Привет, {user_name}! Ты попал(а) в раздел 'новые обновления'. Здесь будет список новых обновлений бота, который обязательно будет дополняться, а также список того, что скоро будет обновлено в боте!

Вышедшие обновления:

1. Наш новый Телеграм-бот для предложений/идей для нашего бота-модератора - @boostDlog_bot
2. Новая система команд /ban и /mute
3. Новые команды: /idea
4. Устранены баги команд /ban и /mute

Скоро:

1. Новая база данных для улучшаемой производительности бота и устранения ошибок + хранение данных команды /top
1.1. Финальная версия команды /top""")


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

# Определение функции is_moderator
def is_moderator(chat_id, user_id):
    # Здесь должна быть логика проверки, является ли пользователь модератором
    return  # Замените это на вашу логику


@bot.message_handler(commands=['ban'])
def ban_command(message):
    if not message.reply_to_message:
        bot.send_message(message.chat.id, "Ошибка: Необходимо ответить на сообщение пользователя, которого вы хотите забанить.")
        return

    user_to_ban = message.reply_to_message.from_user
    if user_to_ban:
        user_id = user_to_ban.id
        chat_id = message.chat.id
        if not is_owner(chat_id, user_id):
            if user_id == bot.get_me().id:
                bot.send_message(chat_id, "Вы не можете использовать эту команду на сообщении бота.")
            elif user_id == message.from_user.id:
                bot.send_message(chat_id, "Вы не можете использовать эту команду на своем собственном сообщении.")

            else:
                bot.send_message(
                    chat_id,
                    f"Вы уверены, что хотите забанить пользователя {user_to_ban.first_name}?",
                    reply_markup=get_confirmation_keyboard('ban', user_id),
                )
        else:
            bot.send_message(chat_id, "Невозможно удалить владельца чата")
    else:
        bot.send_message(chat_id, "Не удалось определить пользователя для бана.")

@bot.message_handler(commands=['mute'])
def mute_command(message):
    if not message.reply_to_message:
        bot.send_message(message.chat.id, "Ошибка: Необходимо ответить на сообщение пользователя, которому вы хотите выдать мут.")
        return

    user_to_mute = message.reply_to_message.from_user
    if user_to_mute:
        user_id = user_to_mute.id
        chat_id = message.chat.id
        if user_id == bot.get_me().id:
            bot.send_message(chat_id, "Вы не можете использовать эту команду на сообщении бота.")
        elif user_id == message.from_user.id:
            bot.send_message(chat_id, "Вы не можете использовать эту команду на своем собственном сообщении.")
        elif is_owner(chat_id, user_id):  # Добавляем проверку на владельца чата
            bot.send_message(chat_id, "Невозможно выдать мут владельцу чата.")
        else:
            bot.send_message(
                chat_id,
                f"Вы уверены, что хотите выдать мут пользователю {user_to_mute.first_name} на 1 час?",
                reply_markup=get_confirmation_keyboard('mute', user_id),
            )
    else:
        bot.send_message(chat_id, "Не удалось определить пользователя для выдачи мута")



@bot.message_handler(commands=['ban'])
def ban_command(message):
    user_to_ban = message.reply_to_message.from_user
    if user_to_ban:
        user_id = user_to_ban.id
        chat_id = message.chat.id
        if not is_owner(chat_id, user_id):
            if user_id == bot.get_me().id:
                bot.send_message(chat_id, "Вы не можете использовать эту команду на сообщении бота.")
            elif user_id == message.from_user.id:
                bot.send_message(chat_id, "Вы не можете использовать эту команду на своем собственном сообщении.")
            else:
                bot.send_message(
                    chat_id,
                    f"Вы уверены, что хотите забанить пользователя {user_to_ban.first_name}?",
                    reply_markup=get_confirmation_keyboard('ban', user_id),
                )
        else:
            bot.send_message(chat_id, "Невозможно удалить владельца чата")
    else:
        bot.send_message(chat_id, "Не удалось определить пользователя для бана.")

@bot.message_handler(commands=['mute'])
def mute_command(message):
    if not message.reply_to_message:
        bot.send_message(message.chat.id, "Ошибка: Необходимо ответить на сообщение пользователя, которому вы хотите выдать мут.")
        return

    user_to_mute = message.reply_to_message.from_user
    if user_to_mute:
        user_id = user_to_mute.id
        chat_id = message.chat.id
        if user_id == bot.get_me().id:
            bot.send_message(chat_id, "Вы не можете использовать эту команду на сообщении бота.")
        elif user_id == message.from_user.id:
            bot.send_message(chat_id, "Вы не можете использовать эту команду на своем собственном сообщении.")
        elif is_owner(chat_id, user_id):  # Добавляем проверку на владельца чата
            bot.send_message(chat_id, "Невозможно выдать мут владельцу чата.")
        else:
            bot.send_message(
                chat_id,
                f"Вы уверены, что хотите выдать мут пользователю {user_to_mute.first_name} на 1 час?",
                reply_markup=get_confirmation_keyboard('mute', user_id),
            )
    else:
        bot.send_message(chat_id, "Не удалось определить пользователя для выдачи мута")




@bot.message_handler(commands=['ban'])
def ban_command(message):
    user_to_ban = message.reply_to_message.from_user
    if user_to_ban:
        user_id = user_to_ban.id
        chat_id = message.chat.id
        if not is_owner(chat_id, user_id):
            bot.send_message(
                chat_id,
                f"Вы уверены, что хотите забанить пользователя {user_to_ban.first_name}?",
                reply_markup=get_confirmation_keyboard('ban', user_id),
            )
        else:
            bot.send_message(chat_id, "Невозможно удалить владельца чата")

@bot.message_handler(commands=['mute'])
def mute_command(message):
    if not message.reply_to_message:
        bot.send_message(message.chat.id, "Ошибка: Необходимо ответить на сообщение пользователя, которому вы хотите выдать мут.")
        return

    user_to_mute = message.reply_to_message.from_user
    if user_to_mute:
        user_id = user_to_mute.id
        chat_id = message.chat.id
        if user_id == bot.get_me().id:
            bot.send_message(chat_id, "Вы не можете использовать эту команду на сообщении бота.")
        elif user_id == message.from_user.id:
            bot.send_message(chat_id, "Вы не можете использовать эту команду на своем собственном сообщении.")
        elif is_owner(chat_id, user_id):  # Добавляем проверку на владельца чата
            bot.send_message(chat_id, "Невозможно выдать мут владельцу чата.")
        else:
            bot.send_message(
                chat_id,
                f"Вы уверены, что хотите выдать мут пользователю {user_to_mute.first_name} на 1 час?",
                reply_markup=get_confirmation_keyboard('mute', user_id),
            )
    else:
        bot.send_message(chat_id, "Не удалось определить пользователя для выдачи мута")





def get_confirmation_keyboard(action, user_id):
    confirm_button = InlineKeyboardButton(
        'Подтвердить',
        callback_data=f'confirm_{action}_{user_id}',
    )
    cancel_button = InlineKeyboardButton(
        'Отмена',
        callback_data=f'cancel_{action}_{user_id}',
    )
    keyboard = InlineKeyboardMarkup().add(confirm_button, cancel_button)
    return keyboard

def is_owner(chat_id, user_id):
    chat_member = bot.get_chat_member(chat_id, user_id)
    return chat_member.status == 'creator'

@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    if call.data.startswith('confirm'):
        command, user_id = call.data.split('_')[1], call.data.split('_')[2]
        if command == 'ban':
            chat_id = call.message.chat.id
            if not is_owner(chat_id, user_id):
                bot.kick_chat_member(chat_id, user_id)
                bot.answer_callback_query(call.id, 'Пользователь кикнут из чата')
            else:
                bot.answer_callback_query(call.id, 'Невозможно удалить владельца чата')
        elif command == 'mute':
            chat_id = call.message.chat.id
            bot.restrict_chat_member(chat_id, user_id, until_date=datetime.now() + timedelta(seconds=3600))
            bot.answer_callback_query(call.id, 'Пользователю выдан мут на 1 час')
        bot.delete_message(chat_id, call.message.message_id)

    elif call.data.startswith('cancel'):
        chat_id = call.message.chat.id
        bot.delete_message(chat_id, call.message.message_id)
        bot.answer_callback_query(call.id, 'Действие отменено')


try:
    bot.polling()
except telebot.apihelper.ApiTelegramException as e:
    print(f"An error occurred while polling the bot: {str(e)}")
