import sqlite3
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Определяем клавиатуру для перевода
funny_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔤 Английский", callback_data="english_translate"),
     InlineKeyboardButton(text="🇷🇺 Русский", callback_data="russian_translate")]
])


# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('vocabulary.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        english TEXT UNIQUE,
        russian TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        word_id INTEGER,
        FOREIGN KEY(word_id) REFERENCES words(id),
        UNIQUE(user_id, word_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_progress (
        user_id INTEGER PRIMARY KEY,
        added INTEGER DEFAULT 0,
        skipped INTEGER DEFAULT 0,
        correct INTEGER DEFAULT 0,
        wrong INTEGER DEFAULT 0
    )
    ''')

    english_words = {
        "actually": "на самом деле",
        "annoying": "раздражающий",
        "awkward": "неловкий",
        "bother": "беспокоить",
        "common": "распространённый",
        "concern": "беспокойство",
        "confused": "растерянный",
        "convenient": "удобный",
        "crowded": "переполненный",
        "delicious": "вкусный",
        "disappointed": "разочарованный",
        "embarrassed": "смущённый",
        "emergency": "чрезвычайная ситуация",
        "entire": "целый",
        "especially": "особенно",
        "expect": "ожидать",
        "familiar": "знакомый",
        "frustrated": "раздражённый",
        "guilty": "виноватый",
        "huge": "огромный",
        "ignore": "игнорировать",
        "immediately": "немедленно",
        "impressive": "впечатляющий",
        "incredible": "невероятный",
        "informal": "неформальный",
        "instead": "вместо",
        "intend": "намереваться",
        "issue": "проблема",
        "jealous": "ревнивый",
        "likely": "вероятно",
        "mention": "упоминать",
        "messy": "грязный/неаккуратный",
        "necessary": "необходимый",
        "nervous": "нервный",
        "obvious": "очевидный",
        "ordinary": "обычный",
        "particular": "конкретный",
        "patient": "терпеливый",
        "perhaps": "возможно",
        "polite": "вежливый",
        "popular": "популярный",
        "possible": "возможный",
        "prepare": "готовить(ся)",
        "probably": "наверное",
        "promise": "обещание",
        "proud": "гордый",
        "punctual": "пунктуальный",
        "purpose": "цель",
        "recently": "недавно",
        "refuse": "отказываться",
        "regret": "сожалеть",
        "relaxed": "расслабленный",
        "remind": "напоминать",
        "responsible": "ответственный",
        "rude": "грубый",
        "satisfied": "удовлетворённый",
        "serious": "серьёзный",
        "several": "несколько",
        "slightly": "слегка",
        "social": "социальный",
        "suddenly": "вдруг",
        "suitable": "подходящий",
        "support": "поддерживать",
        "surprised": "удивлённый",
        "terrible": "ужасный",
        "tired": "уставший",
        "typical": "типичный",
        "uncomfortable": "неудобный",
        "unusual": "необычный",
        "useful": "полезный",
        "valuable": "ценный",
        "various": "различный",
        "waste": "тратить впустую",
        "whole": "весь",
        "worried": "обеспокоенный",
        "worth": "стоящий",
        "anxious": "тревожный",
        "brave": "храбрый",
        "calm": "спокойный",
        "clever": "умный",
        "doubt": "сомнение",
        "eager": "нетерпеливый",
        "faith": "вера",
        "generous": "щедрый",
        "honest": "честный",
        "humble": "скромный",
        "ideal": "идеальный",
        "kind": "добрый",
        "loyal": "верный",
        "mature": "зрелый",
        "modest": "скромный",
        "optimistic": "оптимистичный",
        "passionate": "страстный",
        "reliable": "надёжный",
        "sincere": "искренний",
        "thoughtful": "внимательный",
        "wise": "мудрый",
        "agree": "соглашаться",
        "apologize": "извиняться",
        "argue": "спорить",
        "arrive": "прибывать",
        "believe": "верить",
        "borrow": "брать взаймы",
        "celebrate": "праздновать",
        "complain": "жаловаться",
        "discuss": "обсуждать",
        "explain": "объяснять",
        "forgive": "прощать",
        "improve": "улучшать",
        "invite": "приглашать",
        "laugh": "смеяться",
        "manage": "управлять",
        "nod": "кивать",
        "offer": "предлагать",
        "pretend": "притворяться",
        "react": "реагировать",
        "smile": "улыбаться",
        "trust": "доверять",
        "wonder": "интересоваться",
        "yell": "кричать",

        "achieve": "достигать",
        "admire": "восхищаться",
        "advise": "советовать",
        "affect": "влиять",
        "allow": "разрешать",
        "amaze": "поражать",
        "amuse": "развлекать",
        "analyze": "анализировать",
        "announce": "объявлять",
        "appear": "появляться",
        "appreciate": "ценить",
        "approve": "одобрять",
        "arrange": "организовывать",
        "attack": "атаковать",
        "attempt": "пытаться",
        "avoid": "избегать",
        "bake": "печь",
        "bathe": "купаться",
        "beg": "умолять",
        "behave": "вести себя",
        "blame": "винить",
        "breathe": "дышать",
        "bury": "хоронить",
        "calculate": "вычислять",
        "challenge": "вызов",
        "cheer": "подбадривать",
        "chew": "жевать",
        "climb": "взбираться",
        "collect": "собирать",
        "compare": "сравнивать",
        "compete": "соревноваться",
        "complain": "жаловаться",
        "complete": "завершать",
        "concentrate": "концентрироваться",
        "confess": "признаваться",
        "connect": "соединять",
        "consider": "рассматривать",
        "contain": "содержать",
        "continue": "продолжать",
        "control": "контролировать",
        "correct": "исправлять",
        "create": "создавать",
        "criticize": "критиковать",
        "dance": "танцевать",
        "decide": "решать",
        "decorate": "украшать",
        "delay": "задерживать",
        "deliver": "доставлять",
        "demand": "требовать",
        "depend": "зависеть",
        "describe": "описывать",
        "deserve": "заслуживать",
        "destroy": "уничтожать",
        "develop": "развивать",
        "disagree": "не соглашаться",
        "discover": "открывать",
        "divide": "делить",
        "doubt": "сомневаться",
        "earn": "зарабатывать",
        "educate": "обучать",
        "encourage": "поощрять",
        "enjoy": "наслаждаться",
        "escape": "сбегать",
        "examine": "исследовать",
        "exchange": "обменивать",
        "exist": "существовать",
        "expand": "расширять",
        "expect": "ожидать",
        "experience": "опыт",
        "express": "выражать",
        "fail": "терпеть неудачу",
        "fear": "бояться",
        "feed": "кормить",
        "feel": "чувствовать",
        "fight": "бороться",
        "fill": "заполнять",
        "find": "находить",
        "fix": "чинить",
        "follow": "следовать",
        "force": "заставлять",
        "forget": "забывать",
        "freeze": "замораживать",
        "frighten": "пугать",
        "gather": "собирать",
        "glow": "светиться",
        "greet": "приветствовать",
        "grow": "расти",
        "guess": "угадывать",
        "guide": "вести",
        "hang": "вешать",
        "happen": "случаться",
        "harm": "вредить",
        "hate": "ненавидеть",
        "heal": "лечить",
        "hear": "слышать",
        "heat": "нагревать",
        "help": "помогать",
        "hide": "прятать",
        "hit": "ударять",
        "hope": "надеяться",
        "hunt": "охотиться",
        "imagine": "представлять",
        "increase": "увеличивать",
        "influence": "влиять",
        "inform": "сообщать",
        "injure": "ранить",
        "insist": "настаивать",
        "introduce": "представлять (кого-то)",
        "invent": "изобретать",
        "join": "присоединяться",
        "jump": "прыгать",
        "keep": "хранить",
        "kick": "пинать",
        "kill": "убивать",
        "knock": "стучать",
        "know": "знать",
        "lack": "недоставать",
        "last": "длиться",
        "lead": "вести",
        "learn": "учить",
        "leave": "оставлять",
        "lend": "одалживать",
        "lie": "лгать",
        "lift": "поднимать",
        "light": "освещать",
        "listen": "слушать",
        "live": "жить",
        "look": "смотреть",
        "lose": "терять",
        "love": "любить",
        "maintain": "поддерживать",
        "make": "делать",
        "matter": "иметь значение",
        "mean": "значить",
        "measure": "измерять",
        "meet": "встречать",
        "melt": "таять",
        "move": "двигаться",
        "need": "нуждаться",
        "notice": "замечать",
        "obey": "подчиняться",
        "observe": "наблюдать",
        "obtain": "получать",
        "occupy": "занимать",
        "occur": "происходить",
        "open": "открывать",
        "order": "заказывать",
        "organize": "организовывать",
        "owe": "быть должным",
        "own": "владеть",
        "pack": "упаковывать",
        "paint": "красить",
        "pass": "проходить",
        "pay": "платить",
        "perform": "выполнять",
        "pick": "выбирать",
        "place": "помещать",
        "plan": "планировать",
        "play": "играть",
        "please": "радовать",
        "point": "указывать",
        "possess": "обладать",
        "practice": "практиковаться",
        "praise": "хвалить",
        "prefer": "предпочитать",
        "press": "нажимать",
        "prevent": "предотвращать",
        "produce": "производить",
        "protect": "защищать",
        "prove": "доказывать",
        "provide": "обеспечивать",
        "pull": "тянуть",
        "punish": "наказывать",
        "push": "толкать",
        "put": "класть",
        "question": "спрашивать",
        "raise": "поднимать",
        "reach": "достигать",
        "read": "читать",
        "realize": "осознавать",
        "receive": "получать",
        "recognize": "узнавать",
        "record": "записывать",
        "reduce": "уменьшать",
        "refer": "ссылаться",
        "reflect": "отражать",
        "refuse": "отказываться",
        "regret": "сожалеть",
        "reject": "отвергать",
        "relax": "расслабляться",
        "remember": "помнить",
        "remove": "удалять",
        "repair": "чинить",
        "repeat": "повторять",
        "replace": "заменять",
        "reply": "отвечать",
        "report": "сообщать",
        "represent": "представлять",
        "require": "требовать",
        "rescue": "спасать",
        "research": "исследовать",
        "respect": "уважать",
        "rest": "отдыхать",
        "result": "результат",
        "return": "возвращать",
        "reveal": "раскрывать",
        "review": "просматривать",
        "reward": "награждать",
        "ride": "ехать верхом",
        "ring": "звонить",
        "rise": "подниматься",
        "risk": "рисковать",
        "roll": "катиться",
        "rub": "тереть",
        "rule": "править",
        "run": "бежать",
        "rush": "торопиться",
        "save": "спасать",
        "say": "говорить",
        "search": "искать",
        "see": "видеть",
        "seem": "казаться",
        "sell": "продавать",
        "send": "отправлять",
        "serve": "служить",
        "set": "устанавливать",
        "settle": "улаживать",
        "shake": "трясти",
        "share": "делиться",
        "shout": "кричать",
        "show": "показывать",
        "shut": "закрывать",
        "sing": "петь",
        "sit": "сидеть",
        "sleep": "спать",
        "smell": "пахнуть",
        "solve": "решать",
        "speak": "говорить",
        "spend": "тратить",
        "stand": "стоять",
        "start": "начинать",
        "stay": "оставаться",
        "steal": "воровать",
        "stick": "приклеивать",
        "stop": "останавливать",
        "study": "учиться",
        "succeed": "преуспевать",
        "suffer": "страдать",
        "suggest": "предлагать",
        "supply": "поставлять",
        "suppose": "предполагать",
        "surround": "окружать",
        "survive": "выживать",
        "suspect": "подозревать",
        "swim": "плавать",
        "take": "брать",
        "talk": "разговаривать",
        "taste": "пробовать",
        "teach": "учить",
        "tear": "рвать",
        "tell": "рассказывать",
        "tend": "иметь тенденцию",
        "test": "проверять",
        "thank": "благодарить",
        "think": "думать",
        "throw": "бросать",
        "touch": "трогать",
        "train": "тренировать",
        "travel": "путешествовать",
        "treat": "обращаться",
        "try": "пытаться",
        "turn": "поворачивать",
        "understand": "понимать",
        "use": "использовать",
        "visit": "посещать",
        "wait": "ждать",
        "walk": "ходить",
        "want": "хотеть",
        "warn": "предупреждать",
        "wash": "мыть",
        "watch": "смотреть",
        "wear": "носить",
        "win": "побеждать",
        "wish": "желать",
        "work": "работать",
        "worry": "беспокоиться",
        "write": "писать",
    }

    # Проверяем, есть ли уже слова в базе
    cursor.execute("SELECT COUNT(*) FROM words")
    if cursor.fetchone()[0] == 0:
        for eng, rus in english_words.items():
            cursor.execute("INSERT OR IGNORE INTO words (english, russian) VALUES (?, ?)", (eng, rus))

    conn.commit()
    return conn



conn = init_db()
cursor = conn.cursor()

# Временное хранилище для текущих тестов
user_tests = {}
user_vocabulary = {}  # Для хранения текущего слова, предложенного пользователю
user_words_pagination = {}  # Для хранения пагинации пользователей

command_router = Router()


def get_word_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Добавить", callback_data="add_word"),
         InlineKeyboardButton(text="⏭ Пропустить", callback_data="skip_word")],
        [InlineKeyboardButton(text="📚 Мои слова", callback_data="my_words_1"),  # Изменено на my_words_1
         InlineKeyboardButton(text="📝 Тест", callback_data="start_test")]
    ])


async def get_random_word(user_id: int):
    # Получаем ID всех слов, которые пользователь уже добавлял
    cursor.execute('''
    SELECT word_id FROM user_words WHERE user_id = ?
    ''', (user_id,))
    used_word_ids = [row[0] for row in cursor.fetchall()]

    # Получаем случайное слово, которое пользователь еще не добавлял
    if used_word_ids:
        cursor.execute(f'''
        SELECT id, english, russian FROM words 
        WHERE id NOT IN ({','.join(['?'] * len(used_word_ids))}) 
        ORDER BY RANDOM() LIMIT 1
        ''', used_word_ids)
    else:
        cursor.execute('''
        SELECT id, english, russian FROM words 
        ORDER BY RANDOM() LIMIT 1
        ''')

    word_data = cursor.fetchone()

    if not word_data:
        # Если все слова использованы, начинаем сначала
        cursor.execute('''
        SELECT id, english, russian FROM words 
        ORDER BY RANDOM() LIMIT 1
        ''')
        word_data = cursor.fetchone()

    if word_data:
        word_id, word, translation = word_data
        user_vocabulary[user_id] = (word_id, word, translation)
        return word, translation
    return None, None


@command_router.message(Command('words'))
async def send_random_word(message: types.Message):
    user_id = message.chat.id
    word, translation = await get_random_word(user_id)

    if word and translation:
        await message.answer(
            text=f"🎲 Случайное слово:\n\n🔤 {word}\n🇷🇺 {translation}",
            reply_markup=get_word_keyboard()
        )
    else:
        await message.answer("😕 Не удалось найти новое слово. Попробуйте позже.")


@command_router.callback_query(F.data == "add_word")
async def handle_add_word(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id in user_vocabulary:
        word_id, word, translation = user_vocabulary[user_id]

        try:
            # Добавляем слово в словарь пользователя
            cursor.execute('''
            INSERT OR IGNORE INTO user_words (user_id, word_id) 
            VALUES (?, ?)
            ''', (user_id, word_id))

            # Обновляем прогресс
            cursor.execute('''
            INSERT OR IGNORE INTO user_progress (user_id, added, skipped) 
            VALUES (?, 0, 0)
            ''', (user_id,))

            cursor.execute('''
            UPDATE user_progress 
            SET added = added + 1 
            WHERE user_id = ?
            ''', (user_id,))

            conn.commit()

            # Удаляем сообщение с предложением слова
            await callback.message.delete()
            await callback.answer("✅ Слово добавлено в ваш словарь!")

            # Отправляем новое слово
            await send_random_word(callback.message)
        except Exception as e:
            logging.error(f"Error adding word: {e}")
            await callback.answer("⚠️ Произошла ошибка при добавлении слова")
    else:
        await callback.answer("⚠️ Не удалось добавить слово. Попробуйте снова.")


@command_router.callback_query(F.data == "skip_word")
async def handle_skip_word(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    try:
        # Обновляем прогресс
        cursor.execute('''
        INSERT OR IGNORE INTO user_progress (user_id, added, skipped) 
        VALUES (?, 0, 0)
        ''', (user_id,))

        cursor.execute('''
        UPDATE user_progress 
        SET skipped = skipped + 1 
        WHERE user_id = ?
        ''', (user_id,))

        conn.commit()

        await callback.answer("⏭ Слово пропущено")
        await send_random_word(callback.message)
    except Exception as e:
        logging.error(f"Error skipping word: {e}")
        await callback.answer("⚠️ Произошла ошибка при пропуске слова")


def get_mywords_keyboard(user_id: int, page: int = 1):
    # Получаем общее количество слов пользователя
    cursor.execute('''
    SELECT COUNT(*) FROM user_words WHERE user_id = ?
    ''', (user_id,))
    total_words = cursor.fetchone()[0]

    buttons = []

    # Если слов больше 20, добавляем кнопки пагинации
    if total_words > 20:
        total_pages = (total_words + 19) // 20  # Округляем вверх

        # Добавляем кнопку "Удалить все слова"
        buttons.append([InlineKeyboardButton(text="🗑 Удалить все слова", callback_data="delete_all_words")])

        # Добавляем кнопки навигации
        nav_buttons = []
        if page > 1:
            nav_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"my_words_{page - 1}"))
        if page < total_pages:
            nav_buttons.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"my_words_{page + 1}"))
        if nav_buttons:
            buttons.append(nav_buttons)

    # Добавляем кнопку возврата в меню
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


@command_router.callback_query(F.data.startswith("my_words_"))
async def handle_my_words_pagination(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    page = int(callback.data.split("_")[-1])

    try:
        # Получаем добавленные слова пользователя с пагинацией
        offset = (page - 1) * 20
        cursor.execute('''
        SELECT w.english, w.russian 
        FROM user_words uw
        JOIN words w ON uw.word_id = w.id
        WHERE uw.user_id = ?
        ORDER BY w.english
        LIMIT 20 OFFSET ?
        ''', (user_id, offset))
        user_words = cursor.fetchall()

        # Получаем прогресс пользователя
        cursor.execute('''
        SELECT added, skipped, correct, wrong 
        FROM user_progress 
        WHERE user_id = ?
        ''', (user_id,))
        progress = cursor.fetchone()

        if user_words:
            words_list = "\n".join([f"🔤 {word} - 🇷🇺 {trans}" for word, trans in user_words])

            # Получаем общее количество слов
            cursor.execute('''
            SELECT COUNT(*) FROM user_words WHERE user_id = ?
            ''', (user_id,))
            total_words = cursor.fetchone()[0]

            page_info = f"\n\n📄 Страница {page} из {(total_words + 19) // 20}" if total_words > 20 else ""

            if progress:
                stats = f"\n\n📊 Ваш прогресс:\n✅ Добавлено: {progress[0]}\n⏭ Пропущено: {progress[1]}"
                if progress[2] or progress[3]:
                    stats += f"\n📝 Тесты:\n✔️ Правильно: {progress[2]}\n❌ Неправильно: {progress[3]}"
            else:
                stats = "\n\n📊 Прогресс пока не доступен"

            await callback.message.edit_text(
                text=f"📚 Ваши добавленные слова ({total_words}):\n\n{words_list}{page_info}{stats}",
                reply_markup=get_mywords_keyboard(user_id, page)
            )
        else:
            await callback.message.edit_text(
                text="📚 У вас пока нет добавленных слов. Нажмите '✅ Добавить', чтобы сохранить слова.",
                reply_markup=get_word_keyboard()
            )
    except Exception as e:
        logging.error(f"Error getting user words: {e}")
        await callback.message.answer("⚠️ Произошла ошибка при получении ваших слов")

    await callback.answer()


@command_router.callback_query(F.data == "delete_all_words")
async def handle_delete_all_words(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    # Создаем клавиатуру с подтверждением удаления
    confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да, удалить", callback_data="confirm_delete_all")],
        [InlineKeyboardButton(text="❌ Нет, отмена", callback_data=f"my_words_1")]
    ])

    await callback.message.edit_text(
        text="⚠️ Вы уверены, что хотите удалить ВСЕ слова из вашего словаря? Это действие нельзя отменить!",
        reply_markup=confirm_keyboard
    )
    await callback.answer()


@command_router.callback_query(F.data == "confirm_delete_all")
async def handle_confirm_delete_all(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    try:
        # Удаляем все слова пользователя
        cursor.execute('''
        DELETE FROM user_words WHERE user_id = ?
        ''', (user_id,))

        # Обновляем прогресс (обнуляем только добавленные слова)
        cursor.execute('''
        UPDATE user_progress 
        SET added = 0 
        WHERE user_id = ?
        ''', (user_id,))

        conn.commit()

        await callback.message.edit_text(
            text="🗑 Все слова успешно удалены из вашего словаря!",
            reply_markup=get_word_keyboard()
        )
    except Exception as e:
        logging.error(f"Error deleting all words: {e}")
        await callback.message.edit_text(
            text="⚠️ Произошла ошибка при удалении слов",
            reply_markup=get_word_keyboard()
        )

    await callback.answer()


@command_router.message(Command('mywords'))
async def handle_mywords_command(message: types.Message):
    user_id = message.from_user.id

    try:
        # Получаем первую страницу слов
        await handle_my_words_pagination(types.CallbackQuery(
            message=message,
            data="my_words_1",
            from_user=message.from_user
        ))
    except Exception as e:
        logging.error(f"Error getting user words: {e}")
        await message.answer("Ваш словарь пусте. Добавление новых слов /words")


def get_test_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Пройти тест еще раз", callback_data="more_test")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_menu")]
    ])


async def generate_test(user_id: int):
    """Генерирует тест только из добавленных пользователем слов"""
    try:
        # Проверяем, что у пользователя достаточно слов для теста
        cursor.execute('''
        SELECT COUNT(*) FROM user_words WHERE user_id = ?
        ''', (user_id,))
        if cursor.fetchone()[0] < 4:
            return None, None, None

        # Выбираем случайное слово из добавленных пользователем
        cursor.execute('''
        SELECT w.id, w.english, w.russian 
        FROM user_words uw
        JOIN words w ON uw.word_id = w.id
        WHERE uw.user_id = ?
        ORDER BY RANDOM() 
        LIMIT 1
        ''', (user_id,))
        test_word_data = cursor.fetchone()

        if not test_word_data:
            return None, None, None

        word_id, test_word, correct_answer = test_word_data

        # Собираем 3 случайных неправильных ответа из ТОЛЬКО добавленных слов
        cursor.execute('''
        SELECT w.russian 
        FROM user_words uw
        JOIN words w ON uw.word_id = w.id
        WHERE uw.user_id = ? AND w.russian != ?
        ORDER BY RANDOM() 
        LIMIT 3
        ''', (user_id, correct_answer))
        wrong_answers = [row[0] for row in cursor.fetchall()]

        # Если не хватает неправильных ответов, дополняем случайными словами
        while len(wrong_answers) < 3:
            cursor.execute('''
            SELECT russian FROM words 
            WHERE russian != ? 
            ORDER BY RANDOM() 
            LIMIT 1
            ''', (correct_answer,))
            word = cursor.fetchone()
            if word and word[0] not in wrong_answers:
                wrong_answers.append(word[0])

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
    except Exception as e:
        logging.error(f"Error generating test: {e}")
        return None, None, None


@command_router.callback_query(F.data == "start_test")
async def handle_start_test(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    try:
        # Проверяем, что у пользователя достаточно слов для теста
        cursor.execute('''
        SELECT COUNT(*) FROM user_words WHERE user_id = ?
        ''', (user_id,))
        if cursor.fetchone()[0] < 4:
            await callback.answer(
                "📝 Для прохождения теста нужно добавить как минимум 4 слова!",
                show_alert=True
            )
            return

        test_word, answers, _ = await generate_test(user_id)

        if not test_word or not answers:
            await callback.answer("⚠️ Не удалось создать тест. Попробуйте позже.")
            return

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
    except Exception as e:
        logging.error(f"Error starting test: {e}")
        await callback.answer("⚠️ Произошла ошибка при запуске теста")

    await callback.answer()


@command_router.message(Command('test'))
async def handle_test(message: types.Message):
    user_id = message.from_user.id

    try:
        # Проверяем, что у пользователя достаточно слов для теста
        cursor.execute('''
        SELECT COUNT(*) FROM user_words WHERE user_id = ?
        ''', (user_id,))
        if cursor.fetchone()[0] < 4:
            await message.answer(
                "📝 Для прохождения теста нужно добавить как минимум 4 слова.\n"
                "Используйте /words, чтобы добавить новые слова!"
            )
            return

        test_word, answers, _ = await generate_test(user_id)

        if not test_word or not answers:
            await message.answer("⚠️ Не удалось создать тест. Попробуйте позже.")
            return

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
    except Exception as e:
        logging.error(f"Error starting test: {e}")
        await message.answer("⚠️ Произошла ошибка при запуске теста")


@command_router.callback_query(F.data.startswith("test_answer_"))
async def handle_test_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    answer_index = int(callback.data.split("_")[-1])

    if user_id not in user_tests:
        await callback.answer("❌ Тест устарел или не найден. Начните новый.")
        return

    test_data = user_tests[user_id]

    try:
        if test_data["answers"][answer_index] == test_data["correct"]:
            response = "✅ Правильно! Отличная работа!"
            # Обновляем прогресс
            cursor.execute('''
            UPDATE user_progress 
            SET correct = correct + 1 
            WHERE user_id = ?
            ''', (user_id,))
        else:
            response = f"❌ Неправильно. Правильный ответ: '{test_data['correct']}'"
            # Обновляем прогресс
            cursor.execute('''
            UPDATE user_progress 
            SET wrong = wrong + 1 
            WHERE user_id = ?
            ''', (user_id,))

        conn.commit()

        await callback.message.edit_text(
            text=f"{response}\n\nСлово: {test_data['word']}\nПеревод: {test_data['correct']}",
            reply_markup=get_test_keyboard()
        )
    except Exception as e:
        logging.error(f"Error processing test answer: {e}")
        await callback.answer("⚠️ Произошла ошибка при обработке ответа")

    await callback.answer()


@command_router.callback_query(F.data == "more_test")
async def handle_more_test(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    try:
        # Проверяем, что у пользователя достаточно слов для теста
        cursor.execute('''
        SELECT COUNT(*) FROM user_words WHERE user_id = ?
        ''', (user_id,))
        if cursor.fetchone()[0] < 4:
            await callback.answer("❌ Недостаточно слов для теста. Добавьте больше слов!")
            return

        test_word, answers, _ = await generate_test(user_id)

        if not test_word or not answers:
            await callback.answer("⚠️ Не удалось создать тест. Попробуйте позже.")
            return

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
    except Exception as e:
        logging.error(f"Error generating more test: {e}")
        await callback.answer("⚠️ Произошла ошибка при создании теста")

    await callback.answer()


@command_router.callback_query(F.data == "to_menu")
async def handle_to_menu(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text(
            text="🏠 Вы вернулись в главное меню",
            reply_markup=get_word_keyboard()
        )
    except Exception as e:
        logging.error(f"Error returning to menu: {e}")
        await callback.answer("⚠️ Произошла ошибка при возврате в меню")

    await callback.answer()


def close_db():
    conn.close()


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
    start_message = ("🌟 <i>Добро пожаловать в SpeakUp Bot! </i>🌟\n\n"
                     "👋 Привет! Я ваш персональный помощник в изучении английского языка!\n\n"
                     "📚 Со мной вы сможете:\n"
                     "• Пополнять свой словарный запас\n"
                     "• Проверять свои знания в тестах\n"
                     "• Отслеживать свой прогресс\n\n"
                     "💡 Все мои услуги абсолютно <i>БЕСПЛАТНЫ</i>!\n\n"
                     "🛠 <i>Быстрый старт:</i>\n"
                     "🔹 /help - все доступные команды\n"
                     "🔹 /about - подробнее о возможностях\n"
                     "🔹 /words - начать учить новые слова прямо сейчас!\n\n"
                     "🎉 Давайте сделаем изучение английского увлекательным вместе!")
    await message.answer(text=start_message, parse_mode='HTML')


@command_router.message(Command('about'))
async def handle_about(message: types.Message):
    about_message = (
        "SpeakUp Bot – это умный помощник для изучения английских слов легко и эффективно!\n"
        '\n'
        "✨ Что умеет бот?\n"
        '\n'
        "1.📚 Учит новым словам с примерами\n"
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
        "Версия 1.0 | Если нужно что-то добавить или у вас вылезает ошибка, писать @Installer_editor36\n"
        '\n'
        'НАЖМИ (/words) ЧТОБЫ НАЧАТЬ УЧИТЬ АНГЛИЙСКИЙ\n'
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


g = ['пока', "bye", "goodbye"]


@command_router.message(lambda message: message.text.lower() in g)
async def reply_goodbye(message: types.Message):
    await message.answer(text="🥺 See you! Have a nice day, Bro :)")


@command_router.message(F.text.lower().contains('thank you'))
async def reply_thanks(message: types.Message):
    await message.answer(text="🥰 You are welcome! 🥰")


@command_router.message(Command('topics'))
async def handle_topics(message: types.Message):
    await message.answer(text="Функция выбора тем в разработке!")


@command_router.message(F.text.lower().contains("перевод"))
async def reply_goodbye(message: types.Message):
    await message.answer(text="Translate", reply_markup=funny_keyboard)


@command_router.message(Command('english'))
async def send_photo(message: types.Message):
    await message.answer_photo(
        photo='https://i.postimg.cc/X7CT7Gbj/Lucid-Realism-Create-an-illustration-featuring-the-Union-Jack-1.jpg',
        caption='❤️Учим английский вместе❤️!',
    )



