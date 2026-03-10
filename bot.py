import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
ReplyKeyboardMarkup, KeyboardButton,
InlineKeyboardMarkup, InlineKeyboardButton,
)

# ┌─────────────────────────────────────────────────────────┐

# │  НАЛАШТУВАННЯ — змініть тут                             │

# └─────────────────────────────────────────────────────────┘

TOKEN          = 8557443538:AAHwd2tcJo3RkrZ31AwpEd7Rw-4uZ08W5mg
ADMIN_ID       = 7118888508
OBSERVER_IDS   = [5936919228]

UAH_PER_STAR   = 0.75
USD_PER_STAR   = 0.025
CARD           = “5168752119088246”
TON            = “UQCy3DgiF5o2rqTrAZKAWGStfWlmxBU3RFHa-FlOlVkUnaFU”

PREM_UAH = {1: 129,  3: 349,  6: 649,  12: 1199}
PREM_TON = {1: 3.5,  3: 9.5,  6: 17.5, 12: 32.0}

REF_BONUS    = 2
MAX_REQUESTS = 5

logging.basicConfig(level=logging.INFO, format=”%(asctime)s %(levelname)s %(message)s”)

# ┌─────────────────────────────────────────────────────────┐

# │  ПЕРЕКЛАДИ                                              │

# └─────────────────────────────────────────────────────────┘

