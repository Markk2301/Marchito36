import json

from aiogram.types import ReplyKeyboardRemove
from keyboars.inline import funny_keyboard
from aiogram import Router, types, F
from aiogram.filters import Command, or_f
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import logging

from keyboars.reply import reply_keyboard

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


user_vocabulary = {}
user_last_random_word_message = {}
user_added_words = {}
user_progress = {}
used_words = {}
user_tests = {}

english_words = {"aisle": "проход", "bargain": "выгодная покупка",
    "complimentary": "бесплатный (предоставляемый)", "delivery": "доставка",
    "expiry": "срок годности", "fragile": "хрупкий",
    "gadget": "гаджет", "handy": "удобный",
    "inventory": "ассортимент", "junk": "хлам",
    "knickknack": "безделушка", "landmark": "ориентир",
    "malfunction": "неисправность", "novelty": "новинка",
    "outlet": "розетка/аутлет", "package": "пакет/посылка",
    "quirky": "необычный", "receipt": "чек",
    "souvenir": "сувенир", "tag": "ценник/бирка",
    "upgrade": "улучшение", "voucher": "талон",
    "warranty": "гарантия", "yield": "уступать дорогу",
    "aisle seat": "место у прохода", "bellhop": "носильщик",
    "concierge": "консьерж", "doorman": "швейцар",
    "etiquette": "этикет", "fare": "плата за проезд",
    "gratuity": "чаевые", "hostel": "хостел",
    "itinerary": "маршрут", "jetlag": "джетлаг",
    "keycard": "ключ-карта", "lodging": "жилье",
    "motel": "мотель", "no-show": "неявка",
    "overnight": "ночевка", "pit stop": "остановка в пути",
    "queue": "очередь", "reservation": "бронирование",
    "stopover": "транзит", "transit": "пересадка",
    "utilities": "коммунальные услуги", "vacancy": "свободные места",
    "walk-in": "без записи", "exchange rate": "курс обмена",
    "zip code": "почтовый индекс", "rush hour": "час пик",
    "awkward": "неловкий", "banter": "дружеский подтрунивание",
    "chitchat": "светская беседа", "dense": "недогадливый",
    "egotistical": "самовлюбленный", "flaky": "ненадежный",
    "gossip": "сплетни", "humblebrag": "скромное хвастовство",
    "icebreaker": "способ разрядить обстановку", "jabber": "болтовня",
    "kudos": "похвала", "lousy": "отвратительный",
    "moody": "переменчивый", "nosy": "любопытный",
    "offbeat": "нестандартный", "petty": "мелочный",
    "quirky": "с причудами", "rant": "гневная тирада",
    "sassy": "дерзкий", "tactless": "бестактный",
    "uptight": "напряженный", "vibe": "атмосфера",
    "whiny": "нытик", "small talk": "светская беседа",
    "backhanded compliment": "комплимент с подтекстом", "blunt": "прямолинейный",
    "cheesy": "банальный", "dorky": "чудаковатый",
    "facepalm": "жест разочарования", "geeky": "увлекающийся технологиями",
    "hang out": "тусоваться", "jumpy": "нервный",
    "kinky": "эксцентричный", "laid-back": "расслабленный",
    "mellow": "спокойный", "nerdy": "ботанистый",
    "obnoxious": "неприятный", "pushy": "настойчивый",
    "quirky": "своеобразный", "rowdy": "шумный",
    "snarky": "язвительный", "thrifty": "бережливый",
    "unplug": "отключаться (от техники)", "vegan": "веган",
    "woke": "просвещенный", "xenial": "гостеприимный",
    "yappy": "болтливый", "zing": "колкость",
    "airdrop": "передача файлов", "binge-watch": "смотреть подряд",
    "clickbait": "замануха", "deepfake": "фейковое видео",
    "emoji": "эмодзи", "fomo": "страх упустить возможность",
    "glitch": "сбой", "hashtag": "хэштег",
    "influencer": "инфлюенсер", "junk mail": "спам",
    "kiosk": "киоск", "livestream": "прямая трансляция",
    "meme": "мем", "notifications": "уведомления",
    "on-brand": "соответствующий стилю", "podcast": "подкаст",
    "QR code": "QR-код", "reboot": "перезагрузка",
    "spoiler": "спойлер", "troll": "тролль",
    "unfriend": "удалить из друзей", "viral": "вирусный",
    "wi-fi": "вай-фай", "app": "приложение",
    "blog": "блог", "crowdfund": "краудфандинг",
    "download": "скачивать", "ebook": "электронная книга",
    "firewall": "брандмауэр", "gigabyte": "гигабайт",
    "homepage": "главная страница", "inbox": "входящие",
    "jpeg": "jpeg", "keyboard": "клавиатура",
    "lag": "задержка", "malware": "вредоносное ПО",
    "netizen": "пользователь интернета", "offline": "вне сети",
    "phishing": "фишинг", "reboot": "перезагрузка",
    "spam": "спам", "tablet": "планшет",
    "username": "имя пользователя", "vlog": "видеоблог",
    "webinar": "вебинар", "zoom": "зум (увеличивать)",
    "boarding pass": "посадочный талон",
    "carry-on": "ручная кладь",
    "connecting flight": "стыковочный рейс",
    "departure gate": "выход на посадку",
    "duty-free": "дьюти-фри",
    "emergency exit": "аварийный выход",
    "fast track": "ускоренный проход",
    "ground transportation": "наземный транспорт",
    "hotel shuttle": "гостиничный шаттл",
    "immigration": "иммиграционный контроль",
    "jet bridge": "телескопический трап",
    "layover": "пересадка",
    "lost and found": "бюро находок",
    "overhead bin": "багажная полка",
    "passport control": "паспортный контроль",
    "red-eye flight": "ночной рейс",
    "seat assignment": "распределение мест",
    "ticket counter": "стойка регистрации",
    "travel adapter": "переходник для розеток",
    "trolley": "тележка",
    "turntable": "багажная карусель",
    "visa waiver": "безвизовый въезд",
    "window seat": "место у окна",
    "boarding time": "время посадки",
    "check-in desk": "стойка регистрации",
    "delayed flight": "задержанный рейс",
    "exit row": "ряд у аварийного выхода",
    "flight attendant": "бортпроводник",
    "luggage allowance": "норма багажа",
    "priority boarding": "приоритетная посадка",
    "appetizer": "закуска",
    "buffet": "шведский стол",
    "chef's special": "фирменное блюдо",
    "doggie bag": "еда с собой из ресторана",
    "entrée": "основное блюдо",
    "fixed menu": "фиксированное меню",
    "gluten-free": "без глютена",
    "happy hour": "счастливый час",
    "ingredients": "ингредиенты",
    "junk food": "фастфуд",
    "kosher": "кошерный",
    "lactose-free": "без лактозы",
    "mocktail": "безалкогольный коктейль",
    "nutritious": "питательный",
    "organic": "органический",
    "portion size": "размер порции",
    "quiche": "киш",
    "reservation": "бронирование",
    "side dish": "гарнир",
    "tap water": "вода из-под крана",
    "utensils": "столовые приборы",
    "vegan option": "веганская опция",
    "waitlist": "лист ожидания",
    "à la carte": "à la carte (по меню)",
    "brunch": "поздний завтрак",
    "condiments": "приправы",
    "dietary restrictions": "пищевые ограничения",
    "food poisoning": "пищевое отравление",
    "gourmet": "гурман",
    "homemade": "домашнего приготовления",
    "barcode": "штрих-код",
    "clearance sale": "распродажа",
    "discount code": "код скидки",
    "exchange policy": "политика обмена",
    "final sale": "без возврата",
    "gift receipt": "подарочный чек",
    "in stock": "в наличии",
    "jewelry counter": "отдел бижутерии",
    "keep the change": "сдачи не надо",
    "loyalty card": "дисконтная карта",
    "mail-in rebate": "возврат по почте",
    "non-refundable": "невозвратный",
    "out of stock": "нет в наличии",
    "price match": "сопоставление цен",
    "quality guarantee": "гарантия качества",
    "return policy": "политика возврата",
    "shopping spree": "шопинг-марафон",
    "try on": "примерять",
    "unworn": "не ношенный",
    "value pack": "выгодная упаковка",
    "warranty card": "гарантийный талон",
    "exchange desk": "стойка обмена",
    "fitting room": "примерочная",
    "gift wrapping": "подарочная упаковка",
    "impulse buy": "спонтанная покупка",
    "last season": "прошлый сезон",
    "must-have": "необходимая вещь",
    "on clearance": "на распродаже",
    "price tag": "ценник",
    "shopping cart": "тележка для покупок",
    "autocorrect": "автозамена",
    "browser": "браузер",
    "cache": "кэш",
    "data plan": "тарифный план",
    "emoji keyboard": "клавиатура с эмодзи",
    "firewall": "брандмауэр",
    "google it": "погугли",
    "hack": "взлом",
    "in-app purchase": "внутриигровая покупка",
    "jailbreak": "взлом устройства",
    "keychain": "связка ключей (паролей)",
    "laggy": "тормозящий",
    "mute": "отключить звук",
    "notifications": "уведомления",
    "offline mode": "автономный режим",
    "pop-up": "всплывающее окно",
    "QR scanner": "QR-сканер",
    "refresh": "обновить",
    "screenshot": "скриншот",
    "touchscreen": "сенсорный экран",
    "unsubscribe": "отписаться",
    "viral content": "вирусный контент",
    "wireless charger": "беспроводная зарядка",
    "airplane mode": "авиарежим",
    "bug fix": "исправление ошибки",
    "cloud storage": "облачное хранилище",
    "dark mode": "темный режим",
    "e-receipt": "электронный чек",
    "facial recognition": "распознавание лица",
    "geotag": "геотег",
    "blackout": "отключение электричества",
    "carpool": "совместная поездка",
    "deadline": "крайний срок",
    "emergency contact": "контакт для экстренных случаев",
    "flat tire": "спущенное колесо",
    "gas station": "заправка",
    "handyman": "мастер на все руки",
    "insurance claim": "страховое требование",
    "jump start": "прикурить автомобиль",
    "keysmith": "мастер по ключам",
    "leak": "протечка",
    "maintenance": "техобслуживание",
    "no parking zone": "место где парковка запрещена",
    "on hold": "на удержании",
    "paperwork": "документы",
    "quick fix": "временное решение",
    "roadside assistance": "помощь на дороге",
    "service charge": "плата за обслуживание",
    "traffic jam": "пробка",
    "utilities": "коммунальные услуги",
    "vandalism": "вандализм",
    "water damage": "повреждение от воды",
    "xerox copy": "ксерокопия",
    "yard sale": "распродажа во дворе",
    "zip tie": "пластиковая стяжка",
    "after hours": "в нерабочее время",
    "break-in": "взлом",
    "customer service": "обслуживание клиентов",
    "dress code": "дресс-код",
    "electrician": "электрик"

}


