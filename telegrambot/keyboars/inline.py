from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

funny_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Переводчик №1", url="https://translate.yandex.ru/?source_lang=ru&target_lang=en")],
        #[InlineKeyboardButton(text="Классный стикер", sticker="")]
        [InlineKeyboardButton(text="Переводчик №2", url="https://translate.yandex.ru/?source_lang=ru&target_lang=en")]
    ]
)



