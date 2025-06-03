from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

channels = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Фонтанка', callback_data='fontankaspb')],
        [InlineKeyboardButton(text='Первый канал', callback_data='ChannelOne_official')],
        [InlineKeyboardButton(text='Вести', callback_data='vestiru24')]
    ]
)