command_router = Router()


def get_word_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Добавить", callback_data="add_word"),
         InlineKeyboardButton(text="⏭ Пропустить", callback_data="skip_word")],
        [InlineKeyboardButton(text="📚 Мои слова", callback_data="my_words"),
         InlineKeyboardButton(text="📝 Тест", callback_data="start_test")]
    ])


async def get_random_word(user_id: int):
    if user_id not in used_words:
        used_words[user_id] = set()

    if user_id not in user_progress:
        user_progress[user_id] = {"added": 0, "skipped": 0}

    if user_id not in user_added_words:
        user_added_words[user_id] = {}

    available_words = {k: v for k, v in english_words.items()
                       if k not in used_words[user_id]}

    if not available_words:
        used_words[user_id] = set()
        available_words = english_words.copy()

    word, translation = random.choice(list(available_words.items()))
    used_words[user_id].add(word)
    return word, translation


@command_router.message(Command('words'))
async def send_random_word(message: types.Message):
    user_id = message.chat.id
    word, translation = await get_random_word(user_id)
    user_vocabulary[user_id] = (word, translation)

    # Delete previous message
    # if user_id in user_last_random_word_message:
    #     last_message_id = user_last_random_word_message[user_id]
    #     await message.chat.delete_message(last_message_id)
    # user_last_random_word_message[user_id] = message.message_id

    await message.answer(
        text=f"🎲 Случайное слово:\n\n🔤 {word}\n🇷🇺 {translation}",
        reply_markup=get_word_keyboard()
    )


