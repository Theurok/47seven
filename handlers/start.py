from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("BLIK 🐝", callback_data='blik'),
         InlineKeyboardButton("Fee 📄", callback_data='fee'),
         InlineKeyboardButton("Konto 💰", callback_data='konto')],
        [InlineKeyboardButton("Utwórz zgłoszenie 📝", callback_data='zgloszenie')]
    ]
    await update.message.reply_text("Witaj! Wybierz jedną z opcji:", reply_markup=InlineKeyboardMarkup(keyboard))