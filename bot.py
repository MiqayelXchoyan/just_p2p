from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from concurrent.futures import ThreadPoolExecutor

from parser1rub import get_bybit_rub
from parser2rub import get_bingx_rub
from parser3rub import get_bitget_rub

from parser4amd import get_binance_amd
from parser5amd import get_bybit_amd
from parser6amd import get_okx_amd
from parser7amd import get_bingx_amd

from limits import can_access, is_premium, add_premium, remove_premium

bot = TeleBot(token="YOUR TELEGRAM BOT TOKEN")

ADMIN_USERNAME = "@username"
ADMIN_ID = 12345678

def gen_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("RUB 🇷🇺", callback_data="rub_yes"),
        InlineKeyboardButton("AMD 🇦🇲", callback_data="amd_yes")
    )
    markup.add(
        InlineKeyboardButton("✨ Активировать Premium", callback_data="activate_premium")
    )
    return markup

def back_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 Назад", callback_data="back"))
    return markup

def wallet_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("💵 Оплатить через TON Wallet", url="TON WALLET URL"),
        InlineKeyboardButton("💸 Оплатить через ЮMoney (4100119158914898)", url="ЮMoney URL"),
        InlineKeyboardButton("💶 Оплатить через Idram (886226199)", url="IDRAM ID")
    )
    markup.add(InlineKeyboardButton("🔙 Назад", callback_data="back"))
    return markup

@bot.message_handler(commands=['start'])
def start_bot(message):
    send_currency_selection(message.chat.id)

@bot.message_handler(commands=['mystatus'])
def my_status(message):
    if is_premium(message.chat.id):
        bot.send_message(message.chat.id, "✨ У вас активен Premium доступ.")
    else:
        bot.send_message(message.chat.id, "🔒 У вас обычный доступ. Вы можете использовать бота 3 раза в день.")

@bot.message_handler(commands=['addpremium'])
def add_premium_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        chat_id = int(message.text.split()[1])
        add_premium(chat_id)
        bot.send_message(message.chat.id, f"✅ Premium выдан для пользователя {chat_id}.")
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Используйте: /addpremium <chat_id>")

@bot.message_handler(commands=['removepremium'])
def remove_premium_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        chat_id = int(message.text.split()[1])
        remove_premium(chat_id)
        bot.send_message(message.chat.id, f"❌ Premium убран у пользователя {chat_id}.")
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Используйте: /removepremium <chat_id>")

