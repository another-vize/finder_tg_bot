from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

unit = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Начать поиск'), KeyboardButton(text='Инструкция')]
    ],
    resize_keyboard=True
)