LANG = {
“uk”: {
“pick_lang”:    “🌐 Оберіть мову:”,
“welcome”:      “👋 Привіт, {name}!\n\nЛаскаво просимо до <b>Nexora Stars Bot</b> ⭐\nКупуй Telegram Stars та Premium вигідно.\n\nОбери пункт меню 👇”,
“btn_buy”:      “⭐ Купити зірки”,
“btn_bal”:      “💰 Баланс”,
“btn_wd”:       “📤 Вивід зірок”,
“btn_prem”:     “💎 Telegram Premium”,
“btn_calc”:     “🧮 Калькулятор”,
“btn_support”:  “🛟 Підтримка”,
“btn_ref”:      “👥 Реферали”,
“btn_tasks”:    “📋 Завдання”,
“btn_info”:     “ℹ️ Інформація”,
“btn_lang”:     “🌐 Мова”,
“info”: (
“📌 <b>Nexora Stars Bot</b>\n\n”
“<b>⭐ Зірки:</b>\n”
f”  • {UAH_PER_STAR} грн / зірка (ПриватБанк)\n”
f”  • ${USD_PER_STAR} / зірка (TON)\n\n”
“<b>💎 Premium:</b>\n”
“  • 1 міс  — 129 грн / 3.5 TON\n”
“  • 3 міс  — 349 грн / 9.5 TON\n”
“  • 6 міс  — 649 грн / 17.5 TON\n”
“  • 12 міс — 1199 грн / 32 TON\n\n”
f”<b>💳 ПриватБанк:</b> <code>{CARD}</code>\n”
f”<b>💎 TON:</b> <code>{TON}</code>\n\n”
“⚠️ Всі підтвердження вручну адміністратором.”
),
“bal”:          “💰 Ваш баланс: <b>{n} ⭐</b>”,
“calc_ask”:     “🧮 <b>Калькулятор</b>\n\nОбери режим:”,
“calc_stars”:   “⭐ Зірки → скільки платити”,
“calc_uah”:     “💰 Гривні → скільки зірок”,
“calc_enter_s”: “Введіть кількість зірок:”,
“calc_enter_u”: “Введіть суму в гривнях:”,
“calc_res_s”:   “⭐ <b>{s} зірок</b> = <b>{u} грн</b> або <b>${d}</b>”,
“calc_res_u”:   “💰 <b>{u} грн</b> = <b>{s} зірок</b>”,
“calc_err”:     “❌ Введіть число більше 0.”,
“ref_show”:     “👥 <b>Реферали</b>\n\nПосилання:\n<code>{link}</code>\n\nЗа кожного друга — <b>+{bonus} ⭐</b>\n\n👤 Запрошено: <b>{cnt}</b>\n🎁 Зароблено: <b>{earned} ⭐</b>”,
“ref_got”:      “🎁 +{bonus} ⭐ за нового друга! Баланс: <b>{bal} ⭐</b>”,
“ref_new”:      “👋 Вас запросив друг!”,
“sup_ask”:      “✍️ Напишіть запитання — адмін відповість тут:”,
“sup_sent”:     “✅ Надіслано! Очікуйте відповіді.”,
“sup_reply”:    “💬 <b>Відповідь підтримки:</b>\n\n{text}”,
“buy_ask”:      “Введіть кількість зірок (мін. 10):”,
“buy_cur”:      “Купуєте <b>{n} ⭐</b>\n\nОберіть спосіб оплати:”,
“buy_uah”:      “💳 <b>ПриватБанк</b>\n\n{n} ⭐ = <b>{total} грн</b>\n\nКарта: <code>{card}</code>\n\n📸 Надішліть скріншот оплати.”,
“buy_ton”:      “💎 <b>TON-гаманець</b>\n\n{n} ⭐ = <b>${total}</b>\n\nAdresa: <code>{ton}</code>\n\n📸 Надішліть скріншот.”,
“buy_confirm”:  “📋 Підтвердіть: <b>{n} ⭐</b> за <b>{total}</b> через <b>{method}</b>”,
“buy_ok”:       “✅ Скріншот отримано! Очікуйте підтвердження адміна.”,
“buy_need_pic”: “📸 Надішліть фото/скріншот платежу.”,
“buy_done”:     “✅ Підтверджено! +<b>{n} ⭐</b>. Баланс: <b>{bal} ⭐</b>”,
“buy_rej”:      “❌ Заявку відхилено. Зверніться до підтримки.”,
“wd_zero”:      “❌ Баланс нульовий.”,
“wd_ask_n”:     “Баланс: <b>{bal} ⭐</b>\n\nСкільки зірок вивести?”,
“wd_ask_u”:     “Введіть @username для отримання зірок:”,
“wd_confirm”:   “📋 Вивід <b>{n} ⭐</b> на <b>{u}</b> — підтверджуєте?”,
“wd_sent”:      “✅ Заявку надіслано адміну. Очікуйте.”,
“wd_done”:      “✅ Вивід підтверджено! Баланс: <b>{bal} ⭐</b>”,
“wd_rej”:       “❌ Вивід відхилено.”,
“wd_bad”:       “❌ Недостатньо зірок.”,
“prem_ask”:     “💎 <b>Telegram Premium</b>\n\nОберіть термін:”,
“prem_pay”:     “Термін: <b>{m} міс.</b>\n\nОберіть оплату:\n  🇺🇦 ПриватБанк: <b>{u} грн</b>\n  💎 TON: <b>{t} TON</b>”,
“prem_uah”:     “💳 Premium {m} міс. = <b>{total} грн</b>\n\nКарта: <code>{card}</code>\n\n📸 Надішліть скріншот.”,
“prem_ton”:     “💎 Premium {m} міс. = <b>{total} TON</b>\n\nTON: <code>{ton}</code>\n\n📸 Надішліть скріншот.”,
“prem_confirm”: “📋 Premium <b>{m} міс.</b> за <b>{total}</b> через <b>{method}</b> — підтверджуєте?”,
“prem_ok”:      “✅ Скріншот отримано! Після перевірки Premium буде оформлено.”,
“prem_done”:    “✅ Premium підтверджено! Буде оформлено на <b>{m} міс.</b>”,
“prem_rej”:     “❌ Заявку на Premium відхилено.”,
“yes”:          “✅ Підтверджую”,
“no”:           “❌ Скасувати”,
“cancel”:       “❌ Скасовано.”,
“menu”:         “Головне меню:”,
“spam”:         “⛔ Ліміт заявок ({max}) вичерпано. Зверніться до підтримки.”,
“mo”:           “міс.”,
“tasks_title”:  “📋 <b>Завдання</b>\n\nВиконуй завдання та отримуй зірки!\n\n”,
“tasks_empty”:  “📋 Наразі завдань немає. Заходь пізніше!”,
“task_item”:    “📌 <b>{name}</b>\n{desc}\n💰 Нагорода: <b>{reward} ⭐</b>”,
“task_done_already”: “✅ Завдання вже виконано!”,
“task_check”:   “🔍 Перевіряємо підписку…”,
“task_ok”:      “✅ Завдання виконано! +<b>{reward} ⭐</b>. Баланс: <b>{bal} ⭐</b>”,
“task_fail”:    “❌ Ви ще не підписались на канал. Підпишіться і натисніть «Перевірити».”,
“task_go”:      “👉 Перейти”,
“task_verify”:  “✅ Перевірити”,
“stats”:        (
“📊 <b>Статистика</b>\n\n”
“👤 Юзерів: <b>{u}</b>\n”
“🛒 Покупок: <b>{b}</b>\n”
“📤 Виводів: <b>{w}</b>\n”
“💎 Premium: <b>{p}</b>\n”
“📋 Завдань виконано: <b>{td}</b>\n”
“👥 Рефералів: <b>{r}</b>\n”
“⭐ Реф. зірок: <b>{rs}</b>\n\n”
“💰 Виручка грн: <b>{rev_uah} грн</b>\n”
“💎 Виручка TON: <b>{rev_ton} TON</b>”
),
},
“ru”: {
“pick_lang”:    “🌐 Выберите язык:”,
“welcome”:      “👋 Привет, {name}!\n\nДобро пожаловать в <b>Nexora Stars Bot</b> ⭐\nПокупай Telegram Stars и Premium выгодно.\n\nВыбери пункт меню 👇”,
“btn_buy”:      “⭐ Купить звёзды”,
“btn_bal”:      “💰 Баланс”,
“btn_wd”:       “📤 Вывод звёзд”,
“btn_prem”:     “💎 Telegram Premium”,
“btn_calc”:     “🧮 Калькулятор”,
“btn_support”:  “🛟 Поддержка”,
“btn_ref”:      “👥 Рефералы”,
“btn_tasks”:    “📋 Задания”,
“btn_info”:     “ℹ️ Информация”,
“btn_lang”:     “🌐 Язык”,
“info”: (
“📌 <b>Nexora Stars Bot</b>\n\n”
“<b>⭐ Звёзды:</b>\n”
f”  • {UAH_PER_STAR} грн / звезда (ПриватБанк)\n”
f”  • ${USD_PER_STAR} / звезда (TON)\n\n”
“<b>💎 Premium:</b>\n”
“  • 1 мес  — 129 грн / 3.5 TON\n”
“  • 3 мес  — 349 грн / 9.5 TON\n”
“  • 6 мес  — 649 грн / 17.5 TON\n”
“  • 12 мес — 1199 грн / 32 TON\n\n”
f”<b>💳 ПриватБанк:</b> <code>{CARD}</code>\n”
f”<b>💎 TON:</b> <code>{TON}</code>\n\n”
“⚠️ Все подтверждения вручную администратором.”
),
“bal”:          “💰 Ваш баланс: <b>{n} ⭐</b>”,
“calc_ask”:     “🧮 <b>Калькулятор</b>\n\nВыбери режим:”,
“calc_stars”:   “⭐ Звёзды → сколько платить”,
“calc_uah”:     “💰 Гривны → сколько звёзд”,
“calc_enter_s”: “Введите количество звёзд:”,
“calc_enter_u”: “Введите сумму в гривнах:”,
“calc_res_s”:   “⭐ <b>{s} звёзд</b> = <b>{u} грн</b> или <b>${d}</b>”,
“calc_res_u”:   “💰 <b>{u} грн</b> = <b>{s} звёзд</b>”,
“calc_err”:     “❌ Введите число больше 0.”,
“ref_show”:     “👥 <b>Рефералы</b>\n\nСсылка:\n<code>{link}</code>\n\nЗа каждого друга — <b>+{bonus} ⭐</b>\n\n👤 Приглашено: <b>{cnt}</b>\n🎁 Заработано: <b>{earned} ⭐</b>”,
“ref_got”:      “🎁 +{bonus} ⭐ за нового друга! Баланс: <b>{bal} ⭐</b>”,
“ref_new”:      “👋 Вас пригласил друг!”,
“sup_ask”:      “✍️ Напишите вопрос — админ ответит здесь:”,
“sup_sent”:     “✅ Отправлено! Ожидайте ответа.”,
“sup_reply”:    “💬 <b>Ответ поддержки:</b>\n\n{text}”,
“buy_ask”:      “Введите количество звёзд (мин. 10):”,
“buy_cur”:      “Покупаете <b>{n} ⭐</b>\n\nВыберите способ оплаты:”,
“buy_uah”:      “💳 <b>ПриватБанк</b>\n\n{n} ⭐ = <b>{total} грн</b>\n\nКарта: <code>{card}</code>\n\n📸 Отправьте скриншот оплаты.”,
“buy_ton”:      “💎 <b>TON-кошелёк</b>\n\n{n} ⭐ = <b>${total}</b>\n\nАдрес: <code>{ton}</code>\n\n📸 Отправьте скриншот.”,
“buy_confirm”:  “📋 Подтвердите: <b>{n} ⭐</b> за <b>{total}</b> через <b>{method}</b>”,
“buy_ok”:       “✅ Скриншот получен! Ожидайте подтверждения.”,
“buy_need_pic”: “📸 Отправьте фото/скриншот платежа.”,
“buy_done”:     “✅ Подтверждено! +<b>{n} ⭐</b>. Баланс: <b>{bal} ⭐</b>”,
“buy_rej”:      “❌ Заявка отклонена. Обратитесь в поддержку.”,
“wd_zero”:      “❌ Баланс нулевой.”,
“wd_ask_n”:     “Баланс: <b>{bal} ⭐</b>\n\nСколько звёзд вывести?”,
“wd_ask_u”:     “Введите @username для получения звёзд:”,
“wd_confirm”:   “📋 Вывод <b>{n} ⭐</b> на <b>{u}</b> — подтверждаете?”,
“wd_sent”:      “✅ Заявка отправлена. Ожидайте.”,
“wd_done”:      “✅ Вывод подтверждён! Баланс: <b>{bal} ⭐</b>”,
“wd_rej”:       “❌ Вывод отклонён.”,
“wd_bad”:       “❌ Недостаточно звёзд.”,
“prem_ask”:     “💎 <b>Telegram Premium</b>\n\nВыберите срок:”,
“prem_pay”:     “Срок: <b>{m} мес.</b>\n\nВыберите оплату:\n  🇺🇦 ПриватБанк: <b>{u} грн</b>\n  💎 TON: <b>{t} TON</b>”,
“prem_uah”:     “💳 Premium {m} мес. = <b>{total} грн</b>\n\nКарта: <code>{card}</code>\n\n📸 Отправьте скриншот.”,
“prem_ton”:     “💎 Premium {m} мес. = <b>{total} TON</b>\n\nTON: <code>{ton}</code>\n\n📸 Отправьте скриншот.”,
“prem_confirm”: “📋 Premium <b>{m} мес.</b> за <b>{total}</b> через <b>{method}</b> — подтверждаете?”,
“prem_ok”:      “✅ Скриншот получен! После проверки Premium будет оформлен.”,
“prem_done”:    “✅ Premium подтверждён! Будет оформлен на <b>{m} мес.</b>”,
“prem_rej”:     “❌ Заявка на Premium отклонена.”,
“yes”:          “✅ Подтверждаю”,
“no”:           “❌ Отмена”,
“cancel”:       “❌ Отменено.”,
“menu”:         “Главное меню:”,
“spam”:         “⛔ Лимит заявок ({max}) исчерпан. Обратитесь в поддержку.”,
“mo”:           “мес.”,
“tasks_title”:  “📋 <b>Задания</b>\n\nВыполняй задания и получай звёзды!\n\n”,
“tasks_empty”:  “📋 Заданий пока нет. Заходи позже!”,
“task_item”:    “📌 <b>{name}</b>\n{desc}\n💰 Награда: <b>{reward} ⭐</b>”,
“task_done_already”: “✅ Задание уже выполнено!”,
“task_check”:   “🔍 Проверяем подписку…”,
“task_ok”:      “✅ Задание выполнено! +<b>{reward} ⭐</b>. Баланс: <b>{bal} ⭐</b>”,
“task_fail”:    “❌ Вы ещё не подписались на канал. Подпишитесь и нажмите «Проверить».”,
“task_go”:      “👉 Перейти”,
“task_verify”:  “✅ Проверить”,
“stats”:        (
“📊 <b>Статистика</b>\n\n”
“👤 Юзеров: <b>{u}</b>\n”
“🛒 Покупок: <b>{b}</b>\n”
“📤 Выводов: <b>{w}</b>\n”
“💎 Premium: <b>{p}</b>\n”
“📋 Заданий выполнено: <b>{td}</b>\n”
“👥 Рефералов: <b>{r}</b>\n”
“⭐ Реф. звёзд: <b>{rs}</b>\n\n”
“💰 Выручка грн: <b>{rev_uah} грн</b>\n”
“💎 Выручка TON: <b>{rev_ton} TON</b>”
),
},
“en”: {
“pick_lang”:    “🌐 Choose language:”,
“welcome”:      “👋 Hello, {name}!\n\nWelcome to <b>Nexora Stars Bot</b> ⭐\nBuy Telegram Stars and Premium at great prices.\n\nChoose a menu item 👇”,
“btn_buy”:      “⭐ Buy Stars”,
“btn_bal”:      “💰 Balance”,
“btn_wd”:       “📤 Withdraw Stars”,
“btn_prem”:     “💎 Telegram Premium”,
“btn_calc”:     “🧮 Calculator”,
“btn_support”:  “🛟 Support”,
“btn_ref”:      “👥 Referrals”,
“btn_tasks”:    “📋 Tasks”,
“btn_info”:     “ℹ️ Information”,
“btn_lang”:     “🌐 Language”,
“info”: (
“📌 <b>Nexora Stars Bot</b>\n\n”
“<b>⭐ Stars:</b>\n”
f”  • {UAH_PER_STAR} UAH / star (PrivatBank)\n”
f”  • ${USD_PER_STAR} / star (TON)\n\n”
“<b>💎 Premium:</b>\n”
“  • 1 mo  — 129 UAH / 3.5 TON\n”
“  • 3 mo  — 349 UAH / 9.5 TON\n”
“  • 6 mo  — 649 UAH / 17.5 TON\n”
“  • 12 mo — 1199 UAH / 32 TON\n\n”
f”<b>💳 PrivatBank:</b> <code>{CARD}</code>\n”
f”<b>💎 TON:</b> <code>{TON}</code>\n\n”
“⚠️ All confirmations are done manually by admin.”
),
“bal”:          “💰 Your balance: <b>{n} ⭐</b>”,
“calc_ask”:     “🧮 <b>Calculator</b>\n\nChoose mode:”,
“calc_stars”:   “⭐ Stars → how much to pay”,
“calc_uah”:     “💰 UAH → how many stars”,
“calc_enter_s”: “Enter number of stars:”,
“calc_enter_u”: “Enter amount in UAH:”,
“calc_res_s”:   “⭐ <b>{s} stars</b> = <b>{u} UAH</b> or <b>${d}</b>”,
“calc_res_u”:   “💰 <b>{u} UAH</b> = <b>{s} stars</b>”,
“calc_err”:     “❌ Enter a number greater than 0.”,
“ref_show”:     “👥 <b>Referrals</b>\n\nYour link:\n<code>{link}</code>\n\nFor each friend — <b>+{bonus} ⭐</b>\n\n👤 Invited: <b>{cnt}</b>\n🎁 Earned: <b>{earned} ⭐</b>”,
“ref_got”:      “🎁 +{bonus} ⭐ for a new friend! Balance: <b>{bal} ⭐</b>”,
“ref_new”:      “👋 You were invited by a friend!”,
“sup_ask”:      “✍️ Write your question — admin will reply here:”,
“sup_sent”:     “✅ Sent! Wait for a reply.”,
“sup_reply”:    “💬 <b>Support reply:</b>\n\n{text}”,
“buy_ask”:      “Enter number of stars (min. 10):”,
“buy_cur”:      “Buying <b>{n} ⭐</b>\n\nChoose payment method:”,
“buy_uah”:      “💳 <b>PrivatBank</b>\n\n{n} ⭐ = <b>{total} UAH</b>\n\nCard: <code>{card}</code>\n\n📸 Send payment screenshot.”,
“buy_ton”:      “💎 <b>TON wallet</b>\n\n{n} ⭐ = <b>${total}</b>\n\nAddress: <code>{ton}</code>\n\n📸 Send screenshot.”,
“buy_confirm”:  “📋 Confirm: <b>{n} ⭐</b> for <b>{total}</b> via <b>{method}</b>”,
“buy_ok”:       “✅ Screenshot received! Wait for admin confirmation.”,
“buy_need_pic”: “📸 Please send a photo/screenshot of payment.”,
“buy_done”:     “✅ Confirmed! +<b>{n} ⭐</b>. Balance: <b>{bal} ⭐</b>”,
“buy_rej”:      “❌ Request rejected. Contact support.”,
“wd_zero”:      “❌ Balance is zero.”,
“wd_ask_n”:     “Balance: <b>{bal} ⭐</b>\n\nHow many stars to withdraw?”,
“wd_ask_u”:     “Enter @username to receive stars:”,
“wd_confirm”:   “📋 Withdraw <b>{n} ⭐</b> to <b>{u}</b> — confirm?”,
“wd_sent”:      “✅ Request sent to admin. Wait.”,
“wd_done”:      “✅ Withdrawal confirmed! Balance: <b>{bal} ⭐</b>”,
“wd_rej”:       “❌ Withdrawal rejected.”,
“wd_bad”:       “❌ Not enough stars.”,
“prem_ask”:     “💎 <b>Telegram Premium</b>\n\nChoose period:”,
“prem_pay”:     “Period: <b>{m} mo.</b>\n\nChoose payment:\n  🇺🇦 PrivatBank: <b>{u} UAH</b>\n  💎 TON: <b>{t} TON</b>”,
“prem_uah”:     “💳 Premium {m} mo. = <b>{total} UAH</b>\n\nCard: <code>{card}</code>\n\n📸 Send screenshot.”,
“prem_ton”:     “💎 Premium {m} mo. = <b>{total} TON</b>\n\nTON: <code>{ton}</code>\n\n📸 Send screenshot.”,
“prem_confirm”: “📋 Premium <b>{m} mo.</b> for <b>{total}</b> via <b>{method}</b> — confirm?”,
“prem_ok”:      “✅ Screenshot received! Premium will be activated after review.”,
“prem_done”:    “✅ Premium confirmed! Will be activated for <b>{m} mo.</b>”,
“prem_rej”:     “❌ Premium request rejected.”,
“yes”:          “✅ Confirm”,
“no”:           “❌ Cancel”,
“cancel”:       “❌ Cancelled.”,
“menu”:         “Main menu:”,
“spam”:         “⛔ Request limit ({max}) reached. Contact support.”,
“mo”:           “mo.”,
“tasks_title”:  “📋 <b>Tasks</b>\n\nComplete tasks and earn stars!\n\n”,
“tasks_empty”:  “📋 No tasks available right now. Come back later!”,
“task_item”:    “📌 <b>{name}</b>\n{desc}\n💰 Reward: <b>{reward} ⭐</b>”,
“task_done_already”: “✅ Task already completed!”,
“task_check”:   “🔍 Checking subscription…”,
“task_ok”:      “✅ Task completed! +<b>{reward} ⭐</b>. Balance: <b>{bal} ⭐</b>”,
“task_fail”:    “❌ You haven’t subscribed to the channel yet. Subscribe and press «Verify».”,
“task_go”:      “👉 Go”,
“task_verify”:  “✅ Verify”,
“stats”:        (
“📊 <b>Statistics</b>\n\n”
“👤 Users: <b>{u}</b>\n”
“🛒 Purchases: <b>{b}</b>\n”
“📤 Withdrawals: <b>{w}</b>\n”
“💎 Premium: <b>{p}</b>\n”
“📋 Tasks done: <b>{td}</b>\n”
“👥 Referrals: <b>{r}</b>\n”
“⭐ Ref. stars: <b>{rs}</b>\n\n”
“💰 Revenue UAH: <b>{rev_uah} UAH</b>\n”
“💎 Revenue TON: <b>{rev_ton} TON</b>”
),
},
}

