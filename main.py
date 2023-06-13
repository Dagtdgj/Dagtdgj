import telebot

bot = telebot.TeleBot("напишите сюда свой API токен", parse_mode=None)

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, """👋Привет! Я - бот-модератор. 
    
    🦾Я могу выдавать мут (/mute) и кикать пользователя из чата (сообщества) (/ban)
    
    👀Что бы я мог это делать, тебе нужно добавить меня в чат (сообщество), назначить администратором и проверить, что бы у меня был доступ к чату и нужным функциям.
     
     доп. информация - /help""")

@bot.message_handler(commands=["help"])
def start(m, res=False):
    bot.send_message(m.chat.id, """вот, что на данный момент я умею:
    
    /mute - выдавать мут пользователю на 1 час (3600 сек)
    
    /ban - кикать человека из чата
    
    что бы воспользоваться командами, вы должны ответить на сообщение пользователя, которого хотите забанить или же выдать мут.
    
    ненужная информация - /dop""")

    @bot.message_handler(commands=["dop"])
    def dop(m, res=False):
        bot.send_message(m.chat.id, """Привет, человек! Если ты написал эту команду, скорее всего тебе либо интересно что она выдает, либо ты пришел немного почитать про меня)
        
        На самом деле я был написан на языке - Python. Если так интересно, то вот мой код - https://github.com/Dagtdgj/Dagtdgj
        
        Мой код на самом деле довольно длинный, но очень простой. Он написан в 57 строчек кода, причем без ипользования интернета, разве что нейросети, которая исправляла ошибки в коде, на случай если мой создатель не понял как их исправить. Что бы написать такого бота, достаточно знать базовые знания Python, не больше)
        
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

bot.polling()
