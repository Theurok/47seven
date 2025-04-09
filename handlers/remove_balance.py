from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from handlers.balances import user_balances

async def remove_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("remove_balance function called")  # Debug statement
    try:
        parts = update.message.text.split()
        if len(parts) != 2:
            raise ValueError("Niepoprawny format wiadomości")
        
        uid, amount = parts
        print(f"Parsed UID: {uid}, Amount: {amount}")  # Debug statement
        uid, amount = int(uid), float(amount)
        user_balances[uid] = user_balances.get(uid, 0.0) - amount
        print(f"Updated balance for UID {uid}: {user_balances[uid]}")  # Debug statement
        await update.message.reply_text(f"✅ Usunięto {amount:.2f} zł od użytkownika {uid}.")
    
    except ValueError as ve:
        print(f"ValueError in remove_balance: {ve}")  # Debug statement
        await update.message.reply_text("❌ Błąd formatu. Upewnij się, że wiadomość zawiera identyfikator użytkownika i kwotę oddzielone spacją.")
    
    except Exception as e:
        print(f"Error in remove_balance: {e}")  # Debug statement
        await update.message.reply_text("❌ Wystąpił błąd podczas przetwarzania.")
    
    return ConversationHandler.END