def T(uid, key, **kw):
l = langs.get(uid, “uk”)
s = LANG[l].get(key, LANG[“uk”].get(key, key))
return s.format(**kw) if kw else s
[10.03.2026 18:37] Nexorik: # ┌─────────────────────────────────────────────────────────┐

# │  ПАМ’ЯТЬ                                                │

# └─────────────────────────────────────────────────────────┘

langs        = {}   # uid → “uk”/“ru”/“en”
stars        = {}   # uid → int
ref_by       = {}   # uid → referrer_uid
ref_cnt      = {}   # uid → скільки запросив
ref_earn     = {}   # uid → зірок від рефералів
req_cnt      = {}   # uid → заявок за сесію
pending_buy  = {}   # key → dict
pending_wd   = {}   # key → dict
pending_prm  = {}   # key → dict

# Завдання: tasks[task_id] = {name, desc, link, channel_id, reward, active}

tasks        = {}
task_counter = 0

# Виконані завдання: done_tasks[uid] = set of task_ids

done_tasks   = {}

stat_b = stat_w = stat_p = stat_td = 0
rev_uah = 0.0   # виручка в гривнях
rev_ton = 0.0   # виручка в TON

def bal(uid):      return stars.get(uid, 0)
def add(uid, n):   stars[uid] = stars.get(uid, 0) + n
def sub(uid, n):   stars[uid] = max(0, stars.get(uid, 0) - n)

def spam_ok(uid):
req_cnt[uid] = req_cnt.get(uid, 0) + 1
return req_cnt[uid] <= MAX_REQUESTS

# ┌─────────────────────────────────────────────────────────┐

# │  FSM                                                    │

# └─────────────────────────────────────────────────────────┘

class S:
class Lang(StatesGroup):
pick = State()
class Buy(StatesGroup):
amount = State()
cur    = State()
conf   = State()
photo  = State()
class Wd(StatesGroup):
amount = State()
user   = State()
conf   = State()
class Prem(StatesGroup):
period = State()
pay    = State()
conf   = State()
photo  = State()
class Calc(StatesGroup):
mode  = State()
value = State()
class Sup(StatesGroup):
msg = State()
class AdminReply(StatesGroup):
msg = State()
class Broadcast(StatesGroup):
content = State()
confirm = State()
class AddTask(StatesGroup):
name    = State()
desc    = State()
link    = State()
channel = State()
reward  = State()

# ┌─────────────────────────────────────────────────────────┐

# │  БОТ                                                    │

