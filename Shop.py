# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Shop.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: atlekbai <atlekbai@student.unit.ua>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/12/14 14:38:39 by atlekbai          #+#    #+#              #
#    Updated: 2018/12/14 14:38:39 by atlekbai         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import json

class Good:
	def __init__(self, name, sizes, prices, type_id):
		self.name = name
		self.size = sizes;
		self.price = prices;
		self.type_id = type_id

class Shop:
	def __init__(self):
		self.phrases =	{
							'start' 	:	'Привет, ты у Бобра!\nНажми на /menu чтобы заказать кофе или панини!',
							'main_menu'	:	'Кофе или панини?',
							'menu_cof'	:	'Выбери кофе, а потом его размер!',
							'menu_pan'	:	'Выбери панини!',
							'time'		:	'\n\nКогда заберешь заказ?\nОтправь *час*:*мин*\n(_Пример: 16:05_)',
							'time_fail'	:	'Ты указал время неправильно, укажи час:мин',
							'order_ok'	:	'Заказ принял!',
							'order_ko'	:	'Произошла ошибка',
							'cancel'	:	'Отменяем!\nЖелаешь чего - то?\nНажми на /menu !',
							'empty'		:	'Ты ничего не заказал 🙃\n/menu чтобы заказать'
						}
		self.categories = list()
		self.objects = dict()
		self.menu = dict()

	def addObject(self, name, sizes, prices, type_id):
		self.objects[type_id].append(Good(name, sizes, prices, type_id))
		self.menu[type_id].append(name)

	def addCategory(self, type_id, name):
		self.categories.append({
			type_id	:	name
			})
		self.menu[type_id] = list()
		self.objects[type_id] = list()

class Order:
	def __init__(self, name_id, size_id, type_id):
		self.id = name_id
		self.s_id = size_id
		self.type_id = type_id