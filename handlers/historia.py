from telegram import Update
from telegram.ext import ContextTypes

async def historia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    historia = transaction_history.get(uid, [])
    if not historia:
        await update.message.reply_text("📭 Brak historii.")
    else:
        await update.message.reply_text("📜 Historia:\n" + "\n".join(historia[-10:]))