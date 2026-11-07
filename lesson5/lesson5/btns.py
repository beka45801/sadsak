from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


start_kb = ReplyKeyboardMarkup(
	keyboard=[[KeyboardButton(text='Старт')]],
	resize_keyboard=True,
)

menu_kb = ReplyKeyboardMarkup(
	keyboard=[
		[KeyboardButton(text='Зарегистрироваться')],
		[KeyboardButton(text='Новости узб')],
	],
	resize_keyboard=True,
)

registered_kb = ReplyKeyboardMarkup(
	keyboard=[[KeyboardButton(text='Новости узб')]],
	resize_keyboard=True,
)
