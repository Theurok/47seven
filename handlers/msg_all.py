from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

async def msg_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("msg_all function called")  # Debug statement
    msg = update.message.text
    for uid in user_balances:
        try:
            await context.bot.send_message(uid, f"📢 {msg}")
        except Exception as e:
            print(f"Error sending message to {uid}: {e}")  # Debug statement
            continue
    await update.message.reply_text("✅ Wiadomość wysłana.")
    return ConversationHandler.END