# └─────────────────────────────────────────────────────────┘

bot = Bot(token=TOKEN)
dp  = Dispatcher(storage=MemoryStorage())

# ┌─────────────────────────────────────────────────────────┐

# │  КЛАВІАТУРИ                                             │

# └─────────────────────────────────────────────────────────┘

def menu_kb(uid):
l = langs.get(uid, “uk”)
b = lambda k: KeyboardButton(text=LANG[l][k])
return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
[b(“btn_buy”),     b(“btn_bal”)],
[b(“btn_wd”),      b(“btn_prem”)],
[b(“btn_calc”),    b(“btn_support”)],
[b(“btn_ref”),     b(“btn_tasks”)],
[b(“btn_info”),    b(“btn_lang”)],
])

def lang_kb():
return InlineKeyboardMarkup(inline_keyboard=[[
InlineKeyboardButton(text=“🇺🇦 Укр”, callback_data=“L_uk”),
InlineKeyboardButton(text=“🇷🇺 Рус”, callback_data=“L_ru”),
InlineKeyboardButton(text=“🇬🇧 Eng”, callback_data=“L_en”),
]])

def yn_kb(uid):
return InlineKeyboardMarkup(inline_keyboard=[[
InlineKeyboardButton(text=T(uid,“yes”), callback_data=“YES”),
InlineKeyboardButton(text=T(uid,“no”),  callback_data=“NO”),
]])

def cur_kb(uid):
return InlineKeyboardMarkup(inline_keyboard=[
[InlineKeyboardButton(text=“🇺🇦 ПриватБанк (грн)”, callback_data=“C_uah”),
InlineKeyboardButton(text=“💎 TON ($)”,            callback_data=“C_ton”)],
[InlineKeyboardButton(text=T(uid,“no”), callback_data=“NO”)],
])

def calc_kb(uid):
return InlineKeyboardMarkup(inline_keyboard=[
[InlineKeyboardButton(text=T(uid,“calc_stars”), callback_data=“CALC_s”)],
[InlineKeyboardButton(text=T(uid,“calc_uah”),   callback_data=“CALC_u”)],
[InlineKeyboardButton(text=T(uid,“no”),         callback_data=“NO”)],
])

def period_kb(uid):
mo = T(uid,“mo”)
return InlineKeyboardMarkup(inline_keyboard=[
[InlineKeyboardButton(text=f”1 {mo}”,  callback_data=“P_1”),
InlineKeyboardButton(text=f”3 {mo}”,  callback_data=“P_3”)],
[InlineKeyboardButton(text=f”6 {mo}”,  callback_data=“P_6”),
InlineKeyboardButton(text=f”12 {mo}”, callback_data=“P_12”)],
[InlineKeyboardButton(text=T(uid,“no”), callback_data=“NO”)],
])
[10.03.2026 18:37] Nexorik: def ppay_kb(uid):
return InlineKeyboardMarkup(inline_keyboard=[
[InlineKeyboardButton(text=“🇺🇦 ПриватБанк”, callback_data=“PP_uah”),
InlineKeyboardButton(text=“💎 TON”,          callback_data=“PP_ton”)],
[InlineKeyboardButton(text=T(uid,“no”),        callback_data=“NO”)],
])

def adm_kb(key, kind):
return InlineKeyboardMarkup(inline_keyboard=[[
InlineKeyboardButton(text=“✅ Підтвердити”, callback_data=f”OK_{kind}*{key}”),
InlineKeyboardButton(text=“❌ Відхилити”,  callback_data=f”NO*{kind}_{key}”),
]])

def rep_kb(uid):
return InlineKeyboardMarkup(inline_keyboard=[[
InlineKeyboardButton(text=“↩️ Відповісти”, callback_data=f”REP_{uid}”),
]])

def tasks_kb(uid, task_list):
“”“Keyboard with tasks buttons (up to 3 active tasks)”””
rows = []
for tid, t in task_list:
done = tid in done_tasks.get(uid, set())
if done:
rows.append([InlineKeyboardButton(text=f”✅ {t[‘name’]}”, callback_data=f”TK_done_{tid}”)])
else:
rows.append([
InlineKeyboardButton(text=f”👉 {t[‘name’]}”, url=t[“link”]),
InlineKeyboardButton(text=“✅ Перевірити”, callback_data=f”TK_check_{tid}”),
])
return InlineKeyboardMarkup(inline_keyboard=rows) if rows else None

def task_admin_kb(tid):
return InlineKeyboardMarkup(inline_keyboard=[[
InlineKeyboardButton(text=“✅ Увімкнути”,  callback_data=f”TA_on_{tid}”),
InlineKeyboardButton(text=“❌ Вимкнути”,   callback_data=f”TA_off_{tid}”),
InlineKeyboardButton(text=“🗑 Видалити”,   callback_data=f”TA_del_{tid}”),
]])

# ┌─────────────────────────────────────────────────────────┐

# │  HELPERS                                                │

# └─────────────────────────────────────────────────────────┘

async def obs(text, photo=None):
for oid in OBSERVER_IDS:
try:
if photo: await bot.send_photo(oid, photo=photo, caption=text, parse_mode=“HTML”)
else:     await bot.send_message(oid, text, parse_mode=“HTML”)
except: pass

def menu(uid):  return menu_kb(uid)
def mn(uid):    return T(uid, “menu”)

def get_active_tasks_for_user(uid):
“”“Get up to 3 active tasks, rotating when all done”””
active = [(tid, t) for tid, t in tasks.items() if t[“active”]]
if not active:
return []
user_done = done_tasks.get(uid, set())
# Tasks not yet done by this user
not_done = [(tid, t) for tid, t in active if tid not in user_done]
if not_done:
return not_done[:3]
# All done — show all active (marked as done)
return active[:3]

# ┌─────────────────────────────────────────────────────────┐

# │  /start — ВИБІР МОВИ при першому запуску                │

# └─────────────────────────────────────────────────────────┘

@dp.message(Command(“start”))
async def cmd_start(msg: types.Message, state: FSMContext):
await state.clear()
uid  = msg.from_user.id
args = msg.text.split()
ref  = args[1] if len(args) > 1 else “”
await state.update_data(ref=ref)
if uid not in langs:
await state.set_state(S.Lang.pick)
await msg.answer(“🌐 <b>Оберіть мову / Choose language / Выберите язык:</b>”,
reply_markup=lang_kb(), parse_mode=“HTML”)
else:
await _go(msg, state, uid)

async def *go(msg, state, uid):
data = await state.get_data()
ref  = data.get(“ref”, “”)
await state.clear()
if ref.startswith(“ref*”) and uid not in ref_by:
try:
rv = int(ref[4:])
if rv != uid:
ref_by[uid]  = rv
ref_cnt[rv]  = ref_cnt.get(rv, 0) + 1
ref_earn[rv] = ref_earn.get(rv, 0) + REF_BONUS
add(rv, REF_BONUS)
try:
await bot.send_message(rv, T(rv,“ref_got”,bonus=REF_BONUS,bal=bal(rv)), parse_mode=“HTML”)
except: pass
await msg.answer(T(uid,“ref_new”))
except: pass
# Notify admin on new user start
if uid not in langs:
    try:
        uname = msg.from_user.username or "—"
        name  = msg.from_user.full_name
        await bot.send_message(ADMIN_ID,
            f"👤 <b>Новий користувач!</b>\n{name} (@{uname})\n🆔 <code>{uid}</code>",
            parse_mode="HTML")
    except: pass

name = msg.from_user.first_name or "друг"
await msg.answer(T(uid,"welcome",name=name), reply_markup=menu(uid), parse_mode="HTML")

@dp.callback_query(S.Lang.pick, F.data.startswith(“L_”))
async def pick_lang_start(cb: types.CallbackQuery, state: FSMContext):
uid = cb.from_user.id
langs[uid] = cb.data[2:]
await cb.message.
[10.03.2026 18:37] Nexorik: delete()
await cb.answer()
await _go(cb.message, state, uid)

@dp.callback_query(F.data.startswith(“L_”))
async def change_lang(cb: types.CallbackQuery, state: FSMContext):
uid = cb.from_user.id
langs[uid] = cb.data[2:]
await state.clear()
await cb.message.delete()
name = cb.from_user.first_name or “друг”
await bot.send_message(uid, T(uid,“welcome”,name=name), reply_markup=menu(uid), parse_mode=“HTML”)
await cb.answer()

ALL_LANG_BTNS = [“🌐 Мова”,“🌐 Язык”,“🌐 Language”]
@dp.message(lambda m: m.text in ALL_LANG_BTNS)
async def lang_menu(msg: types.Message, state: FSMContext):
await state.clear()
await msg.answer(“🌐 <b>Оберіть мову / Choose language / Выберите язык:</b>”,
reply_markup=lang_kb(), parse_mode=“HTML”)

@dp.callback_query(F.data == “NO”)
async def no_cb(cb: types.CallbackQuery, state: FSMContext):
uid = cb.from_user.id
await state.clear()
await cb.message.edit_text(T(uid,“cancel”))
await bot.send_message(uid, mn(uid), reply_markup=menu(uid))
await cb.answer()

