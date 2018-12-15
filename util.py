# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    util.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: atlekbai <atlekbai@student.unit.ua>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/12/15 12:15:25 by atlekbai          #+#    #+#              #
#    Updated: 2018/12/15 12:15:26 by atlekbai         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from Shop import *

shop = Shop()

def fillShop(_shop_):
	_shop_.addCategory(0, 'Кофе')
	_shop_.addCategory(1, 'Панини')

	_shop_.addObject('Еспрессо', [110], [13], 0)
	_shop_.addObject('Макиато', [110], [14], 0)
	_shop_.addObject('Допио', [175], [18], 0)
	_shop_.addObject('Американо', [175, 200], [15, 20], 0)
	_shop_.addObject('Капучино', [250, 340, 500], [20, 24, 30], 0)
	_shop_.addObject('Латте', [250, 340, 500], [20, 24, 30], 0)
	_shop_.addObject('Флет Уайт', [200, 340], [24, 26], 0)
	_shop_.addObject('Раф кофе', [250, 340, 500], [25, 29, 35], 0)
	_shop_.addObject('Какао', [250, 340, 500], [20, 25, 30], 0)
	_shop_.addObject('Шоколад', [175, 250], [25, 30], 0)

	_shop_.addObject('с курицей', [1], [30], 1)
	_shop_.addObject('с сыром', [1], [35], 1)

def markupCoffee(coffee):
	"""
		Create ReplyMarkup for choosing coffee details
	"""
	button_list = [];
	for i in range(len(coffee.size)):
		text = str(coffee.size[i]) + " мл.\t" + str(coffee.price[i] )+ " грн."
		button_list.append([InlineKeyboardButton(text, callback_data=i)])
	button_list.append([
		InlineKeyboardButton('Назад', callback_data=100),
		InlineKeyboardButton('Готово', callback_data=101)
		])
	return (button_list)

def markupPanini(shop, id):
	"""
		Create ReplyMarkup for choosing panini
	"""
	menu = shop.menu
	objects = shop.objects
	button_list = [];
	for i in range(len(menu[id])):
		text = menu[id][i] + " " + \
				str(objects[id][i].price[0]) + " грн."
		button_list.append([InlineKeyboardButton(text, callback_data=i)])

	button_list.append([
		InlineKeyboardButton('Назад', callback_data=103),
		InlineKeyboardButton('Готово', callback_data=101)
		])
	return (button_list)

def mainMenu(shop_obj):
	button_list = [];
	for i, obj in enumerate(shop_obj.categories):
		button_list.append([InlineKeyboardButton(obj[i], callback_data=i)])
	button_list.append([
		InlineKeyboardButton('Назад', callback_data=103),
		InlineKeyboardButton('Готово', callback_data=101)
		])
	return (button_list)

def markupMenu(menu, id):
	"""
		Create ReplyMarkup out of menu
	"""
	button_list = [];
	for i, obj in enumerate(menu[id]):
		button_list.append([InlineKeyboardButton(obj, callback_data=i)])
	button_list.append([
		InlineKeyboardButton('Назад', callback_data=103),
		InlineKeyboardButton('Готово', callback_data=101)
		])
	return (button_list)

def toJson(user_data, shop):
	data = dict()
	objects = shop.objects
	data['orders'] = list()
	for order in user_data['order']:
		data['orders'].append({
				'name'	:	objects[order.type_id][order.id].name,
				'size'	:	objects[order.type_id][order.id].size[order.s_id],
				'price'	:	objects[order.type_id][order.id].price[order.s_id]
			})
	data['price'] = user_data['price']
	data['chat_id'] = user_data['chat_id']
	data['name'] = user_data['name']
	data['time'] = user_data['time']
	return (data)

def getOrders(user_data):
	res = "\n(/cancel _для отмены_)\n*Твой заказ:* "
	orders = user_data['order']
	for order in orders:
		if (order.type_id == 0):
			res += "\n∙ " + coffeeFull(shop.objects[order.type_id][order.id], order.s_id)
		elif (order.type_id == 1):
			res += "\n∙ _панини " + shop.objects[order.type_id][order.id].name + "_"
	res += "\n" + getPrice(user_data)
	return (res)

def getInvitation(matchObj):
	text = "\nПриходи в *" + matchObj.group(1) + ":" + matchObj.group(2) + "*"
	return (text)

def getPrice(user_data):
	price = "\n_" + str(user_data['price']) + "_ грн."
	return (price)

def coffeeFull(coffee, size_id):
	return ("_"+ coffee.name + "_ " + str(coffee.size[size_id]) + " мл.")

def sendMessage(bot, update, text, reply_markup=None):
	if (reply_markup):
		reply_markup = InlineKeyboardMarkup(reply_markup)
	bot.send_message(
		chat_id=update.message.chat_id,
		text=text, 
		reply_markup=reply_markup,
		parse_mode=telegram.ParseMode.MARKDOWN)

def editMessage(bot, update, text, reply_markup=None):
	if (reply_markup):
		reply_markup = InlineKeyboardMarkup(reply_markup)
	bot.edit_message_text(
		chat_id=update.message.chat_id,
		message_id=update.message.message_id,
		reply_markup=reply_markup,
		parse_mode=telegram.ParseMode.MARKDOWN,
		text=text)
