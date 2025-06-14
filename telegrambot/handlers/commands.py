from aiogram import Router,types, F
from aiogram.filters import Command, or_f
from telebot.types import CallbackQuery

from keyboars.inline import funny_keyboard




command_router = Router()


@command_router.message(Command('start'))
async def handle_start(m: types.message) -> None:
    start_message= ("ПРИВЕТ! Я ваш личный преподаватель английского языка. Я всегда готов научить вас чему то новому! Нажмите /help, чтобы начать наш урок."
                    )
    await m.answer(text = start_message)

@command_router.message(Command('help'))
async def handle_start(m:types.Message) -> None:
    start_message = (
                     f'🔹/about – информация о боте:\n'
                     f'🥺Обучение🥺:\n'
                     f'Напиши слово (перевод), если нужно будет что то перевести\n'
                     f'📖 /words – новые слова дня\n'
                     f'🔄 /repeat – повторить изученное\n'
                     f'📝 /test – пройти тест на знание слов\n'
                     f'🎯 /topics – выбрать тему (путешествия, бизнес и др.)\n'
    )
    await m.answer(text = start_message)

@command_router.message(Command('about'))
async def handle_start(m:types.Message) -> None:
    start_message = (f'SpeakUp Bot – это умный помощник для изучения английских слов легко и эффективно!\n'
                     f'✨ Что умеет бот?\n' 
                     f'📚 Учит новым словам с примерами и озвучкой\n'
                     f'🔄 Помогает повторять слова по алгоритму интервальных повторений\n'
                     f'📊 Отслеживает ваш прогресс в обучении\n'
                     f'📌 Принципы обучения:\n'
                     f'✔️ Мини-уроки по 5-10 минут в день\n'
                     f'✔️ Игровой формат\n'
                     f'🚀 Наша цель – сделать изучение английской лексики простым и увлекательным!\n'
                     f'Версия 1.0 | По вопросам: @Installer_editor36\n'
                     f'Нажми /help, если нужно будет посмотреть какие есть у меня есть команды\n')
    await m.answer(text=start_message)

@command_router.message(F.sticker)
async def handle_sticker(message: types.Message):
    await message.answer(text = '️😎OMG!! It is so good sticker!️😎')


TRIGGER_WORDS = ["привет", "hi", "hello", "приветствую"]
@command_router.message(lambda message: message.text.lower() in TRIGGER_WORDS)
async def say_hi(message: types.Message):
    await message.answer(text="🤗Hi! How are you? ^,^")

@command_router.message(F.text.lower().contains("bye"))
async def reply_goodbye(message: types.Message):
    await message.answer(text = "🥺See you! Have a nice day, Bro :)")

@command_router.message(F.text.lower().contains('Thanks'))
async def reply_goodbye(message: types.Message):
    await message.answer(text = "🥰U are welcome🥰")

@command_router.message(or_f(Command("menu")), (F.text.lower() == "menu"))
async def reply_goodbye(message: types.Message):
    await message.answer(text="There is menu ---> /")

@command_router.message(Command('words'))
async def handle_start(m: types.message) -> None:
    start_message = ('')
    await m.answer(text=start_message)

@command_router.message(Command('repeat'))
async def handle_start(m: types.message) -> None:
    start_message = ('')
    await m.answer(text=start_message)

@command_router.message(Command('test'))
async def handle_start(m: types.message) -> None:
    start_message = ('')
    await m.answer(text=start_message)

@command_router.message(Command('topics'))
async def handle_start(m: types.message) -> None:
    start_message = ('')
    await m.answer(text=start_message)



@command_router.message(F.text.lower().contains("перевод"))
async def reply_goodbye(message: types.Message):
    await message.answer(text="Translate", reply_markup=funny_keyboard)