# ┌─────────────────────────────────────────────────────────┐

# │  INFO                                                   │

# └─────────────────────────────────────────────────────────┘

INFO_BTNS = [“ℹ️ Інформація”,“ℹ️ Информация”,“ℹ️ Information”]
@dp.message(lambda m: m.text in INFO_BTNS)
async def info_h(msg: types.Message):
await msg.answer(T(msg.from_user.id,“info”), parse_mode=“HTML”)

# ┌─────────────────────────────────────────────────────────┐

# │  БАЛАНС                                                 │

# └─────────────────────────────────────────────────────────┘

BAL_BTNS = [“💰 Баланс”,“💰 Balance”]
@dp.message(lambda m: m.text in BAL_BTNS)
async def bal_h(msg: types.Message):
uid = msg.from_user.id
await msg.answer(T(uid,“bal”,n=bal(uid)), parse_mode=“HTML”)

# ┌─────────────────────────────────────────────────────────┐

# │  КАЛЬКУЛЯТОР                                            │

# └─────────────────────────────────────────────────────────┘

CALC_BTNS = [“🧮 Калькулятор”,“🧮 Calculator”]
@dp.message(lambda m: m.text in CALC_BTNS)
async def calc_h(msg: types.Message, state: FSMContext):
uid = msg.from_user.id
await state.set_state(S.Calc.mode)
await msg.answer(T(uid,“calc_ask”), reply_markup=calc_kb(uid), parse_mode=“HTML”)

@dp.callback_query(S.Calc.mode, F.data.in_({“CALC_s”,“CALC_u”}))
async def calc_mode(cb: types.CallbackQuery, state: FSMContext):
uid = cb.from_user.id
m   = cb.data
await state.update_data(m=m)
await state.set_state(S.Calc.value)
txt = T(uid,“calc_enter_s”) if m==“CALC_s” else T(uid,“calc_enter_u”)
await cb.message.edit_text(txt)
await cb.answer()

@dp.message(S.Calc.value)
async def calc_val(msg: types.Message, state: FSMContext):
uid = msg.from_user.id
d   = await state.get_data()
try:
v = float((msg.text or “”).replace(”,”,”.”))
assert v > 0
except:
await msg.answer(T(uid,“calc_err”)); return
await state.clear()
if d[“m”] == “CALC_s”:
s = int(v)
await msg.answer(T(uid,“calc_res_s”, s=s, u=round(s*UAH_PER_STAR,2), d=round(s*USD_PER_STAR,4)),
reply_markup=menu(uid), parse_mode=“HTML”)
else:
await msg.answer(T(uid,“calc_res_u”, u=round(v,2), s=int(v/UAH_PER_STAR)),
reply_markup=menu(uid), parse_mode=“HTML”)

# ┌─────────────────────────────────────────────────────────┐

# │  РЕФЕРАЛИ                                               │

# └─────────────────────────────────────────────────────────┘

REF_BTNS = [“👥 Реферали”,“👥 Рефералы”,“👥 Referrals”]
@dp.message(lambda m: m.text in REF_BTNS)
async def ref_h(msg: types.Message):
uid = msg.from_user.id
me  = await bot.get_me()
lnk = f”https://t.me/{me.username}?start=ref_{uid}”
await msg.answer(T(uid,“ref_show”,link=lnk,bonus=REF_BONUS,
cnt=ref_cnt.get(uid,0),earned=ref_earn.get(uid,0)), parse_mode=“HTML”)

# ┌─────────────────────────────────────────────────────────┐

# │  ПІДТРИМКА                                              │

# └─────────────────────────────────────────────────────────┘

SUP_BTNS = [“🛟 Підтримка”,“🛟 Поддержка”,“🛟 Support”]
@dp.message(lambda m: m.text in SUP_BTNS)
async def sup_h(msg: types.Message, state: FSMContext):
uid = msg.from_user.
id
await state.set_state(S.Sup.msg)
await msg.answer(T(uid,“sup_ask”))

@dp.message(S.Sup.msg)
async def sup_msg(msg: types.Message, state: FSMContext):
uid   = msg.from_user.id
uname = msg.from_user.username or “—”
name  = msg.from_user.full_name
txt = (f”🛟 <b>Підтримка</b>\n\n👤 {name} (@{uname})\n”
f”🆔 <code>{uid}</code>\n\n💬 {msg.text}”)
await bot.send_message(ADMIN_ID, txt, reply_markup=rep_kb(uid), parse_mode=“HTML”)
await obs(txt)
await state.clear()
await msg.answer(T(uid,“sup_sent”), reply_markup=menu(uid))

@dp.callback_query(F.data.startswith(“REP_”))
async def rep_click(cb: types.CallbackQuery, state: FSMContext):
if cb.from_user.id != ADMIN_ID:
await cb.answer(“⛔”, show_alert=True); return
tuid = int(cb.data[4:])
await state.set_state(S.AdminReply.msg)
await state.update_data(tuid=tuid)
await cb.message.answer(f”✍️ Відповідь для <code>{tuid}</code>:”, parse_mode=“HTML”)
await cb.answer()

@dp.message(S.AdminReply.msg)
async def rep_send(msg: types.Message, state: FSMContext):
if msg.from_user.id != ADMIN_ID: return
d = await state.get_data()
await state.clear()
tuid = d[“tuid”]
try:
await bot.send_message(tuid, T(tuid,“sup_reply”,text=msg.text), parse_mode=“HTML”)
await msg.answer(“✅ Надіслано.”)
except Exception as e:
await msg.answer(f”❌ {e}”)

# ┌─────────────────────────────────────────────────────────┐

# │  КУПИТИ ЗІРКИ                                           │

# └─────────────────────────────────────────────────────────┘

BUY_BTNS = [“⭐ Купити зірки”,“⭐ Купить звёзды”,“⭐ Buy Stars”]
@dp.message(lambda m: m.text in BUY_BTNS)
async def buy_h(msg: types.Message, state: FSMContext):
uid = msg.from_user.id
await state.set_state(S.Buy.amount)
await msg.answer(T(uid,“buy_ask”))

@dp.message(S.Buy.amount)
async def buy_amount(msg: types.Message, state: FSMContext):
uid = msg.from_user.id
if not (msg.text or “”).isdigit() or int(msg.text) < 10:
await msg.answer(T(uid,“buy_ask”)); return
n = int(msg.text)
await state.update_data(n=n)
await state.set_state(S.Buy.cur)
await msg.answer(T(uid,“buy_cur”,n=n), reply_markup=cur_kb(uid), parse_mode=“HTML”)

@dp.callback_query(S.Buy.cur, F.data.in_({“C_uah”,“C_ton”}))
async def buy_cur_cb(cb: types.CallbackQuery, state: FSMContext):
uid = cb.from_user.id
d   = await state.get_data()
n   = d[“n”]
c   = cb.data
if c == “C_uah”:
total   = round(n * UAH_PER_STAR, 2)
total_s = f”{total} грн”
meth    = “ПриватБанк”
else:
total   = round(n * USD_PER_STAR, 4)
total_s = f”${total}”
meth    = “TON”
await state.update_data(c=c, total=total, total_s=total_s, meth=meth)
await state.set_state(S.Buy.conf)
await cb.message.edit_text(
T(uid,“buy_confirm”,n=n,total=total_s,method=meth),
reply_markup=yn_kb(uid), parse_mode=“HTML”
)
await cb.answer()

@dp.callback_query(S.Buy.conf, F.data == “YES”)
async def buy_yes(cb: types.CallbackQuery, state: FSMContext):
uid = cb.from_user.id
if not spam_ok(uid):
await state.clear()
await cb.message.edit_text(T(uid,“spam”,max=MAX_REQUESTS), parse_mode=“HTML”)
await cb.answer(); return
d = await state.get_data()
if d[“c”] == “C_uah”:
txt = T(uid,“buy_uah”, n=d[“n”], total=d[“total”], card=CARD)
else:
txt = T(uid,“buy_ton”, n=d[“n”], total=d[“total”], ton=TON)
await state.set_state(S.Buy.photo)
await cb.message.edit_text(txt, parse_mode=“HTML”)
await cb.answer()

@dp.message(S.Buy.photo, F.photo)
async def buy_photo(msg: types.Message, state: FSMContext):
global stat_b, rev_uah, rev_ton
uid   = msg.from_user.id
d     = await state.get_data()
uname = msg.from_user.username or “—”
name  = msg.from_user.full_name
key   = f”b_{uid}_{msg.message_id}”
pending_buy[key] = {“uid”: uid, “n”: d[“n”], “c”: d[“c”], “total”: d[“total”]}
stat_b += 1
adm = (f”🛒 <b>Купівля зірок</b>\n👤 {name} (@{uname})\n”
f”🆔 <code>{uid}</code>\n⭐ <b>{d[‘n’]}</b> | 💰 <b>{d[‘total_s’]}</b>”)
await bot.send_photo(ADMIN_ID, photo=msg.photo[-1].file_id,
caption=adm, reply_markup=adm_kb(key,“b”), parse_mode=“HTML”)
await obs(adm, msg.photo[-1].file_id)
await state.clear()
await msg.answer(T(uid,“buy_ok”), reply_markup=menu(uid))

