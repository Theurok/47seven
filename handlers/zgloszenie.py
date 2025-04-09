from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from config import ADMIN_ID

async def przyjmij_zgloszenie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 Zgłoszenie od @{user.username or user.id}:\n\n{text}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✉️ Odpowiedz", callback_data=f"reply_{user.id}")]]))
    await update.message.reply_text("✅ Zgłoszenie wysłane.")
    return ConversationHandler.END