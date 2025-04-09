from telegram import Update
from telegram.ext import ContextTypes
from handlers.balances import user_balances

async def konto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    saldo = user_balances.get(update.effective_user.id, 0.0)
    await update.message.reply_text(f"Twoje saldo wynosi: {saldo:.2f} zł")