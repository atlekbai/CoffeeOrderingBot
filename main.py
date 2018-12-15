# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: atlekbai <atlekbai@student.unit.ua>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/12/14 12:08:55 by atlekbai          #+#    #+#              #
#    Updated: 2018/12/14 12:08:55 by atlekbai         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)
logger = logging.getLogger(__name__)

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Bot
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram.ext import MessageHandler, Filters
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from Shop import *
from util import *
import re


cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ubobrakyiv.firebaseio.com' })
orders = db.reference('orders')

TOKEN = '626240872:AAGd7TpPfxthvc58yxQczqNlM5C2TRX77Mw'
adminToken = "784780047:AAHM5_Bi5bJy5i4Rje8_giIxpzYkadO7CSc"
MENU_SWITCH, PANINI_MENU, COFFEE_MENU, COFFEE_SIZE, TIME = range(5)
admin = Bot(adminToken)

def footerCheck(bot, query, user_data):
	data = int(query.data)
	if (data == 101): # Готово button
		if not user_data['order']:
			editMessage(bot, query, shop.phrases['empty'])
			return (ConversationHandler.END)
		editMessage(bot, query, getOrders(user_data) + shop.phrases['time'])
		return (TIME)
	return (200)

def startFunc(bot, update):
	sendMessage(bot, update, shop.phrases['start'])

def menuFunc(bot, update, user_data):
	user_data['order'] = list()
	user_data['price'] = 0
	user_data['chat_id'] = update.message.chat.id
	user_data['name'] = ""
	if (update.message.chat.first_name):
		user_data['name'] = update.message.chat.first_name + " "
	if (update.message.chat.last_name):
		user_data['name'] += update.message.chat.last_name
	sendMessage(bot, update, shop.phrases['main_menu'], mainMenu(shop))
	return (MENU_SWITCH)

def menuSwitch(bot, update, user_data):
	query = update.callback_query
	data = int(query.data)

	if (data == 0):
		editMessage(bot, query, shop.phrases['menu_cof'], markupMenu(shop.menu, data))
		return (COFFEE_MENU)
	if (data == 1):
		editMessage(bot, query, shop.phrases['menu_pan'], markupPanini(shop, data))
		return (PANINI_MENU)
	check = footerCheck(bot, query, user_data)
	if (check != 200): return (check)
	if (data == 103):
		editMessage(bot, query,  shop.phrases['cancel'])
		return (ConversationHandler.END)

def paniniMenu(bot, update, user_data):
	query = update.callback_query
	data = int(query.data)
	check = footerCheck(bot, query, user_data)
	if (check != 200): return (check)
	if (data == 103):
		editMessage(bot, query,  shop.phrases['main_menu'], mainMenu(shop))
		return (MENU_SWITCH)
	user_data['order'].append(Order(data, 0, 1))
	user_data['price'] += shop.objects[1][data].price[0]
	return (PANINI_MENU)

def coffeeMenu(bot, update, user_data):
	query = update.callback_query
	data = int(query.data)
	
	check = footerCheck(bot, query, user_data)
	if (check != 200): return (check)
	if (data == 103):
		editMessage(bot, query,  shop.phrases['main_menu'], mainMenu(shop))
		return (MENU_SWITCH)

	user_data['type'] = 0
	user_data['coffee'] = data
	editMessage(bot, query, shop.objects[0][data].name + " какой?", markupCoffee(shop.objects[0][data]))
	return (COFFEE_SIZE)

def coffeeSize(bot, update, user_data):
	query = update.callback_query
	data = int(query.data)	
	if (data == 100 or data == 101):
		orders = getOrders(user_data)
	
	if (data == 100): # Назад buttton
		editMessage(bot, query, shop.phrases['menu_cof'] + orders, markupMenu(shop.menu, 0))
		return (COFFEE_MENU)

	if (data == 101): # Готово button
		if not user_data['order']:
			editMessage(bot, query, shop.phrases['empty'])
			return (ConversationHandler.END)
		editMessage(bot, query, orders + shop.phrases['time'])
		return (TIME)

	user_data['order'].append(Order(user_data['coffee'], data, user_data['type']))
	user_data['price'] += shop.objects[user_data['type']][user_data['coffee']].price[data]
	return (COFFEE_SIZE)

def timeGet(bot, update, user_data):
	time = update.message.text
	matchObj = re.match( r'([0-9]{1,2}):([0-9]{2})', time)
	
	if (matchObj):
		user_data['time'] = time
		orders.push(toJson(user_data, shop))
		admin.send_message(chat_id=389337650, text="Новый заказ!")
		sendMessage(bot, update, shop.phrases['order_ok'] + getInvitation(matchObj))
		return (ConversationHandler.END)

	sendMessage(bot, update, shop.phrases['time_fail'])
	return (TIME)

def cancel(bot, update, user_data):
	sendMessage(bot, update, shop.phrases['cancel'])
	return (ConversationHandler.END)

def main():
	"""
		Start the bot
	"""
	fillShop(shop)
	updater = Updater(token=TOKEN)
	dispatcher = updater.dispatcher

	conv_handler = ConversationHandler(
        entry_points=[CommandHandler('menu', menuFunc, pass_user_data=True)],
        states={
            MENU_SWITCH:	[CallbackQueryHandler(menuSwitch, pass_user_data=True)],
            PANINI_MENU:	[CallbackQueryHandler(paniniMenu, pass_user_data=True)],
            COFFEE_MENU:	[CallbackQueryHandler(coffeeMenu, pass_user_data=True)],
            COFFEE_SIZE:	[CallbackQueryHandler(coffeeSize, pass_user_data=True)],
            TIME:			[MessageHandler(Filters.text, timeGet, pass_user_data=True)]
        },
        fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
    )
	dispatcher.add_handler(conv_handler)
	dispatcher.add_handler(CommandHandler('start', startFunc))

	updater.start_polling()
	updater.idle()

if (__name__ == '__main__'):
	main()