@command_router.callback_query(F.data == "add_word")
async def handle_add_word(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id in user_vocabulary:
        word, translation = user_vocabulary[user_id]
        user_added_words[user_id][word] = translation
        user_progress[user_id]["added"] += 1

        await callback.answer("✅ Слово добавлено в ваш словарь!")
        await send_random_word(callback.message)
    else:
        await callback.answer("⚠️ Не удалось добавить слово. Попробуйте снова.")


@command_router.callback_query(F.data == "skip_word")
async def handle_skip_word(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id in user_progress:
        user_progress[user_id]["skipped"] += 1

    await callback.answer("⏭ Слово пропущено")
    await send_random_word(callback.message)


@command_router.callback_query(F.data == "my_words")
async def handle_my_words(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id in user_added_words and user_added_words[user_id]:
        words_list = "\n".join([f"🔤 {word} - 🇷🇺 {trans}"
                                for word, trans in user_added_words[user_id].items()])

        progress = user_progress.get(user_id, {"added": 0, "skipped": 0})
        stats = f"\n\n📊 Ваш прогресс:\n✅ Добавлено: {progress['added']}\n⏭ Пропущено: {progress['skipped']}"

        await callback.message.answer(
            text=f"📚 Ваши добавленные слова:\n\n{words_list}{stats}",
            reply_markup=get_word_keyboard()
        )
    else:
        await callback.message.answer(
            text="📚 У вас пока нет добавленных слов. Нажмите '✅ Добавить', чтобы сохранить слова.",
            reply_markup=get_word_keyboard()
        )

    await callback.answer()


@command_router.message(Command('mywords'))
async def handle_mywords_command(message: types.Message):
    user_id = message.from_user.id

    if user_id in user_added_words and user_added_words[user_id]:
        words_list = "\n".join([f"🔤 {word} - 🇷🇺 {trans}"
                                for word, trans in user_added_words[user_id].items()])

        progress = user_progress.get(user_id, {"added": 0, "skipped": 0})
        stats = f"\n\n📊 Ваш прогресс:\n✅ Добавлено: {progress['added']}\n⏭ Пропущено: {progress['skipped']}"

        await message.answer(
            text=f"📚 Ваши добавленные слова:\n\n{words_list}{stats}"
        )
    else:
        await message.answer(
            text="📚 У вас пока нет добавленных слов. Используйте команду /words, чтобы начать учить новые слова."
        )

@command_router.message(Command('help'))
async def handle_help(message: types.Message):
    help_message = (
        "🔹/about – информация о боте:\n"
        '\n'
        "🥺Обучение🥺:\n"
        '\n'
        "Напиши слово ( перевод ), если нужно будет что-то перевести.\n"
        '\n'
        "📖 /words – новые слова дня.\n"
        '\n'
        "📚 /mywords – просмотр добавленных слов в вашем личном словарике.\n" 
        '\n'
        "📝 /test – пройти тест на знание слов.\n"
        '\n'
        "🎯 /topics – выбрать тему (путешествия, бизнес и др.)\n"
    )
    await message.answer(text=help_message)

@command_router.message(Command('start'))
async def handle_start(message: types.Message):
    start_message = ("ПРИВЕТ! Я ваш личный преподаватель английского языка. "
                     "Я всегда готов научить вас чему-то новому абсолютно БЕСПЛАТНО! Нажмите /help, чтобы перейти в панель управления командами или "
                     "нажмите /about, чтобы узнать больше информации о боте.")
    await message.answer(text=start_message)

@command_router.message(Command('about'))
async def handle_about(message: types.Message):
    about_message = (
        "SpeakUp Bot – это умный помощник для изучения английских слов легко и эффективно!\n"
         '\n'
        "✨ Что умеет бот?\n"
        '\n'
        "1.📚 Учит новым словам с примерами и озвучкой\n"
        "2.🔄 Помогает повторять слова по алгоритму интервальных повторений\n"
        "3.📊 Отслеживает ваш прогресс в обучении\n"
         '\n'
        "📌 Принципы обучения:\n"
         '\n'
        "1.✔️ Мини-уроки по 5-10 минут в день\n"
        "2.✔️ Игровой формат\n"
         '\n'
        "❤️ Наша цель – сделать изучение английской лексики простым и увлекательным!❤️\n"
         '\n'
        "Версия 1.0 | Если ошибка или есть нужно что то добавить, писать @Installer_editor36\n"
         '\n'
        "Нажми /help, если нужно будет посмотреть какие есть у меня команды"
    )
    await message.answer(text=about_message)

@command_router.message(F.sticker)
async def handle_sticker(message: types.Message):
    await message.answer(text='😎 OMG!! It is so good sticker! 😎')

TRIGGER_WORDS = ["привет", "hi", "hello", "приветствую"]

@command_router.message(lambda message: message.text.lower() in TRIGGER_WORDS)
async def say_hi(message: types.Message):
    await message.answer(text="🤗 Hi! How are you? ^,^")

g = ['пока',"bye", "goodbye"]
@command_router.message(lambda message: message.text.lower() in g)
async def reply_goodbye(message: types.Message):
    await message.answer(text="🥺 See you! Have a nice day, Bro :)")

@command_router.message(F.text.lower().contains('thank you'))
async def reply_thanks(message: types.Message):
    await message.answer(text="🥰 You are welcome! 🥰")

@command_router.message(or_f(Command("menu"), (F.text.lower() == "menu")))
async def show_menu(message: types.Message):
    await message.answer(text="Главное меню:\n/words - Новые слова \n/help - Все команды")

@command_router.message(Command('topics'))
async def handle_topics(message: types.Message):
    await message.answer(text="Функция выбора тем в разработке!")

@command_router.message(F.text.lower().contains("перевод"))
async def reply_goodbye(message: types.Message):
    await message.answer(text="Translate", reply_markup=funny_keyboard)

@command_router.message(Command('english'))
async def send_photo(message:types.Message):
    await message.answer_photo(
    photo = 'https://i.postimg.cc/X7CT7Gbj/Lucid-Realism-Create-an-illustration-featuring-the-Union-Jack-1.jpg',
    caption = '❤️Учим английский вместе❤️!',
    )


def get_test_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Пройти тест еще раз", callback_data="more_test")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_menu")]
    ])


