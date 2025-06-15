from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Профиль")],
        [KeyboardButton(text="Настройки")]
    ],
    resize_keyboard=True
)