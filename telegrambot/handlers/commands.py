import sqlite3
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import logging

from keyboars.inline import funny_keyboard

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

ADMIN_ID = 5098839971
DEFAULT_WORDS = {
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
        "offer": "предлагать",
        "pretend": "притворяться",
        "react": "реагировать",
        "smile": "улыбаться",
        "trust": "доверять",
        "wonder": "интересоваться",
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
        'swear':'клятва',
        "bake": "печь",
        "swim": "купаться",
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
        "ask": "спрашивать",
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
        "aisle": "проход",
        "bargain": "выгодная покупка",
        "complimentary":
        "бесплатный (предоставляемый)",
        "delivery": "доставка",
        "expiry": "срок годности",
        "fragile": "хрупкий",
        "gadget": "гаджет",
        "handy": "удобный",
        "inventory": "ассортимент",
        "junk": "хлам",
        "knickknack": "безделушка",
        "landmark": "ориентир",
        "malfunction": "неисправность",
        "novelty": "новинка",
        "outlet": "розетка/аутлет",
        "package": "пакет/посылка",
        "quirky": "необычный",
        "receipt": "чек",
        "souvenir": "сувенир",
        "tag": "ценник/бирка",
        "upgrade": "улучшение",
        "voucher": "талон",
        "warranty": "гарантия",
        "aisle seat": "место у прохода",
        "bellhop": "носильщик",
        "concierge": "консьерж",
        "doorman": "швейцар",
        "etiquette": "этикет",
        "fare": "плата за проезд",
        "gratuity": "чаевые",
        "hostel": "хостел",
        "itinerary": "маршрут",
        "keycard": "ключ-карта",
        "lodging": "жилье",
        "motel": "мотель",
        "no-show": "неявка",
        "overnight": "ночевка",
        "pit stop": "остановка в пути",
        "queue": "очередь",
        "reservation": "бронирование",
        "stopover": "транзит",
        "transit": "пересадка",
        "utilities": "коммунальные услуги",
        "vacancy": "свободные места",
        "walk-in": "без записи",
        "exchange rate": "курс обмена",
        "zip code": "почтовый индекс",
        "rush hour": "час пик",
        "awkward": "неловкий",
        'go out':'пойти гулять на улицу',
        "banter": "дружеский подтрунивание",
        "chitchat": "светская беседа",
        "dense": "недогадливый",
        "egotistical": "самовлюбленный",
        "flaky": "ненадежный",
        "gossip": "сплетни",
        "humblebrag": "скромное хвастовство",
        "icebreaker": "способ разрядить обстановку",
        "jabber": "болтовня",
        "kudos": "похвала",
        "lousy": "отвратительный",
        "moody": "переменчивый",
        "nosy": "любопытный",
        "offbeat": "нестандартный",
        "petty": "мелочный",
        "quirky": "с причудами",
        "rant": "гневная тирада",
        "sassy": "дерзкий",
        "tactless": "бестактный",
        "uptight": "напряженный",
        "vibe": "атмосфера",
        "whiny": "нытик",
        "small talk": "светская беседа",
        "backhanded compliment": "комплимент с подтекстом",
        "blunt": "прямолинейный",
        "cheesy": "банальный",
        "dorky": "чудаковатый",
        "facepalm": "жест разочарования",
        "geeky": "увлекающийся технологиями",
        "hang out": "тусоваться",
        "jumpy": "нервный",
        "laid-back": "расслабленный",
        "mellow": "спокойный",
        "nerdy": "ботанистый",
        "obnoxious": "неприятный",
        "pushy": "настойчивый",
        "quirky": "своеобразный",
        "rowdy": "шумный",
        "snarky": "язвительный",
        "thrifty": "бережливый",
        "unplug": "отключаться (от техники)",
        "vegan": "веган",
        "woke": "просвещенный",
        "xenial": "гостеприимный",
        "yappy": "болтливый",
        "zing": "колкость",
        "airdrop": "передача файлов",
        "binge-watch": "смотреть подряд",
        "clickbait": "замануха",
        "deepfake": "фейковое видео",
        "emoji": "эмодзи",
        "fomo": "страх упустить возможность",
        "glitch": "сбой",
        "junk mail": "спам",
        "livestream": "прямая трансляция",
        "meme": "мем",
        "notifications": "уведомления",
        "on-brand": "соответствующий стилю",
        "podcast": "подкаст",
        "QR code": "QR-код",
        "reboot": "перезагрузка",
        "spoiler": "спойлер",
        "troll": "тролль",
        "unfriend": "удалить из друзей",
        "app": "приложение",
        "blog": "блог",
        "crowdfund": "краудфандинг",
        "download": "скачивать",
        "ebook": "электронная книга",
        "firewall": "брандмауэр",
        "gigabyte": "гигабайт",
        "homepage": "главная страница",
        "inbox": "входящие",
        "jpeg": "jpeg",
        "keyboard": "клавиатура",
        "lag": "задержка",
        "netizen": "пользователь интернета",
        "offline": "вне сети",
        "phishing": "фишинг",
        "spam": "спам",
        "tablet": "планшет",
        "username": "имя пользователя",
        "vlog": "видеоблог",
        "webinar": "вебинар",
        "boarding pass": "посадочный талон",
        "carry-on": "ручная кладь",
        "connecting flight": "стыковочный рейс",
        "departure gate": "выход на посадку",
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
        "doggie bag": "еда с собой из ресторана",
        "fixed menu": "фиксированное меню",
        "gluten-free": "без глютена",
        "happy hour": "счастливый час",
        "ingredients": "ингредиенты",
        'nature': 'природа',
        "lactose-free": "без лактозы",
        "mocktail": "безалкогольный коктейль",
        "nutritious": "питательный",
        "organic": "органический",
        "portion size": "размер порции",
        "reservation": "бронирование",
        "side dish": "гарнир",
        "tap water": "вода из-под крана",
        "utensils": "столовые приборы",
        "vegan option": "веганская опция",
        "waitlist": "лист ожидания",
        "brunch": "поздний завтрак",
        "condiments": "приправы",
        "dietary restrictions": "пищевые ограничения",
        "food poisoning": "пищевое отравление",
        "homemade": "домашнего приготовления",
        "barcode": "штрих-код",
        "clearance sale": "распродажа",
        "discount code": "код скидки",
        "exchange policy": "политика обмена",
        "final sale": "без возврата",
        "gift receipt": "подарочный чек",
        "in stock": "в наличии",
        "jewelry ": " бижутерия",
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
        'royalty':'королевский',
        "unworn": "не ношенный",
        "value pack": "выгодная упаковка",
        "exchange desk": "стойка обмена",
        "fitting room": "примерочная",
        "gift wrapping": "подарочная упаковка",
        "impulse buy": "спонтанная покупка",
        "last season": "прошлый сезон",
        "must-have": "необходимая вещь",
        "on clearance": "на распродаже",
        "price tag": "ценник",
        "shopping cart": "тележка для покупок",
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
        "utilities": "коммунальные услуги",
        "vandalism": "вандализм",
        "water damage": "повреждение от воды",
        "xerox copy": "ксерокопия",
        "yard sale": "распродажа во дворе",
        "after hours": "в нерабочее время",
        "break-in": "взлом",
        "customer service": "обслуживание клиентов",
        "dress code": "дресс-код",
        "electrician": "электрик",
        'stick at': 'упорно над чем-то трудиться',
        'youth': 'молодежь',
        "muscle": "мышца",
        "nail": "ноготь",
        "neck": "шея",
        "nerve": "нерв",
        "nose": "нос",
        "palm": "ладонь",
        "rib": "ребро",
        "ring finger": "безымянный палец",
        "skeleton": "скелет",
        "skin": "кожа",
        "skull": "череп",
        "stomach": "желудок",
        "throat": "горло",
        "thumb": "большой палец",
        "toe": "палец на ноге",
        "tongue": "язык",
        "tooth": "зуб",
        "wrist": "запястье",
        "active": "активный",
        "angry": "злой",
        "blue": "грустный",
        "boring": "скучный",
        "brave": "храбрый",
        "calm": "спокойный",
        "careful": "осторожный",
        "character": "характер",
        "cheerful": "радостный",
        "clever": "умный",
        "confused": "сбитый с толку",
        "creative": "креативный, творческий",
        "cruel": "жестокий",
        "curious": "любопытный",
        "easy-going": "легкий на подъем",
        "emotional": "эмоциональный",
        "excited": "взволнованный",
        "fair": "честный",
        "friendly": "дружелюбный",
        "generous": "щедрый",
        "genius": "гениальный",
        "gentle": "мягкий",
        "glad": "довольный",
        "greedy": "жадный",
        "happy": "счастливый",
        "hard-working": "трудолюбивый",
        "honest": "честный",
        "intelligent": "умный",
        "jealous": "ревнивый, завистливый",
        "kind": "добрый",
        "lazy": "ленивый",
        "loyal": "верный",
        "lucky": "удачливый",
        "moody": "хмурый",
        "nervous": "нервный",
        "open": "открытый",
        "optimistic": "оптимистичный",
        "patient": "терпеливый",
        "proud": "гордый",
        "quiet": "тихий",
        "reliable": "надежный",
        "romantic": "романтичный",
        "rude": "грубый",
        "sad": "грустный",
        "shy": "стеснительный",
        "sensitive": "чувствительный",
        "serious": "серьезный",
        "stupid": "глупый",
        "talented": "талантливый",
        "tough": "жесткий",
        "upset": "расстроенный",
        "wise": "мудрый",
        "witty": "остроумный",
        "adoption": "усыновление",
        "aunt": "тетя",
        "boyfriend": "парень (друг)",
        "bride": "невеста",
        "brother": "брат",
        "brother-in-law": "шурин, деверь",
        "cousin": "двоюродный брат или сестра",
        "daughter": "дочь",
        "daughter-in-law": "сноха, невестка",
        "divorce": "развод",
        "engagement": "помолвка",
        "ex-husband": "бывший муж",
        "ex-wife": "бывшая жена",
        "family": "семья",
        "father": "отец",
        "foster family": "приемная семья",
        "friend": "друг",
        "girlfriend": "девушка (подруга)",
        "godfather": "крестный отец",
        "godmother": "крестная мать",
        "grandchildren": "внуки",
        "granddaughter": "внучка",
        "grandfather": "дедушка",
        "grandmother": "бабушка",
        "grandparents": "бабушка и дедушка",
        "grandson": "внук",
        "half-brother": "брат со стороны отца или матери",
        "half-sister": "сестра со стороны отца или матери",
        "husband": "муж",
        "lover": "любовник(-ца)",
        "marriage": "брак",
        "mother": "мать",
        "mother-in-law": "теща, свекровь",
        "nephew": "племянник",
        "niece": "племянница",
        "parents": "родители",
        "relative": "родственник",
        "sister": "сестра",
        "son": "сын",
        "stepbrother": "сводный брат",
        "stepfather": "отчим",
        "stepmother": "мачеха",
        "stepsister": "сводная сестра",
        "twins": "близнецы",
        "uncle": "дядя",
        "wedding": "свадьба",
        "widow": "вдова",
        "widower": "вдовец",
        "wife": "жена",
        'to rest':'отдыхать',
        "go out": "развлекаться вне дома",
        "eat out": "обедать в ресторане",
        "check out": "1) выезжать из гостиницы; 2) проверять",
        "give out": "раздавать что-то бесплатно",
        "come out": "оказываться, выясняться",
        "work out": "1) тренироваться; 2) разбираться",
        "break up": "расстаться, прекратить отношения",
        "break down": "1) сломаться; 2) потерять контроль над собой",
        "call by": "зайти, навестить",
        "bring up": "1) воспитывать; 2) поднимать тему",
        "call off": "отменять",
        "find out": "узнавать",
        "give up": "сдаваться",
        "look after": "заботиться",
        "put off": "откладывать",
        "run into": "случайно встретить",
        "set up": "организовывать",
        "take off": "1) взлетать; 2) снимать (одежду)",
        "break up": "расставаться",
        "come up with": "предлагать идею",
        "get through": "справляться с трудностями",
        "hold on": "подождать",
        "keep up": "поддерживать уровень",
        "let down": "подвести",
        "look forward to": "ждать с нетерпением",
        "put up with": "терпеть",
        "show up": "появляться",
        "stand out": "выделяться",
        "turn up": "1) приходить; 2) увеличивать громкость",
        "cut off": "прерывать",
        "drop off": "подбросить (на машине)",
        "fall apart": "разрушаться",
        "give in": "уступать",
        "pass out": "терять сознание",
        "take after": "быть похожим",
        "try on": "примерять",
        "turn down": "1) отказывать; 2) уменьшать громкость",
        "back up": "1) поддерживать; 2) создавать резервную копию",
        "blow up": "1) взрывать; 2) злиться",
        "bring about": "вызывать, приводить к",
        "carry on": "продолжать",
        "come across": "1) натыкаться; 2) производить впечатление",
        "come over": "заходить в гости",
        "do away with": "покончить с, устранить",
        "dress up": "наряжаться",
        "end up": "в конечном итоге",
        "figure out": "понимать, решать",
        "fill in": "1) заполнять; 2) заменять",
        "get along": "ладить",
        "get away": "уйти, сбежать",
        "get over": "1) оправиться; 2) преодолеть",
        "go ahead": "продолжать, начинать",
        "go through": "1) пережить; 2) тщательно изучить",
        "hand in": "сдавать (работу)",
        "hang out": "тусоваться",
        "leave out": "пропускать, исключать",
        "make up": "1) выдумывать; 2) мириться",
        "pick up": "1) подбирать; 2) улучшаться",
        "point out": "указывать",
        "pull over": "притормозить (о машине)",
        "put aside": "откладывать",
        "put on": "1) надевать; 2) включать",
        "run out": "заканчиваться",
        "settle down": "1) успокаиваться; 2) остепениться",
        "speak up": "говорить громче",
        "take up": "1) начинать заниматься; 2) занимать место",
        "think over": "обдумывать",
        "turn off": "1) выключать; 2) отталкивать",
        "turn on": "1) включать; 2) возбуждать",
        "watch out": "быть осторожным",
        "can": "мочь (физическая возможность)",
        "could": "1) мог (прошедшее от can); 2) мог бы (вежливая форма)",
        "may": "можно (разрешение), может (вероятность)",
        "might": "может (меньшая вероятность)",
        "must": "должен (обязанность)",
        "shall": "должен (в вопросах, предложениях)",
        "should": "следует (совет)",
        "will": "будет (будущее время)",
        "would": "1) бы (условное наклонение); 2) привычка в прошлом",
        "ought to": "следует (моральный долг)",
        "have to": "должен (внешняя необходимость)",
        "need to": "нужно (необходимость)",
        "be able to": "быть в состоянии",
        "be allowed to": "иметь разрешение",
        "be supposed to": "предполагается, что должен",
        "had better": "лучше бы (совет)",
        "would rather": "предпочел бы",
        "dare": "осмеливаться",
        "need": "нуждаться",
        "used to": "раньше (привычка в прошлом)",
        "act up": "1) плохо себя вести; 2) барахлить (о технике)",
        "answer back": "огрызаться, дерзить",
        "bank on": "рассчитывать на",
        "barge in": "вламываться, вмешиваться",
        "bear out": "подтверждать",
        "beat up": "избивать",
        "black out": "1) терять сознание; 2) затемнять",
        "block off": "блокировать, перекрывать",
        "boil down to": "сводиться к",
        "branch out": "расширять деятельность",
        "brush up": "освежать знания",
        "bump into": "случайно встретить",
        "buy out": "выкупать долю",
        "call around": "обзванивать",
        "call back": "перезванивать",
        "carry out": "выполнять",
        "catch on": "становиться популярным",
        "chicken out": "струсить",
        "chip in": "скидываться деньгами",
        "clamp down": "ужесточить контроль",
        "conk out": "1) сломаться; 2) отрубиться (заснуть)",
        "count on": "рассчитывать на",
        "cross out": "вычеркивать",
        "deal with": "иметь дело с",
        "do without": "обходиться без",
        "drag on": "затягиваться",
        "draw up": "1) составлять документ; 2) подъезжать",
        "drown out": "заглушать звук",
        "face up to": "признавать проблему",
        "fend off": "отбиваться",
        "fizzle out": "сойти на нет",
        "flare up": "1) вспыхивать; 2) обостряться (о болезни)",
        "fool around": "валять дурака",
        "geek out": "увлекаться (технологиями)",
        "go about": "приступать к",
        "grow on": "нравиться со временем",
        "hang up": "1) вешать трубку; 2) вешать (на крючок)",
        "hit back": "давать сдачи",
        "jack up": "1) поднимать домкратом; 2) повышать цены",
        "knock out": "1) нокаутировать; 2) впечатлять",
        "be bound to": "непременно (должен произойти)",
        "be likely to": "вероятно",
        "be meant to": "предназначен для",
        "be to": "должен (по плану)",
        "can't help": "не могу не",
        "couldn't help": "не мог не",
        "would rather": "предпочел бы",
        "would sooner": "скорее бы",
        "may as well": "можно и",
        "might as well": "можно и",
        "shall not": "не должен (запрет)",
        "should have": "должен был (в прошлом)",
        "must have": "должно быть (догадка)",
        "can't have": "не может быть",
        "needn't have": "не нужно было",
        "dare not": "не смею",
        "need not": "не нужно",
        "used not to": "раньше не",

        # Фразовые глаголы с частицами
        "get by": "сводить концы с концами",
        "give away": "1) раздавать; 2) выдавать секрет",
        "go after": "преследовать цель",
        "go against": "противоречить",
        "hold back": "1) сдерживать; 2) утаивать",
        "keep on": "продолжать",
        "let in": "впускать",
        "look into": "исследовать",
        "make out": "1) понимать; 2) целоваться",
        "pass away": "умереть",
        "put down": "1) записывать; 2) усыплять животное",
        "put forward": "выдвигать",
        "rule out": "исключать возможность",
        "see through": "раскусить",
        "send off": "отправлять",
        "set aside": "откладывать",
        "stand by": "1) поддерживать; 2) быть готовым",
        "take in": "1) понимать; 2) обманывать",
        "talk over": "обсуждать",
        "throw away": "выбрасывать",
        "touch on": "касаться темы",
        "turn around": "1) разворачиваться; 2) улучшать",
        "wind up": "1) заканчивать; 2) заводить (механизм)",
        "awkward": "неловкий",
        "bargain": "выгодная покупка",
        "blurry": "размытый",
        "clumsy": "неуклюжий",
        "dread": "сильно бояться",
        "fluffy": "пушистый",
        "gloomy": "мрачный",
        "grumpy": "ворчливый",
        "hassle": "неприятность",
        "junk": "хлам",
        "appliance": "бытовая техника",
        "clutter": "беспорядок",
        "drafty": "продуваемый (о помещении)",
        "flicker": "мерцать",
        "leaky": "протекающий",
        "stain": "пятно",
        "stuffy": "душный",
        "tangled": "спутанный",
        "wobbly": "шаткий",
        "wrinkled": "помятый",
        "bland": "пресный",
        "crunchy": "хрустящий",
        "expire": "истекать (о сроке годности)",
        "leftovers": "остатки еды",
        "melt": "таять",
        "ripe": "спелый",
        "rotten": "гнилой",
        "spicy": "острый",
        "stale": "черствый",
        "tart": "терпкий",
        "commute": "ехать на работу",
        "detour": "объезд",
        "fare": "плата за проезд",
        "jam": "пробка",
        "landmark": "ориентир",
        "pedestrian": "пешеход",
        "rush hour": "час пик",
        "sidewalk": "тротуар",
        "suburb": "пригород",
        "venue": "место проведения",
        "ache": "боль",
        "bruise": "синяк",
        "dizzy": "головокружение",
        "nauseous": "тошнота",
        "rash": "сыпь",
        "sore": "больной",
        "swollen": "опухший",
        "throbbing": "пульсирующий (о боли)",
        "twist": "вывихнуть",
        "wheezy": "хрипящий",
        "breeze": "легкий ветер",
        "chilly": "прохладно",
        "drizzle": "мелкий дождь",
        "frost": "иней",
        "humid": "влажный",
        "muggy": "душный (о погоде)",
        "overcast": "пасмурно",
        "puddle": "лужа",
        "sunburn": "солнечный ожог",
        "thaw": "оттепель",
        "by the way": "кстати",
        "hang on": "подожди",
        "I reckon": "я считаю",
        "no worries": "не беспокойся",
        "sort of": "вроде как",
        "what's up?": "как дела?",
        "you bet": "конечно",
        "my bad": "моя вина",
        "no biggie": "не проблема",
        "give it a shot": "попробуй"

}