@dp.message(S.Buy.photo)
async def buy_nophoto(msg: types.Message):
await msg.answer(T(msg.from_user.id,“buy_need_pic”), parse_mode=“HTML”)

# ┌─────────────────────────────────────────────────────────┐

# │  ВИВІД ЗІРОК                                            │

# └─────────────────────────────────────────────────────────┘

WD_BTNS = [“📤 Вивід зірок”,“📤 Вывод звёзд”,“📤 Withdraw Stars”]
@dp.message(lambda m: m.text in WD_BTNS)
async def wd_h(msg: types.Message, state: FSMContext):
uid = msg.from_user.id
if bal(uid) == 0:
await msg.answer(T(uid,“wd_zero”)); return
await state.set_state(S.Wd.amount)
await msg.answer(T(uid,“wd_ask_n”,bal=bal(uid)), parse_mode=“HTML”)

@dp.message(S.Wd.amount)
async def wd_amount(msg: types.Message, state: FSMContext):
uid = msg.from_user.id
if not (msg.text or “”).isdigit():
await msg.answer(T(uid,“calc_err”)); return
n = int(msg.text)
if n <= 0 or n > bal(uid):
await msg.answer(T(uid,“wd_bad”), parse_mode=“HTML”); return
await state.update_data(n=n)
await state.set_state(S.Wd.user)
await msg.answer(T(uid,“wd_ask_u”))

@dp.message(S.Wd.user)
async def wd_user(msg: types.Message, state: FSMContext):
uid = msg.from_user.id
u   = msg.text.strip()
d   = await state.get_data()
await state.update_data(u=u)
await state.set_state(S.Wd.conf)
await msg.answer(T(uid,“wd_confirm”,n=d[“n”],u=u), reply_markup=yn_kb(uid), parse_mode=“HTML”)

@dp.callback_query(S.Wd.conf, F.data == “YES”)
async def wd_yes(cb: types.CallbackQuery, state: FSMContext):
global stat_w
uid   = cb.from_user.id
if not spam_ok(uid):
await state.clear()
await cb.message.edit_text(T(uid,“spam”,max=MAX_REQUESTS), parse_mode=“HTML”)
await cb.answer(); return
d     = await state.get_data()
uname = cb.from_user.username or “—”
name  = cb.from_user.full_name
key   = f”w_{uid}_{cb.message.message_id}”
pending_wd[key] = {“uid”: uid, “n”: d[“n”]}
stat_w += 1
adm = (f”📤 <b>Вивід зірок</b>\n👤 {name} (@{uname})\n”
f”🆔 <code>{uid}</code>\n⭐ <b>{d[‘n’]}</b> → {d[‘u’]}”)
await bot.send_message(ADMIN_ID, adm, reply_markup=adm_kb(key,“w”), parse_mode=“HTML”)
await obs(adm)
await state.clear()
await cb.message.edit_text(T(uid,“wd_sent”))
await bot.send_message(uid, mn(uid), reply_markup=menu(uid))
await cb.answer()

# ┌─────────────────────────────────────────────────────────┐

# │  TELEGRAM PREMIUM                                       │

# └─────────────────────────────────────────────────────────┘

@dp.message(lambda m: m.text == “💎 Telegram Premium”)
async def prem_h(msg: types.Message, state: FSMContext):
uid = msg.from_user.id
await state.set_state(S.Prem.period)
await msg.answer(T(uid,“prem_ask”), reply_markup=period_kb(uid), parse_mode=“HTML”)

@dp.callback_query(S.Prem.period, F.data.startswith(“P_”))
async def prem_period(cb: types.CallbackQuery, state: FSMContext):
uid = cb.from_user.id
m   = int(cb.data[2:])
await state.update_data(m=m)
await state.set_state(S.Prem.pay)
await cb.message.edit_text(
T(uid,“prem_pay”, m=m, u=PREM_UAH[m], t=PREM_TON[m]),
reply_markup=ppay_kb(uid), parse_mode=“HTML”
)
await cb.answer()

@dp.callback_query(S.Prem.pay, F.data.in_({“PP_uah”,“PP_ton”}))
async def prem_pay(cb: types.CallbackQuery, state: FSMContext):
uid = cb.from_user.id
d   = await state.get_data()
m   = d[“m”]
p   = cb.data
if p == “PP_uah”:
total   = PREM_UAH[m]
total_s = f”{total} грн”
meth    = “ПриватБанк”
else:
total   = PREM_TON[m]
total_s = f”{total} TON”
meth    = “TON”
await state.update_data(p=p, total=total, total_s=total_s, meth=meth)
await state.set_state(S.Prem.conf)
await cb.message.edit_text(
T(uid,“prem_confirm”, m=m, total=total_s, method=meth),
reply_markup=yn_kb(uid), parse_mode=“HTML”
)
await cb.answer()

@dp.callback_query(S.Prem.conf, F.data == “YES”)
async def prem_yes(cb: types.CallbackQuery, state: FSMContext):
uid = cb.from_user.id
d   = await state.get_data()
if d[“p”] == “PP_uah”:
txt = T(uid,“prem_uah”, m=d[“m”], total=d[“total”], card=CARD)
else:
txt = T(uid,“prem_ton”, m=d[“m”], total=d[“total”], ton=TON)
await state.set_state(S.Prem.photo)
await cb.message.edit_text(txt, parse_mode=“HTML”)
await cb.answer()

@dp.message(S.Prem.
photo, F.photo)
async def prem_photo(msg: types.Message, state: FSMContext):
global stat_p, rev_uah, rev_ton
uid   = msg.from_user.id
d     = await state.get_data()
uname = msg.from_user.username or “—”
name  = msg.from_user.full_name
key   = f”p_{uid}_{msg.message_id}”
pending_prm[key] = {“uid”: uid, “m”: d[“m”], “p”: d[“p”], “total”: d[“total”]}
stat_p += 1
adm = (f”💎 <b>Telegram Premium</b>\n👤 {name} (@{uname})\n”
f”🆔 <code>{uid}</code>\n📅 <b>{d[‘m’]} міс.</b> | 💰 <b>{d[‘total_s’]}</b>”)
await bot.send_photo(ADMIN_ID, photo=msg.photo[-1].file_id,
caption=adm, reply_markup=adm_kb(key,“p”), parse_mode=“HTML”)
await obs(adm, msg.photo[-1].file_id)
await state.clear()
await msg.answer(T(uid,“prem_ok”), reply_markup=menu(uid))

@dp.message(S.Prem.photo)
async def prem_nophoto(msg: types.Message):
await msg.answer(T(msg.from_user.id,“buy_need_pic”), parse_mode=“HTML”)

# ┌─────────────────────────────────────────────────────────┐

# │  ЗАВДАННЯ                                               │

# └─────────────────────────────────────────────────────────┘

TASKS_BTNS = [“📋 Завдання”,“📋 Задания”,“📋 Tasks”]
@dp.message(lambda m: m.text in TASKS_BTNS)
async def tasks_h(msg: types.Message):
uid = msg.from_user.id
task_list = get_active_tasks_for_user(uid)
if not task_list:
await msg.answer(T(uid,“tasks_empty”), reply_markup=menu(uid))
return
text = T(uid,"tasks_title")
user_done = done_tasks.get(uid, set())
for i, (tid, t) in enumerate(task_list, 1):
    done = tid in user_done
    status = "✅" if done else "🔲"
    text += f"{status} <b>{i}. {t['name']}</b>\n{t['desc']}\n💰 +<b>{t['reward']} ⭐</b>\n\n"

kb_rows = []
for tid, t in task_list:
    done = tid in user_done
    if done:
        kb_rows.append([InlineKeyboardButton(text=f"✅ {t['name']}", callback_data=f"TK_done_{tid}")])
    else:
        kb_rows.append([
            InlineKeyboardButton(text=f"👉 {t['name']}", url=t["link"]),
            InlineKeyboardButton(text="✅ Перевірити", callback_data=f"TK_check_{tid}"),
        ])
kb = InlineKeyboardMarkup(inline_keyboard=kb_rows)
await msg.answer(text, reply_markup=kb, parse_mode="HTML")

@dp.callback_query(F.data.startswith(“TK_done_”))
async def task_already_done(cb: types.CallbackQuery):
uid = cb.from_user.id
await cb.answer(T(uid,“task_done_already”), show_alert=True)

@dp.callback_query(F.data.startswith(“TK_check_”))
async def task_check(cb: types.CallbackQuery):
global stat_td
uid = cb.from_user.id
tid = int(cb.data[9:])
await cb.answer(T(uid,“task_check”))
if tid not in tasks:
    await cb.answer("❌ Завдання не знайдено", show_alert=True); return

