from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from config import ADMIN_ID
from handlers.add_balance import add_balance
from handlers.remove_balance import remove_balance
from handlers.msg_all import msg_all

# Poprawna liczba zmiennych do rozpakowania wartości z range(6)
ZGLOSZENIE_TEKST, ADMIN_ODPOWIEDZ, ADMIN_PANEL, DODAJ_BALANCE, USUN_BALANCE, WIADOMOSC_ALL = range(6)

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 1 and context.args[0] == "1525":
        keyboard = [
            [InlineKeyboardButton("➕ Dodaj balance", callback_data="add_balance"),
             InlineKeyboardButton("➖ Usuń balance", callback_data="remove_balance")],
            [InlineKeyboardButton("📢 Wiadomość do wszystkich", callback_data="msg_all")],
            [InlineKeyboardButton("🔕 Powiadomienia", callback_data="toggle_notifs")]
        ]
        await update.message.reply_text("🔧 Panel admina:", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text("Brak dostępu.")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "add_balance":
        await query.edit_message_text(text="Podaj ID użytkownika i kwotę do dodania (np. '123 45.67'):")
        return DODAJ_BALANCE
    elif query.data == "remove_balance":
        await query.edit_message_text(text="Podaj ID użytkownika i kwotę do usunięcia (np. '123 45.67'):")
        return USUN_BALANCE
    elif query.data == "msg_all":
        await query.edit_message_text(text="Podaj wiadomość do wysłania do wszystkich użytkowników:")
        return WIADOMOSC_ALL

async def przyjmij_zgloszenie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 Zgłoszenie od @{user.username or user.id}:\n\n{text}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✉️ Odpowiedz", callback_data=f"reply_{user.id}")]]))
    await update.message.reply_text("✅ Zgłoszenie wysłane.")
    return ConversationHandler.END