command_router = Router()



def get_word_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Добавить", callback_data="add_word"),
         InlineKeyboardButton(text="⏭ Пропустить", callback_data="skip_word")],
        [InlineKeyboardButton(text="📚 Мои слова", callback_data="my_words_1"),
         InlineKeyboardButton(text="📝 Тест", callback_data="start_test")]
    ])





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


    for eng, rus in DEFAULT_WORDS.items():
        try:
            cursor.execute("INSERT OR IGNORE INTO words (english, russian) VALUES (?, ?)", (eng, rus))
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    return conn



conn = init_db()
cursor = conn.cursor()


user_tests = {}
user_vocabulary = {}
admin_add_word = {}

async def get_random_word(user_id: int):
    try:
        cursor.execute('SELECT word_id FROM user_words WHERE user_id = ?', (user_id,))
        used_word_ids = [row[0] for row in cursor.fetchall()]

        if used_word_ids:
            query = '''
            SELECT id, english, russian FROM words 
            WHERE id NOT IN ({}) 
            ORDER BY RANDOM() LIMIT 1
            '''.format(','.join(['?'] * len(used_word_ids)))
            cursor.execute(query, used_word_ids)
        else:
            cursor.execute('SELECT id, english, russian FROM words ORDER BY RANDOM() LIMIT 1')

        word_data = cursor.fetchone()

        if not word_data:
            cursor.execute('SELECT id, english, russian FROM words ORDER BY RANDOM() LIMIT 1')
            word_data = cursor.fetchone()

        if word_data:
            word_id, word, translation = word_data
            user_vocabulary[user_id] = (word_id, word, translation)
            return word, translation
        return None, None
    except Exception as e:
        logging.error(f"Error getting random word: {e}")
        return None, None


