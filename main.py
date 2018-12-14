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

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram.ext import MessageHandler, Filters
from Shop import Shop, Coffee, User
import re

TOKEN = '626240872:AAGd7TpPfxthvc58yxQczqNlM5C2TRX77Mw'
COFFEE, TIME_REQUEST, TIME = range(3)
shop = Shop()

def startFunc(bot, update):
	"""
		User info:
		user_id = update.message.chat.id
		first_name = update.message.chat.first_name
		last_name = update.message.chat.last_name
		username = update.message.chat.username
	"""
	bot.send_message(chat_id=update.message.chat_id, text=shop.phrases['start'])

def menuFunc(bot, update):
	reply_markup = InlineKeyboardMarkup(createMarkupMenu(shop.menu))
	bot.send_message(chat_id=update.message.chat_id, text=shop.phrases['menu'], reply_markup=reply_markup)
	return (COFFEE)

def coffeeType(bot, update, user_data):
	query = update.callback_query
	coffeeId = int(query.data)
	
	user_data['coffeeId'] = coffeeId
	user_data['chat_id'] = query.message.chat.id
	user_data['name'] = query.message.chat.first_name + " " + query.message.chat.last_name

	reply_markup = InlineKeyboardMarkup(createMarkupCoffee(shop.objects[coffeeId]))
	bot.edit_message_text(
		chat_id=query.message.chat_id,
		message_id=query.message.message_id,
		reply_markup=reply_markup,
		text=shop.objects[coffeeId].name + " какой?"
		)
	return (TIME_REQUEST)

def timeRequest(bot, update, user_data):
	query = update.callback_query
	coffeeSizeId = int(query.data)
	user_data['coffeeSizeId'] = coffeeSizeId
	bot.edit_message_text(
		chat_id=query.message.chat_id,
		message_id=query.message.message_id,
		text=shop.phrases['time'])
	return (TIME)

def timeGet(bot, update, user_data):
	time = update.message.text
	matchObj = re.match( r'([0-9]{1,2}):([0-9]{2})', time)
	if (matchObj):
		text =	"\nТвой заказ: " + coffeeFull(shop.objects[user_data['coffeeId']], user_data['coffeeSizeId']) + \
				"\nПриходи в " + matchObj.group(1) + ":" + matchObj.group(2)
		user_data['time'] = time
		print(user_data)
		bot.send_message(
			chat_id=update.message.chat_id,
			text=shop.phrases['order_ok'] + text
			)
		return (ConversationHandler.END)
	bot.send_message(chat_id=update.message.chat_id, text=shop.phrases['time_fail'])
	return (TIME)

def cancel(bot, update, user_data):
	bot.send_message(chat_id=update.message.chat_id, text=shop.phrases['cancel'])
	return (ConversationHandler.END)

def fillShop(_shop_):
	_shop_.addObject('Капучино', [200, 340, 500], [20, 35, 30])
	_shop_.addObject('Латте', [200, 340, 500], [20, 35, 30])
	_shop_.addObject('Американо', [50, 100], [10, 15])
	_shop_.addObject('Флет Уайт', [200, 340], [24, 26])

def createMarkupCoffee(coffee):
	"""
		Create ReplyMarkup for choosing coffee details
	"""
	button_list = [];
	for i in range(len(coffee.size)):
		text = str(coffee.size[i]) + " мл.\t" + str(coffee.price[i] )+ " грн."
		button_list.append([InlineKeyboardButton(text, callback_data=i)])
	return (button_list)

def createMarkupMenu(menu):
	"""
		Create ReplyMarkup out of menu
	"""
	button_list = [];
	for i, obj in enumerate(menu):
		button_list.append([InlineKeyboardButton(obj, callback_data=i)])
	return (button_list)

def coffeeFull(coffee, size_id):
	return (coffee.name + " " + str(coffee.size[size_id]) + " мл.")

def main():
	"""
		Start the bot
	"""
	fillShop(shop)
	updater = Updater(token=TOKEN)
	dispatcher = updater.dispatcher

	conv_handler = ConversationHandler(
        entry_points=[CommandHandler('menu', menuFunc)],
        states={
            COFFEE:			[CallbackQueryHandler(coffeeType, pass_user_data=True)],
            TIME_REQUEST:	[CallbackQueryHandler(timeRequest, pass_user_data=True)],
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
