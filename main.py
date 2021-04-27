import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

st = {}
games = [["Real Madrid", "Chelsea", {}], ["PSG", "Man City", {}]]

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
    msg = "کدوم بت"
    msg = msg + "\n"
    for i in range(len(games)):
        msg = msg + str(i) + ": " + games[i][0] + " - " + games[i][1] + "\n"
    update.message.reply_text(msg, parse_mode="HTML")
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
        update.message.reply_text("tedade gole " + games[st[user_id][0]][0] + " : ")
        return
    if len(st[user_id]) == 1:
        msg = update.message.text
        try:
            x = int(msg)
        except:
            return
        st[user_id] += [x]
        update.message.reply_text("tedade gole " + games[st[user_id][0]][1] + " : ")
        return
    if len(st[user_id]) == 2:
        msg = update.message.text
        try:
            x = int(msg)
        except:
            return
        st[user_id] += [x]
        update.message.reply_text("fact : ")
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


def add_admin(update, context):
    user_id = update.message.chat.id
    global admins

    print(user_id)
    if not user_id in admins:
        return
    admins += [context.args[0]]

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


updater = Updater("1635730125:AAHUrL_TaPYlEwJW9IfinEPa94Bf9F34LDI", use_context=True)

dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("bet", bet))
dp.add_handler(CommandHandler("cancel", cancel))
dp.add_handler(CommandHandler("add_admin", add_admin))
dp.add_handler(CommandHandler("print", prnt))
dp.add_handler(MessageHandler(Filters.all & ~Filters.command, handle))


updater.start_polling()

updater.idle()