t = tasks[tid]
user_done = done_tasks.get(uid, set())
if tid in user_done:
    await cb.answer(T(uid,"task_done_already"), show_alert=True); return

# Check subscription
channel_id = t.get("channel_id")
subscribed = False
if channel_id:
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=uid)
        subscribed = member.status not in ("left", "kicked", "banned")
    except:
        subscribed = False
else:
    subscribed = True  # No channel check needed

if subscribed:
    if uid not in done_tasks:
        done_tasks[uid] = set()
    done_tasks[uid].add(tid)
    add(uid, t["reward"])
    stat_td += 1
    await cb.message.answer(
        T(uid,"task_ok", reward=t["reward"], bal=bal(uid)),
        parse_mode="HTML", reply_markup=menu(uid)
    )
    # Refresh tasks view
    task_list = get_active_tasks_for_user(uid)
    if task_list:
        text = T(uid,"tasks_title")
        user_done2 = done_tasks.get(uid, set())
        for i, (t2id, t2) in enumerate(task_list, 1):
            done = t2id in user_done2
            status = "✅" if done else "🔲"
            text += f"{status} <b>{i}. {t2['name']}</b>\n{t2['desc']}\n💰 +<b>{t2['reward']} ⭐</b>\n\n"
        kb_rows = []
        for t2id, t2 in task_list:
            done = t2id in user_done2
            if done:
                kb_rows.append([InlineKeyboardButton(text=f"✅ {t2['name']}", callback_data=f"TK_done_{t2id}")])
            else:
                kb_rows.append([
f”📋 <b>Завдання #{tid}</b> — {status}\n\n”
f”📌 <b>{t[‘name’]}</b>\n{t[‘desc’]}\n”
f”🔗 {t[‘link’]}\n”
f”📡 Канал: {t.get(‘channel_id’) or ‘—’}\n”
f”💰 Нагорода: <b>{t[‘reward’]} ⭐</b>”
)
await msg.answer(text, reply_markup=task_admin_kb(tid), parse_mode=“HTML”)

# ┌─────────────────────────────────────────────────────────┐

# │  MAIN                                                   │

# └─────────────────────────────────────────────────────────┘

async def main():
logging.info(“🚀 Nexora Stars Bot запущено!”)
try:
await bot.send_message(ADMIN_ID,
“🟢 <b>Nexora Stars Bot запущено!</b>\n\n”
“Команди адміна:\n”
“/stats — статистика\n”
“/balances — баланси\n”
“/add_stars — нарахувати зірки\n”
“/sub_stars — забрати зірки\n”
“/broadcast — розсилка\n”
“/add_task — додати завдання\n”
“/tasks_list — список завдань”,
parse_mode=“HTML”)
except: pass
await dp.start_polling(bot, skip_updates=True)

if name == “**main**”:
asyncio.run(main())
[10.03.2026 18:37] Nexorik: InlineKeyboardButton(text=f"👉 {t2['name']}", url=t2["link"]),
                    InlineKeyboardButton(text="✅ Перевірити", callback_data=f"TK_check_{t2id}"),
                ])
        kb = InlineKeyboardMarkup(inline_keyboard=kb_rows)
        try:
            await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
        except: pass
else:
    await cb.answer(T(uid,"task_fail"), show_alert=True)

# ┌─────────────────────────────────────────────────────────┐

# │  ADMIN CALLBACKS                                        │

# └─────────────────────────────────────────────────────────┘

@dp.callback_query(F.data.startswith(“OK_b_”))
async def ok_buy(cb: types.CallbackQuery):
global rev_uah, rev_ton
if cb.from_user.id != ADMIN_ID: await cb.answer(“⛔”,show_alert=True); return
key = cb.data[5:]
o   = pending_buy.pop(key, None)
if not o: await cb.answer(“Вже оброблено.”,show_alert=True); return
add(o[“uid”], o[“n”])
# Track revenue
if o.get(“c”) == “C_uah”:
rev_uah += o.get(“total”, 0)
else:
rev_ton += o.get(“total”, 0)
await bot.send_message(o[“uid”], T(o[“uid”],“buy_done”,n=o[“n”],bal=bal(o[“uid”])), parse_mode=“HTML”)
await cb.message.edit_caption(caption=cb.message.caption+”\n\n✅ ПІДТВЕРДЖЕНО”, parse_mode=“HTML”)
await cb.answer(“✅”)

@dp.callback_query(F.data.startswith(“NO_b_”))
async def no_buy(cb: types.CallbackQuery):
if cb.from_user.id != ADMIN_ID: await cb.answer(“⛔”,show_alert=True); return
key = cb.data[5:]
o   = pending_buy.pop(key, None)
if not o: await cb.answer(“Вже оброблено.”,show_alert=True); return
await bot.send_message(o[“uid”], T(o[“uid”],“buy_rej”))
await cb.message.edit_caption(caption=cb.message.caption+”\n\n❌ ВІДХИЛЕНО”, parse_mode=“HTML”)
await cb.answer(“❌”)

@dp.callback_query(F.data.startswith(“OK_w_”))
async def ok_wd(cb: types.CallbackQuery):
if cb.from_user.id != ADMIN_ID: await cb.answer(“⛔”,show_alert=True); return
key = cb.data[5:]
o   = pending_wd.pop(key, None)
if not o: await cb.answer(“Вже оброблено.”,show_alert=True); return
sub(o[“uid”], o[“n”])
await bot.send_message(o[“uid”], T(o[“uid”],“wd_done”,bal=bal(o[“uid”])), parse_mode=“HTML”)
await cb.message.edit_text(cb.message.text+”\n\n✅ ПІДТВЕРДЖЕНО”, parse_mode=“HTML”)
await cb.answer(“✅”)

@dp.callback_query(F.data.startswith(“NO_w_”))
async def no_wd(cb: types.CallbackQuery):
if cb.from_user.id != ADMIN_ID: await cb.answer(“⛔”,show_alert=True); return
key = cb.data[5:]
o   = pending_wd.pop(key, None)
if not o: await cb.answer(“Вже оброблено.”,show_alert=True); return
await bot.send_message(o[“uid”], T(o[“uid”],“wd_rej”))
await cb.message.edit_text(cb.message.text+”\n\n❌ ВІДХИЛЕНО”, parse_mode=“HTML”)
await cb.answer(“❌”)

@dp.callback_query(F.data.startswith(“OK_p_”))
async def ok_prem(cb: types.CallbackQuery):
global rev_uah, rev_ton
if cb.from_user.id != ADMIN_ID: await cb.answer(“⛔”,show_alert=True); return
key = cb.data[5:]
o   = pending_prm.pop(key, None)
if not o: await cb.answer(“Вже оброблено.”,show_alert=True); return
# Track revenue
if o.get(“p”) == “PP_uah”:
rev_uah += o.get(“total”, 0)
else:
rev_ton += o.get(“total”, 0)
await bot.send_message(o[“uid”], T(o[“uid”],“prem_done”,m=o[“m”]), parse_mode=“HTML”)
await cb.message.edit_caption(caption=cb.message.caption+”\n\n✅ ПІДТВЕРДЖЕНО”, parse_mode=“HTML”)
await cb.answer(“✅”)

@dp.callback_query(F.data.startswith(“NO_p_”))
async def no_prem(cb: types.CallbackQuery):
if cb.from_user.id != ADMIN_ID: await cb.answer(“⛔”,show_alert=True); return
key = cb.data[5:]
o   = pending_prm.pop(key, None)
if not o: await cb.answer(“Вже оброблено.”,show_alert=True); return
await bot.send_message(o[“uid”], T(o[“uid”],“prem_rej”))
await cb.message.edit_caption(caption=cb.message.caption+”\n\n❌ ВІДХИЛЕНО”, parse_mode=“HTML”)
await cb.answer(“❌”)

# Task admin callbacks

