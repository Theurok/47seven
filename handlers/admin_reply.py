from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from config import pending_responses, ADMIN_ODPOWIEDZ

async def admin_reply_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = int(query.data.split('_')[1])
    pending_responses[user_id] = query.message.message_id
    await query.edit_message_text("✏️ Podaj odpowiedź:")
    return ADMIN_ODPOWIEDZ

async def admin_send_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    response = update.message.text
    if user_id in pending_responses:
        original_message_id = pending_responses.pop(user_id)
        await context.bot.send_message(chat_id=user_id, text=f"📩 Odpowiedź: {response}")
        await context.bot.edit_message_text(
            chat_id=ADMIN_ID,
            message_id=original_message_id,
            text=f"✉️ Odpowiedź wysłana:\n\n{response}"
        )
    else:
        await update.message.reply_text("❌ Brak wiadomości do odpowiedzi.")
    return ConversationHandler.END