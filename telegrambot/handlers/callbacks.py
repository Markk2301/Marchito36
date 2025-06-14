import aiogram
from aiogram import Router, F, types

callbacks_router = Router()


@callbacks_router.callback_query(F.data == "button_pressed")
async def handle_button(callback: aiogram.types.CallbackQuery):
    await callback.answer("Вы нажали кнопку!")


@callbacks_router.callback_query(F.data == "send_text")
async def send_text(callback: types.CallbackQuery):
    await callback.answer()  # закрывает "часики" на кнопке
    await callback.message.answer("Это обычное текстовое сообщение ")