async def generate_test(user_id: int):
    """Генерирует тест только из добавленных пользователем слов"""
    if user_id not in user_added_words or len(user_added_words[user_id]) < 4:
        return None, None, None

    # Выбираем случайное слово из добавленных пользователем
    test_word, correct_answer = random.choice(list(user_added_words[user_id].items()))

    # Собираем 3 случайных неправильных ответа из ТОЛЬКО добавленных слов
    wrong_answers = []
    all_added_words = list(user_added_words[user_id].values())

    while len(wrong_answers) < 3:
        word = random.choice(all_added_words)
        if word != correct_answer and word not in wrong_answers:
            wrong_answers.append(word)

    # Смешиваем ответы
    all_answers = [correct_answer] + wrong_answers
    random.shuffle(all_answers)

    # Сохраняем данные теста
    user_tests[user_id] = {
        "word": test_word,
        "correct": correct_answer,
        "answers": all_answers
    }

    return test_word, all_answers, all_answers.index(correct_answer)


@command_router.callback_query(F.data == "start_test")
async def handle_start_test(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    # Проверяем, что у пользователя достаточно слов для теста
    if user_id not in user_added_words or len(user_added_words[user_id]) < 4:
        await callback.answer(
            "📝 Для прохождения теста нужно добавить как минимум 4 слова!",
            show_alert=True
        )
        return

    test_word, answers, _ = await generate_test(user_id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=answers[0], callback_data="test_answer_0")],
        [InlineKeyboardButton(text=answers[1], callback_data="test_answer_1")],
        [InlineKeyboardButton(text=answers[2], callback_data="test_answer_2")],
        [InlineKeyboardButton(text=answers[3], callback_data="test_answer_3")],
    ])

    await callback.message.edit_text(
        text=f"📝 Тест: Как переводится слово '{test_word}'?",
        reply_markup=keyboard
    )
    await callback.answer()


