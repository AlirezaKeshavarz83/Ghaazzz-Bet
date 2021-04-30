import logging

import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

token = os.getenv("token")

updater = Updater(token, use_context=True)

st = {}
bet_message = {}
games = [["Esteghlal", "Al Shorta", {}]]

admins = [1203400559]

def start(update, context):
    user_id = update.message.chat.id
    f = 0
    try:
        st[user_id]
        f = 1
    except:
        f = 0
    if f == 0:
        update.message.reply_text("salam")
    else:
        update.message.reply_text("salami dobare")
    st[user_id] = 0
def bet(update, context):
    user_id = update.message.chat.id
    f = 0
    try:
        st[user_id]
        f = 1
    except:
        f = 0
    if f == 0:
        update.message.reply_text("ابتدا از دستور /start استفاده کنید.")
        return
    if st[user_id] != 0:
        update.message.reply_text("شما در استیت درست قرار ندارید.")
        return
    keys = []
    i = 0
    for game in games:
        keys.append([InlineKeyboardButton(text = game[0] + " - " + game[1],
                                            callback_data = "bet " + str(i))])
        i += 1
    markup = InlineKeyboardMarkup(keys)
    msg = "کدوم بت"
    bet_message[user_id] = update.message.reply_text(msg, reply_markup = markup, parse_mode='HTML')
    st[user_id] = []
def cancel(update, context):
    user_id = update.message.chat.id
    f = 0
    try:
        st[user_id]
        f = 1
    except:
        f = 0
    if f == 0:
        update.message.reply_text("ابتدا از دستور /start استفاده کنید.")
        return
    update.message.reply_text("شما در استیت مین قرار دارید.")
    st[user_id] = 0
def handle(update, context):
    user_id = update.message.chat.id
    f = 0
    try:
        st[user_id]
        f = 1
    except:
        f = 0
    if f == 0:
        update.message.reply_text("ابتدا از دستور /start استفاده کنید.")
        return
    if st[user_id] == 0:
        msg = update.message.text
        update.message.reply_text(msg)
        return
    if len(st[user_id]) == 0:
        msg = update.message.text
        try:
            x = int(msg)
        except:
            return
        x = x % len(games)
        st[user_id] += [x]
        try:
            games[st[user_id][0]][2][user_id]
            update.message.reply_text("شما قبلا پیش بینی کرده اید.")
            update.message.reply_text(games[st[user_id][0]][0] + " " +str(games[st[user_id][0]][2][user_id][1]) + 
            " - " + str(games[st[user_id][0]][2][user_id][2]) + " " + games[st[user_id][0]][1])
            st[user_id] = 0
        except:
            update.message.reply_text("تعداد گل " + games[st[user_id][0]][0] + " : ")
        return
    if len(st[user_id]) == 1:
        msg = update.message.text
        try:
            x = int(msg)
        except:
            return
        st[user_id] += [x]
        update.message.reply_text("تعداد گل " + games[st[user_id][0]][1] + " : ")
        return
    if len(st[user_id]) == 2:
        msg = update.message.text
        try:
            x = int(msg)
        except:
            return
        st[user_id] += [x]
        update.message.reply_text("فکت : ")
        return
    if len(st[user_id]) == 3:
        msg = update.message.text
        st[user_id] += [msg]
        try:
            games[st[user_id][0]][2][user_id]
            update.message.reply_text("شما قبلا پیش بینی کرده اید.")
            st[user_id] = 0
        except:
            games[st[user_id][0]][2][user_id] = st[user_id]
            update.message.reply_text("پیش بینی شما ذخیره شد.")
            st[user_id] = 0
        return

def handle_key(update, context):
    user_id = update.callback_query.from_user.id
    query = update.callback_query
    try:
        if(query.message.message_id != bet_message[user_id].message_id):
            return
    except:
        return
    if st[user_id] == 0:
        return
    if len(st[user_id]) != 0:
        return
    x = int(query.data[4:])
    bot = context.bot
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text = games[x][0] + ' - ' + games[x][1]
    )
    st[user_id] += [x]
    try:
        games[st[user_id][0]][2][user_id]
        bet_message[user_id].reply_text("شما قبلا پیش بینی کرده اید.")
        bet_message[user_id].reply_text(games[st[user_id][0]][0] + " " + str(games[st[user_id][0]][2][user_id][1]) + 
            " - " + str(games[st[user_id][0]][2][user_id][2]) + " " + games[st[user_id][0]][1])
        st[user_id] = 0
    except:
        bet_message[user_id].reply_text("تعداد گل " + games[st[user_id][0]][0] + " : ")

def add_admin(update, context):
    user_id = update.message.chat.id
    global admins

    print(user_id)
    if not user_id in admins:
        return
    admins += [context.args[0]]
#def add_game(update, context):


def prnt(update, context):
    user_id = update.message.chat.id
    global admins

    if not user_id in admins:
        return
    msg = ""
    for i in range(len(games)):
        msg += str(i) + "\n"
        for bt in games[i][2].keys():
            msg += " <a href=\"tg://user?id=" + str(bt) + "\">" + str(bt) + "</a>  " + str(games[i][2][bt][1]) + " - " + str(games[i][2][bt][2]) + "\n"
        msg += "\n"
    update.message.reply_text(msg, parse_mode="HTML")




dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("bet", bet))
dp.add_handler(CommandHandler("cancel", cancel))
dp.add_handler(CommandHandler("add_admin", add_admin))
dp.add_handler(CommandHandler("print", prnt))
dp.add_handler(MessageHandler(Filters.all & ~Filters.command, handle))
dp.add_handler(CallbackQueryHandler(handle_key, pattern = "^bet"))


updater.start_polling()

updater.idle()
