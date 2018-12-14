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

class Coffee:
	def __init__(self, name, sizes, prices):
		self.name = name
		self.size = sizes;
		self.price = prices;

class Shop:
	def __init__(self):
		self.phrases =	{
							'start' 	:	'Привет, ты у Бобра!\nНажми на /menu чтобы заказать кофе или панини!',
							'menu'		:	'Выбери кофе, а потом его размер!',
							'time'		:	'Когда заберешь кофе?\nУкажи час:мин',
							'time_fail'	:	'Ты указал время неправильно, укажи час:мин',
							'order_ok'	:	'Отлично! Заказ принял!',
							'order_ko'	:	'Произошла ошибка',
							'cancel'	:	'Отменяем!\nЖелаешь чего - то?\nНажми на /menu !'
						}
		self.objects = list()
		self.menu = list()

	def addObject(self, name, sizes, prices):
		self.objects.append(Coffee(name, sizes, prices))
		self.menu.append(name)

	def refreshMenu(self):
		self.menu.clear();
		for coffee in self.objects:
			self.menu.append(coffee.name)

	def getMenu(self):
		return (self.menu)

class User:
	def __init__(self, user_id, first, last, username):
		self.first_name = first
		self.last_name = last
		self.user_id = user_id
		self.username = username

	def getInfo(self):
		d = {
			'first_name'	: self.first_name,
			'last_name'		: self.last_name,
			'user_id'		: self.user_id,
			'username'		: self.username
		}
		return (d);