@command_router.message(Command('test'))
async def handle_test(message: types.Message):
    user_id = message.from_user.id

    # Проверяем, что у пользователя достаточно слов для теста
    if user_id not in user_added_words or len(user_added_words[user_id]) < 4:
        await message.answer(
            "📝 Для прохождения теста нужно добавить как минимум 4 слова.\n"
            "Используйте /words, чтобы добавить новые слова!"
        )
        return

    test_word, answers, _ = await generate_test(user_id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=answers[0], callback_data="test_answer_0")],
        [InlineKeyboardButton(text=answers[1], callback_data="test_answer_1")],
        [InlineKeyboardButton(text=answers[2], callback_data="test_answer_2")],
        [InlineKeyboardButton(text=answers[3], callback_data="test_answer_3")],
    ])

    await message.answer(
        text=f"📝 Тест: Как переводится слово '{test_word}'?",
        reply_markup=keyboard
    )


@command_router.callback_query(F.data.startswith("test_answer_"))
async def handle_test_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    answer_index = int(callback.data.split("_")[-1])

    if user_id not in user_tests:
        await callback.answer("❌ Тест устарел или не найден. Начните новый.")
        return

    test_data = user_tests[user_id]

    if test_data["answers"][answer_index] == test_data["correct"]:
        response = "✅ Правильно! Отличная работа!"
        if "correct" not in user_progress[user_id]:
            user_progress[user_id]["correct"] = 0
        user_progress[user_id]["correct"] += 1
    else:
        response = f"❌ Неправильно. Правильный ответ: '{test_data['correct']}'"
        if "wrong" not in user_progress[user_id]:
            user_progress[user_id]["wrong"] = 0
        user_progress[user_id]["wrong"] += 1

    await callback.message.edit_text(
        text=f"{response}\n\nСлово: {test_data['word']}\nПеревод: {test_data['correct']}",
        reply_markup=get_test_keyboard()
    )
    await callback.answer()