def get_mywords_keyboard(user_id: int, page: int = 1):
    try:
        cursor.execute('SELECT COUNT(*) FROM user_words WHERE user_id = ?', (user_id,))
        total_words = cursor.fetchone()[0]

        buttons = []

        if total_words > 0:
            buttons.append([InlineKeyboardButton(text="🗑 Удалить все слова", callback_data="delete_all_words")])

        if total_words > 20:
            total_pages = (total_words + 19) // 20
            nav_buttons = []
            if page > 1:
                nav_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"my_words_{page - 1}"))
            if page < total_pages:
                nav_buttons.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"my_words_{page + 1}"))
            if nav_buttons:
                buttons.append(nav_buttons)

        buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_menu")])

        return InlineKeyboardMarkup(inline_keyboard=buttons)
    except Exception as e:
        logging.error(f"Error creating mywords keyboard: {e}")
        return InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_menu")]])


def get_test_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Пройти тест еще раз", callback_data="more_test")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_menu")]
    ])


async def generate_test(user_id: int):
    try:
        cursor.execute('SELECT COUNT(*) FROM user_words WHERE user_id = ?', (user_id,))
        if cursor.fetchone()[0] < 4:
            return None, None, None

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

        cursor.execute('''
        SELECT w.russian 
        FROM user_words uw
        JOIN words w ON uw.word_id = w.id
        WHERE uw.user_id = ? AND w.russian != ?
        ORDER BY RANDOM() 
        LIMIT 3
        ''', (user_id, correct_answer))
        wrong_answers = [row[0] for row in cursor.fetchall()]

        while len(wrong_answers) < 3:
            cursor.execute('SELECT russian FROM words WHERE russian != ? ORDER BY RANDOM() LIMIT 1', (correct_answer,))
            word = cursor.fetchone()
            if word and word[0] not in wrong_answers:
                wrong_answers.append(word[0])

        all_answers = [correct_answer] + wrong_answers
        random.shuffle(all_answers)

        user_tests[user_id] = {
            "word": test_word,
            "correct": correct_answer,
            "answers": all_answers
        }

        return test_word, all_answers, all_answers.index(correct_answer)
    except Exception as e:
        logging.error(f"Error generating test: {e}")
        return None, None, None