@dp.callback_query(F.data.startswith(“TA_on_”))
async def task_on(cb: types.CallbackQuery):
if cb.from_user.id != ADMIN_ID: await cb.answer(“⛔”,show_alert=True); return
tid = int(cb.data[6:])
if tid in tasks:
tasks[tid][“active”] = True
await cb.
[10.03.2026 18:37] Nexorik: answer(f”✅ Завдання #{tid} увімкнено”, show_alert=True)
await cb.answer()

@dp.callback_query(F.data.startswith(“TA_off_”))
async def task_off(cb: types.CallbackQuery):
if cb.from_user.id != ADMIN_ID: await cb.answer(“⛔”,show_alert=True); return
tid = int(cb.data[7:])
if tid in tasks:
tasks[tid][“active”] = False
await cb.answer(f”❌ Завдання #{tid} вимкнено”, show_alert=True)
await cb.answer()

@dp.callback_query(F.data.startswith(“TA_del_”))
async def task_del(cb: types.CallbackQuery):
if cb.from_user.id != ADMIN_ID: await cb.answer(“⛔”,show_alert=True); return
tid = int(cb.data[7:])
if tid in tasks:
del tasks[tid]
await cb.message.edit_text(f”🗑 Завдання #{tid} видалено.”)
await cb.answer()

# ┌─────────────────────────────────────────────────────────┐

# │  ADMIN COMMANDS                                         │

# └─────────────────────────────────────────────────────────┘

@dp.message(Command(“stats”))
async def cmd_stats(msg: types.Message):
if msg.from_user.id != ADMIN_ID: return
await msg.answer(
T(ADMIN_ID,“stats”,
b=stat_b, w=stat_w, p=stat_p,
td=stat_td,
r=sum(ref_cnt.values()), rs=sum(ref_earn.values()),
u=len(langs),
rev_uah=round(rev_uah,2),
rev_ton=round(rev_ton,4)),
parse_mode=“HTML”
)

@dp.message(Command(“add_stars”))
async def cmd_add(msg: types.Message):
if msg.from_user.id != ADMIN_ID: return
parts = msg.text.split()
if len(parts)!=3 or not parts[1].isdigit() or not parts[2].isdigit():
await msg.answer(“Використання: /add_stars <user_id> <кількість>”); return
uid, n = int(parts[1]), int(parts[2])
add(uid, n)
await msg.answer(f”✅ +{n} ⭐ → {uid}. Баланс: {bal(uid)}”)

@dp.message(Command(“sub_stars”))
async def cmd_sub(msg: types.Message):
if msg.from_user.id != ADMIN_ID: return
parts = msg.text.split()
if len(parts) != 3 or not parts[1].isdigit() or not parts[2].isdigit():
await msg.answer(“Використання: /sub_stars <user_id> <кількість>”); return
uid, n = int(parts[1]), int(parts[2])
before = bal(uid)
sub(uid, n)
after = bal(uid)
actually = before - after
await msg.answer(f”✅ -{actually} ⭐ від {uid}. Баланс: {after}”)

@dp.message(Command(“balances”))
async def cmd_bals(msg: types.Message):
if msg.from_user.id != ADMIN_ID: return
if not stars:
await msg.answer(“Порожньо.”); return
lines = [f”<code>{u}</code>: {s} ⭐” for u,s in stars.items()]
await msg.answer(“📊 <b>Баланси:</b>\n\n”+”\n”.join(lines), parse_mode=“HTML”)

# ─── /broadcast ───────────────────────────────────────────

@dp.message(Command(“broadcast”))
async def cmd_broadcast(msg: types.Message, state: FSMContext):
if msg.from_user.id != ADMIN_ID: return
await state.set_state(S.Broadcast.content)
await msg.answer(
“📢 <b>Розсилка</b>\n\nНадішліть текст або фото з підписом для розсилки.\n\n”
“Натисніть /cancel для скасування.”,
parse_mode=“HTML”
)

@dp.message(S.Broadcast.content, Command(“cancel”))
async def broadcast_cancel(msg: types.Message, state: FSMContext):
if msg.from_user.id != ADMIN_ID: return
await state.clear()
await msg.answer(“❌ Розсилку скасовано.”)

@dp.message(S.Broadcast.content)
async def broadcast_content(msg: types.Message, state: FSMContext):
if msg.from_user.id != ADMIN_ID: return
# Save content info
data = {}
if msg.photo:
data[“photo_id”] = msg.photo[-1].file_id
data[“caption”]  = msg.caption or “”
data[“type”]     = “photo”
elif msg.text:
data[“text”] = msg.text
data[“type”] = “text”
else:
await msg.answer(“❌ Надішліть текст або фото.”); return
await state.update_data(**data)
await state.set_state(S.Broadcast.confirm)

# Preview
preview_text = f"👁 <b>Прев'ю розсилки</b>\n\nОтримувачів: <b>{len(langs)}</b>\n\n"
kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="✅ Відправити всім", callback_data="BC_yes"),
    InlineKeyboardButton(text="❌ Скасувати",       callback_data="BC_no"),
]])
if data["type"] == "photo":
    await msg.answer_photo(
        photo=data["photo_id"],
        caption=preview_text + (data["caption"] or ""),
        reply_markup=kb, parse_mode="HTML"
    )
else:
    await msg.answer(preview_text + data["text"], reply_markup=kb, parse_mode="HTML")

@dp.callback_query(S.
Broadcast.confirm, F.data == “BC_yes”)
async def broadcast_send(cb: types.CallbackQuery, state: FSMContext):
if cb.from_user.id != ADMIN_ID: return
d = await state.get_data()
await state.clear()
await cb.message.edit_reply_markup(reply_markup=None)
await cb.answer()
total = len(langs)
sent = 0
failed = 0
status_msg = await cb.message.answer(f"📤 Відправляю... 0/{total}")

for uid in list(langs.keys()):
    try:
        if d["type"] == "photo":
            await bot.send_photo(uid, photo=d["photo_id"], caption=d.get("caption",""), parse_mode="HTML")
        else:
            await bot.send_message(uid, d["text"], parse_mode="HTML")
        sent += 1
    except:
        failed += 1
    await asyncio.sleep(0.05)  # flood protection

await status_msg.edit_text(
    f"✅ <b>Розсилку завершено!</b>\n\n"
    f"✅ Успішно: <b>{sent}</b>\n❌ Помилок: <b>{failed}</b>",
    parse_mode="HTML"
)

@dp.callback_query(S.Broadcast.confirm, F.data == “BC_no”)
async def broadcast_no(cb: types.CallbackQuery, state: FSMContext):
if cb.from_user.id != ADMIN_ID: return
await state.clear()
await cb.message.edit_text(“❌ Розсилку скасовано.”)
await cb.answer()

# ─── /add_task ────────────────────────────────────────────

@dp.message(Command(“add_task”))
async def cmd_add_task(msg: types.Message, state: FSMContext):
if msg.from_user.id != ADMIN_ID: return
await state.set_state(S.AddTask.name)
await msg.answer(
“📋 <b>Додавання завдання</b>\n\n<b>Крок 1/5</b> — Введіть назву завдання:”,
parse_mode=“HTML”
)

@dp.message(S.AddTask.name)
async def task_add_name(msg: types.Message, state: FSMContext):
if msg.from_user.id != ADMIN_ID: return
await state.update_data(name=msg.text.strip())
await state.set_state(S.AddTask.desc)
await msg.answer(”<b>Крок 2/5</b> — Введіть опис завдання:”, parse_mode=“HTML”)

@dp.message(S.AddTask.desc)
async def task_add_desc(msg: types.Message, state: FSMContext):
if msg.from_user.id != ADMIN_ID: return
await state.update_data(desc=msg.text.strip())
await state.set_state(S.AddTask.link)
await msg.answer(”<b>Крок 3/5</b> — Введіть посилання на канал (https://t.me/…):”, parse_mode=“HTML”)

@dp.message(S.AddTask.link)
async def task_add_link(msg: types.Message, state: FSMContext):
if msg.from_user.id != ADMIN_ID: return
await state.update_data(link=msg.text.strip())
await state.set_state(S.AddTask.channel)
await msg.answer(
“<b>Крок 4/5</b> — Введіть username або ID каналу для перевірки підписки\n”
“(наприклад: @mychannel або -1001234567890)\n\n”
“Або введіть <code>-</code> якщо перевірка не потрібна:”,
parse_mode=“HTML”
)

@dp.message(S.AddTask.channel)
async def task_add_channel(msg: types.Message, state: FSMContext):
if msg.from_user.id != ADMIN_ID: return
ch = msg.text.strip()
if ch == “-”:
channel_id = None
else:
channel_id = ch
await state.update_data(channel_id=channel_id)
await state.set_state(S.AddTask.reward)
await msg.answer(”<b>Крок 5/5</b> — Введіть нагороду в зірках (число):”, parse_mode=“HTML”)

@dp.message(S.AddTask.reward)
async def task_add_reward(msg: types.Message, state: FSMContext):
global task_counter
if msg.from_user.id != ADMIN_ID: return
if not msg.text.isdigit() or int(msg.text) <= 0:
await msg.answer(“❌ Введіть число більше 0.”); return
reward = int(msg.text)
d = await state.get_data()
await state.clear()
task_counter += 1
tid = task_counter
tasks[tid] = {
    "name":       d["name"],
    "desc":       d["desc"],
    "link":       d["link"],
    "channel_id": d.get("channel_id"),
    "reward":     reward,
    "active":     True,
}
await msg.answer(
    f"✅ <b>Завдання #{tid} додано!</b>\n\n"
    f"📌 <b>{d['name']}</b>\n{d['desc']}\n"
    f"🔗 {d['link']}\n"
    f"📡 Канал: {d.get('channel_id') or '—'}\n"
    f"💰 Нагорода: <b>{reward} ⭐</b>",
    parse_mode="HTML"
)

# ─── /tasks_list ──────────────────────────────────────────

@dp.message(Command(“tasks_list”))
async def cmd_tasks_list(msg: types.Message):
if msg.from_user.id != ADMIN_ID: return
if not tasks:
await msg.answer(“📋 Завдань немає.”); return
for tid, t in tasks.items():
status = “✅ Активне” if t[“active”] else “❌ Вимкнено”
text = (