def send_currency_selection(chat_id):
    text = (
        "<b>BINANCE, BYBIT, OKX, BINGX, BITGET</b>\n\n"
        "Бот показывает лучшие курсы обмена на USDT 💲.\n"
        "Выберите валюту ⬇️💸"
    )
    bot.send_message(chat_id, text, parse_mode='HTML', reply_markup=gen_markup())

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    chat_id = callback.message.chat.id
    data = callback.data

    
    bot.answer_callback_query(callback.id)

    if data == "rub_yes":
        if not can_access(chat_id):
            bot.send_message(
                chat_id,
                f"<b>Достигнут лимит: 3 бесплатных использования в сутки.</b>\n"
                f"Для продолжения — активируйте Premium за 4 USD / 400 RUB / 1600 AMD.\n"
                f"✉️ Напишите {ADMIN_USERNAME} после оплаты и отправьте чек.",
                parse_mode="HTML",
                reply_markup=wallet_markup()
            )
            return

        bot.send_message(chat_id, "⏳ Минуту, ищу лучший курс USDT для RUB 🇷🇺\n😊Не закрывайте бот", reply_markup=back_markup())

        with ThreadPoolExecutor() as executor:
            future_bybit = executor.submit(get_bybit_rub)
            future_bingx = executor.submit(get_bingx_rub)
            future_bitget = executor.submit(get_bitget_rub)

            bybit_buy, bybit_sell = future_bybit.result()
            bingx_buy, bingx_sell = future_bingx.result()
            bitget_buy, bitget_sell = future_bitget.result()

        result = (
            "📊 <b>Актуальные курсы USDT (RUB)</b>:\n\n"
            "🌐 <b>Bybit</b>\n"
            f"🔹 Покупка: <b>₽{bybit_buy}</b>\n"
            f"🔺 Продажа: <b>₽{bybit_sell}</b>\n\n"
            "🌐 <b>BingX</b>\n"
            f"🔹 Покупка: <b>{bingx_buy}</b>\n"
            f"🔺 Продажа: <b>{bingx_sell}</b>\n\n"
            "🌐 <b>Bitget</b>\n"
            f"🔹 Покупка: <b>₽{bitget_buy}</b>\n"
            f"🔺 Продажа: <b>₽{bitget_sell}</b>"
        )

        bot.send_message(chat_id, result, parse_mode="HTML", reply_markup=back_markup())

    elif data == "amd_yes":
        if not can_access(chat_id):
            bot.send_message(
                chat_id,
                f"<b>Достигнут лимит: 3 бесплатных использования в сутки.</b>\n"
                f"Для продолжения — активируйте Premium за 4 USD / 400 RUB / 1600 AMD.\n"
                f"✉️ Напишите {ADMIN_USERNAME} после оплаты и отправьте чек.",
                parse_mode="HTML",
                reply_markup=wallet_markup()
            )
            return

        bot.send_message(chat_id, "⏳ Минуту, ищу лучший курс USDT для AMD 🇦🇲\n😊Не закрывайте бот", reply_markup=back_markup())

        with ThreadPoolExecutor() as executor:
            future_binance = executor.submit(get_binance_amd)
            future_bybit = executor.submit(get_bybit_amd)
            future_okx = executor.submit(get_okx_amd)
            future_bingx = executor.submit(get_bingx_amd)

            binance_buy, binance_sell = future_binance.result()
            bybit_buy, bybit_sell = future_bybit.result()
            okx_buy, okx_sell = future_okx.result()
            bingx_buy, bingx_sell = future_bingx.result()

        result = (
            "📊 <b>Актуальные курсы USDT (AMD)</b>:\n\n"
            "🌐 <b>Binance</b>\n"
            f"🔹 Покупка: <b>֏{binance_buy}</b>\n"
            f"🔺 Продажа: <b>֏{binance_sell}</b>\n\n"
            "🌐 <b>Bybit</b>\n"
            f"🔹 Покупка: <b>֏{bybit_buy}</b>\n"
            f"🔺 Продажа: <b>֏{bybit_sell}</b>\n\n"
            "🌐 <b>OKX</b>\n"
            f"🔹 Покупка: <b>֏{okx_buy}</b>\n"
            f"🔺 Продажа: <b>֏{okx_sell}</b>\n\n"
            "🌐 <b>BingX</b>\n"
            f"🔹 Покупка: <b>{bingx_buy}</b>\n"
            f"🔺 Продажа: <b>{bingx_sell}</b>"
        )

        bot.send_message(chat_id, result, parse_mode="HTML", reply_markup=back_markup())

    elif data == "activate_premium":
        text = (
            "<b>Для активации Premium доступа</b>\n\n"
            "💲 Стоимость: 4 USD / 400 RUB / 1600 AMD в месяц\n"
            f"✉️ После оплаты обязательно напишите в чат {ADMIN_USERNAME} с подтверждением."
        )
        bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=wallet_markup())

    elif data == "back":
        
        send_currency_selection(chat_id)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_unknown_message(message):
    
    if message.text.startswith('/'):
        return

    bot.send_message(
        message.chat.id,
        "❗️Я понимаю только команды и нажатия на кнопки.\n\n"
        "Пожалуйста, используйте меню ниже или нажмите /start для начала.",
        reply_markup=gen_markup()
    )



bot.infinity_polling(allowed_updates=['message', 'callback_query'])