@command_router.message(Command('start'))
async def handle_start(message: types.Message):
    start_message = (
        "🌟 <i>Добро пожаловать в SpeakUp Bot!</i> 🌟\n\n"
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
        "🎉 Давайте сделаем изучение английского увлекательным вместе!"
    )
    await message.answer(text=start_message, parse_mode='HTML')


@command_router.message(Command('help'))
async def handle_help(message: types.Message):
    help_message = (
        "🔹/about – информация о боте:\n"
        '\n'
        "🥺Обучение🥺:\n"
        '\n'
        "Напиши слово ( перевод ), если потребуется переводчик.\n"
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


@command_router.message(Command('about'))
async def handle_about(message: types.Message):
    about_message = (
        "SpeakUp Bot – это умный помощник для изучения английских слов легко и эффективно!\n"
        '\n'
        "✨ Что умеет бот?\n"
        '\n'
        "1.📚 Учит новым словам с примерами.\n"
        "2.🔄 Помогает повторять слова по алгоритму интервальных повторений.\n"
        "3.📊 Отслеживает ваш прогресс в обучении.\n"
        '\n'
        "📌 Принципы обучения:\n"
        '\n'
        "1.✔️ Мини-уроки по 5-10 минут в день.\n"
        "2.✔️ Игровой формат.\n"
        '\n'
        "❤️ Наша цель – сделать изучение английской лексики простым и увлекательным!❤️\n"
        '\n'
        "🤖 <b>Бот версии 1.0</b>\n"
        "⚙ Если есть ошибки или предложения — писать @Installer_editor36.\n"
        '\n'
        'НАЖМИ (/words) ЧТОБЫ НАЧАТЬ УЧИТЬ АНГЛИЙСКИЙ!\n'
        '\n'
        "Нажми /help, если нужно будет посмотреть какие есть у меня команды."
    )
    await message.answer(text=about_message,parse_mode='HTML')


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


@command_router.message(Command('mywords'))
async def handle_mywords_command(message: types.Message):
    user_id = message.from_user.id
    await show_my_words_page(user_id, message, 1)


async def show_my_words_page(user_id: int, message: types.Message | types.CallbackQuery, page: int):
    try:
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

        cursor.execute('SELECT added, skipped, correct, wrong FROM user_progress WHERE user_id = ?', (user_id,))
        progress = cursor.fetchone()

        if user_words:
            words_list = "\n".join([f"🔤 {word} - 🇷🇺 {trans}" for word, trans in user_words])

            cursor.execute('SELECT COUNT(*) FROM user_words WHERE user_id = ?', (user_id,))
            total_words = cursor.fetchone()[0]

            page_info = f"\n\n📄 Страница {page} из {(total_words + 19) // 20}" if total_words > 20 else ""

            if progress:
                stats = f"\n\n📊 Ваш прогресс:\n✅ Добавлено: {progress[0]}\n⏭ Пропущено: {progress[1]}"
                if progress[2] or progress[3]:
                    stats += f"\n📝 Тесты:\n✔️ Правильно: {progress[2]}\n❌ Неправильно: {progress[3]}"
            else:
                stats = "\n\n📊 Прогресс пока не доступен"

            text = f"📚 Ваши добавленные слова ({total_words}):\n\n{words_list}{page_info}{stats}"

            if isinstance(message, types.Message):
                await message.answer(text, reply_markup=get_mywords_keyboard(user_id, page))
            else:
                await message.message.edit_text(text, reply_markup=get_mywords_keyboard(user_id, page))
        else:
            text = "📚 У вас пока нет добавленных слов. Нажмите '✅ Добавить', чтобы сохранить слова."
            if isinstance(message, types.Message):
                await message.answer(text, reply_markup=get_word_keyboard())
            else:
                await message.message.edit_text(text, reply_markup=get_word_keyboard())
    except Exception as e:
        logging.error(f"Error showing my words page: {e}")
        error_text = "⚠️ Произошла ошибка при получении ваших слов"
        if isinstance(message, types.Message):
            await message.answer(error_text)
        else:
            await message.message.edit_text(error_text)


@command_router.message(Command('test'))
async def handle_test(message: types.Message):
    user_id = message.from_user.id
    await start_test_for_user(user_id, message)


async def start_test_for_user(user_id: int, message: types.Message | types.CallbackQuery):
    try:
        cursor.execute('SELECT COUNT(*) FROM user_words WHERE user_id = ?', (user_id,))
        if cursor.fetchone()[0] < 4:
            text = "📝 Для прохождения теста нужно добавить как минимум 4 слова.\nИспользуйте /words, чтобы добавить новые слова!"
            if isinstance(message, types.Message):
                await message.answer(text)
            else:
                await message.answer(text, show_alert=True)
            return

        test_word, answers, _ = await generate_test(user_id)

        if not test_word or not answers:
            text = "⚠️ Не удалось создать тест. Попробуйте позже."
            if isinstance(message, types.Message):
                await message.answer(text)
            else:
                await message.answer(text, show_alert=True)
            return

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=answers[0], callback_data="test_answer_0")],
            [InlineKeyboardButton(text=answers[1], callback_data="test_answer_1")],
            [InlineKeyboardButton(text=answers[2], callback_data="test_answer_2")],
            [InlineKeyboardButton(text=answers[3], callback_data="test_answer_3")],
        ])

        text = f"📝 Тест: Как переводится слово '{test_word}'?"

        if isinstance(message, types.Message):
            await message.answer(text, reply_markup=keyboard)
        else:
            await message.message.edit_text(text, reply_markup=keyboard)
    except Exception as e:
        logging.error(f"Error starting test: {e}")
        text = "⚠️ Произошла ошибка при запуске теста"
        if isinstance(message, types.Message):
            await message.answer(text)
        else:
            await message.answer(text, show_alert=True)