@command_router.callback_query(F.data == "more_test")
async def handle_more_test(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in user_added_words or len(user_added_words[user_id]) < 4:
        await callback.answer("❌ Недостаточно слов для теста. Добавьте больше слов!")
        return

    test_word, answers, _ = await generate_test(user_id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=answers[0], callback_data="test_answer_0")],
        [InlineKeyboardButton(text=answers[1], callback_data="test_answer_1")],
        [InlineKeyboardButton(text=answers[2], callback_data="test_answer_2")],
        [InlineKeyboardButton(text=answers[3], callback_data="test_answer_3")],
    ])

    await callback.message.edit_text(
        text=f"📝 Тест: Как переводится слово '{test_word}'?",
        reply_markup=keyboard
    )
    await callback.answer()


@command_router.callback_query(F.data == "to_menu")
async def handle_to_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="🏠 Вы вернулись в главное меню",
        reply_markup=get_word_keyboard()
    )
    await callback.answer()





# @command_router.message(Command("menu1"))
# async def handle_goyda(m: types.message) -> None:
#     menu_messange = ("bh")
#     await m.answer(text=menu_messange, reply_markup=reply_keyboard)

# @command_router.message(Command("menu1"))
# async def handle_menu(m: types.Message) -> None:
#     menu_message = "Выберите действие:"
#     await m.answer(text=menu_message, reply_markup=reply_keyboard)
#
# # Обработчики для кнопок
# @command_router.message(F.text == "Функция 1")
# async def handle_func1(m: types.Message):
#     await m.answer("Выполняется функция 1", reply_markup=types.ReplyKeyboardRemove())






