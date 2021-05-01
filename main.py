import logging

import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class Team:
    def __init__(self, name):
        self.name = name
class Bet:
    def __init__(self, user, game):
        self.user = user
        self.game = game
class Game:
    def __init__(self, first_team, second_team):
        self.first_team = first_team
        self.second_team = second_team
        self.bets = {}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

token = "1635730125:AAHUrL_TaPYlEwJW9IfinEPa94Bf9F34LDI" #os.getenv("token")

updater = Updater(token, use_context=True)

st = {}
bet_message = {}
games = []
user_bet = {}
add_teams = []

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
    st[user_id] = "main"
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
    if st[user_id] != "main":
        update.message.reply_text("شما در استیت درست قرار ندارید.")
        return
    if len(games) == 0:
        update.message.reply_text("در حال حاضر بازی ای برای شرط بندی وجود ندارد.")
        return

    keys = []
    i = 0
    for game in games:
        keys.append([InlineKeyboardButton(text = game.first_team.name + " - " + game.second_team.name,
                                            callback_data = "bet " + str(i))])
        i += 1
    markup = InlineKeyboardMarkup(keys)
    msg = "کدوم بت"
    bet_message[user_id] = update.message.reply_text(msg, reply_markup = markup, parse_mode='HTML')
    st[user_id] = "bet0"
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
    st[user_id] = "main"
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
    if st[user_id] == "main":
        return
    if st[user_id] == "bet0":
        msg = update.message.text
        try:
            x = int(msg)
        except:
            return
        x = x % len(games)
        user_bet[user_id] = Bet(update.message.from_user, games[x])
        st[user_id] = "bet1"
        try:
            user_bet[user_id].game.bets[user_id]
            update.message.reply_text("شما قبلا پیش بینی کرده اید.")
            update.message.reply_text(user_bet[user_id].game.first_team.name + " " + str(user_bet[user_id].game.bets[user_id].first_score) + 
            " - " + str(user_bet[user_id].game.bets[user_id].second_score) + " " + user_bet[user_id].game.second_team.name)
            st[user_id] = "main"
        except:
            update.message.reply_text("تعداد گل " + user_bet[user_id].game.first_team.name + " : ")
        return
    if st[user_id] == "bet1":
        msg = update.message.text
        try:
            x = int(msg)
        except:
            return
        user_bet[user_id].first_score = x
        st[user_id] = "bet2"
        update.message.reply_text("تعداد گل " + user_bet[user_id].game.second_team.name + " : ")
        return
    if st[user_id] == "bet2":
        msg = update.message.text
        try:
            x = int(msg)
        except:
            return
        user_bet[user_id].second_score = x
        st[user_id] = "bet3"
        update.message.reply_text("فکت : ")
        return
    if st[user_id] == "bet3":
        msg = update.message.text
        user_bet[user_id].facts = msg
        user_bet[user_id].time = update.message.date
        try:
            user_bet[user_id].game.bets[user_id]
            update.message.reply_text("شما قبلا پیش بینی کرده اید.")
            st[user_id] = "main"
        except:
            user_bet[user_id].game.bets[user_id] = user_bet[user_id]
            update.message.reply_text("پیش بینی شما ذخیره شد.")
            st[user_id] = "main"
        return
    if st[user_id] == "add0":
        name = update.message.text
        add_teams.append(Team(name))
        update.message.reply_text("نام تیم دوم:")
        st[user_id] = "add1"
        return
    if st[user_id] == "add1":
        name = update.message.text
        add_teams.append(Team(name))
        games.append(Game(add_teams[0], add_teams[1]))
        update.message.reply_text("بازی افزوده شد.")
        add_teams.clear()
        st[user_id] = "main"
        return

def handle_key(update, context):
    user_id = update.callback_query.from_user.id
    query = update.callback_query
    try:
        if(query.message.message_id != bet_message[user_id].message_id):
            return
    except:
        return
    if st[user_id] == "main":
        return
    if st[user_id] != "bet0":
        return
    x = int(query.data[4:])
    bot = context.bot
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text = games[x].first_team.name + ' - ' + games[x].second_team.name
    )
    user_bet[user_id] = Bet(update.callback_query.from_user, games[x])
    st[user_id] = "bet1"
    try:
        user_bet[user_id].game.bets[user_id]
        bet_message[user_id].reply_text("شما قبلا پیش بینی کرده اید.")
        bet_message[user_id].reply_text(user_bet[user_id].game.first_team.name + " " + str(user_bet[user_id].game.bets[user_id].first_score) + 
        " - " + str(user_bet[user_id].game.bets[user_id].second_score) + " " + user_bet[user_id].game.second_team.name)
        st[user_id] = "main"
    except:
        bet_message[user_id].reply_text("تعداد گل " + user_bet[user_id].game.first_team.name + " : ")

def add_admin(update, context):
    user_id = update.message.chat.id
    global admins

    if not user_id in admins:
        return
    admins += [context.args[0]]
def add_game(update, context):
    user_id = update.message.chat.id
    global admins

    if not user_id in admins:
        return
    update.message.reply_text("نام تیم اول:")
    st[user_id] = "add0"
def remove_game(update, context):
    user_id = update.message.chat.id
    global admins

    if not user_id in admins:
        return
    games.remove(games[int(context.args[0])])

def prnt(update, context):
    user_id = update.message.chat.id
    global admins

    if not user_id in admins:
        return
    if len(context.args) > 0:
        game = games[int(context.args[0])]
        for ii in context.args[1:]:
            i = int(ii)
            bt = list(game.bets.values())[i]
            msg = " <a href=\"tg://user?id=" + str(bt.user.id) + "\">" + bt.user.first_name + "</a>  " + str(bt.first_score) + " - " + str(bt.second_score) + "\n"
            msg += bt.facts + "\n"
            msg += str(bt.time) + "\n"
            update.message.reply_text(msg, parse_mode="HTML")
        return
    msg = ""
    for i in range(len(games)):
        msg += str(i) + ": " + games[i].first_team.name + " - " + games[i].second_team.name + "\n"
        j = 0
        for bt in games[i].bets.values():
            msg += "   " + str(j) + ": <a href=\"tg://user?id=" + str(bt.user.id) + "\">" + bt.user.first_name + "</a>  " + str(bt.first_score) + " - " + str(bt.second_score) + "\n"
            j += 1
        msg += "\n"
    update.message.reply_text(msg, parse_mode="HTML")




dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("bet", bet))
dp.add_handler(CommandHandler("cancel", cancel))
dp.add_handler(CommandHandler("add_admin", add_admin))
dp.add_handler(CommandHandler("add_game", add_game))
dp.add_handler(CommandHandler("remove_game", remove_game))
dp.add_handler(CommandHandler("print", prnt))
dp.add_handler(MessageHandler(Filters.all & ~Filters.command, handle))
dp.add_handler(CallbackQueryHandler(handle_key, pattern = "^bet"))


updater.start_polling()

updater.idle()