@command_router.message(Command('topics'))
async def handle_topics(message: types.Message):
    await message.answer(text="Функция выбора тем в разработке!")


@command_router.message(Command('english'))
async def send_photo(message: types.Message):
    await message.answer_photo(
        photo='https://i.postimg.cc/X7CT7Gbj/Lucid-Realism-Create-an-illustration-featuring-the-Union-Jack-1.jpg',
        caption='❤️Учим английский вместе❤️!',
    )

@command_router.message(Command('add_word'))
async def handle_add_word_command(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ У вас нет прав для выполнения этой команды.")
        return

    admin_add_word[message.from_user.id] = {'state': 'waiting_english'}
    await message.answer("✏️ Введите английское слово:")


@command_router.message(F.from_user.id == ADMIN_ID, F.text,
                        lambda message: admin_add_word.get(message.from_user.id, {}).get('state') == 'waiting_english')
async def handle_english_word_input(message: types.Message):
    english_word = message.text.strip().lower()

    cursor.execute("SELECT id FROM words WHERE english = ?", (english_word,))
    if cursor.fetchone():
        await message.answer(f"⚠️ Слово '{english_word}' уже существует в базе данных.")
        del admin_add_word[message.from_user.id]
        return

    admin_add_word[message.from_user.id] = {
        'state': 'waiting_russian',
        'english_word': english_word
    }
    await message.answer(f"✏️ Введите перевод для слова '{english_word}':")


@command_router.message(F.from_user.id == ADMIN_ID, F.text,
                        lambda message: admin_add_word.get(message.from_user.id, {}).get('state') == 'waiting_russian')
async def handle_russian_translation_input(message: types.Message):
    russian_translation = message.text.strip()
    user_data = admin_add_word[message.from_user.id]
    english_word = user_data['english_word']

    try:
        cursor.execute("INSERT INTO words (english, russian) VALUES (?, ?)",
                       (english_word, russian_translation))
        conn.commit()

        await message.answer(f"✅ Слово успешно добавлено:\n🔤 {english_word} - 🇷🇺 {russian_translation}")
        del admin_add_word[message.from_user.id]

        cursor.execute("SELECT id FROM words WHERE english = ?", (english_word,))
        if not cursor.fetchone():
            await message.answer("⚠️ Предупреждение: слово не было добавлено в базу данных. Пожалуйста, проверьте.")
    except sqlite3.IntegrityError:
        await message.answer(f"⚠️ Слово '{english_word}' уже существует в базе данных.")
    except Exception as e:
        logging.error(f"Error adding word by admin: {e}")
        await message.answer("⚠️ Произошла ошибка при добавлении слова. Попробуйте еще раз.")
    finally:
        if message.from_user.id in admin_add_word:
            del admin_add_word[message.from_user.id]

@command_router.callback_query(F.data == "add_word")
async def handle_add_word(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id in user_vocabulary:
        word_id, word, translation = user_vocabulary[user_id]

        try:
            cursor.execute('INSERT OR IGNORE INTO user_words (user_id, word_id) VALUES (?, ?)', (user_id, word_id))

            cursor.execute('INSERT OR IGNORE INTO user_progress (user_id, added, skipped) VALUES (?, 0, 0)', (user_id,))
            cursor.execute('UPDATE user_progress SET added = added + 1 WHERE user_id = ?', (user_id,))
            conn.commit()

            await callback.message.delete()
            await callback.answer("✅ Слово добавлено в ваш словарь!")
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
        cursor.execute('INSERT OR IGNORE INTO user_progress (user_id, added, skipped) VALUES (?, 0, 0)', (user_id,))
        cursor.execute('UPDATE user_progress SET skipped = skipped + 1 WHERE user_id = ?', (user_id,))
        conn.commit()

        await callback.message.delete()

        word, translation = await get_random_word(user_id)
        if word and translation:
            await callback.message.answer(
                text=f"🎲 Случайное слово:\n\n🔤 {word}\n🇷🇺 {translation}",
                reply_markup=get_word_keyboard()
            )
        else:
            await callback.message.answer("😕 Не удалось найти новое слово. Попробуйте позже.")

        await callback.answer()
    except Exception as e:
        logging.error(f"Error skipping word: {e}")
        await callback.answer("⚠️ Произошла ошибка при пропуске слова")


@command_router.callback_query(F.data.startswith("my_words_"))
async def handle_my_words_pagination(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    page = int(callback.data.split("_")[-1])
    await show_my_words_page(user_id, callback, page)
    await callback.answer()


@command_router.callback_query(F.data == "delete_all_words")
async def handle_delete_all_words(callback: types.CallbackQuery):
    user_id = callback.from_user.id

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
        cursor.execute('DELETE FROM user_words WHERE user_id = ?', (user_id,))
        cursor.execute('UPDATE user_progress SET added = 0 WHERE user_id = ?', (user_id,))
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


@command_router.callback_query(F.data == "start_test")
async def handle_start_test(callback: types.CallbackQuery):
    await start_test_for_user(callback.from_user.id, callback)
    await callback.answer()


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
            cursor.execute('UPDATE user_progress SET correct = correct + 1 WHERE user_id = ?', (user_id,))
        else:
            response = f"❌ Неправильно. Правильный ответ: '{test_data['correct']}'"
            cursor.execute('UPDATE user_progress SET wrong = wrong + 1 WHERE user_id = ?', (user_id,))

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
    await start_test_for_user(callback.from_user.id, callback)
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

@command_router.message(F.sticker)
async def handle_sticker(message: types.Message):
    """Обработчик стикеров"""
    await message.answer(text='😎 OMG!! It is so good sticker! 😎')


TRIGGER_WORDS = ["привет", "hi", "hello", "приветствую"]


@command_router.message(lambda message: message.text.lower() in TRIGGER_WORDS)
async def say_hi(message: types.Message):
    await message.answer(text="🤗 Hi! How are you? ^,^")


GOODBYE_WORDS = ['пока', "bye", "goodbye"]


@command_router.message(lambda message: message.text.lower() in GOODBYE_WORDS)
async def reply_goodbye(message: types.Message):
    await message.answer(text="🥺 See you! Have a nice day, Bro :)")


@command_router.message(F.text.lower().contains('thank you'))
async def reply_thanks(message: types.Message):
    await message.answer(text="🥰 You are welcome! 🥰")


@command_router.message(F.text.lower().contains("перевод"))
async def handle_translate_request(message: types.Message):
    await message.answer(text="Нажмите на кнопку, чтобы перевести слово.", reply_markup=funny_keyboard)


def close_db():
    conn.close()
