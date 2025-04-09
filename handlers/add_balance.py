from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from handlers.balances import user_balances

async def add_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("add_balance function called")  # Dodane logowanie
    try:
        parts = update.message.text.split()
        if len(parts) != 2:
            raise ValueError("Niepoprawny format wiadomości")
        
        uid, amount = parts
        print(f"Parsed UID: {uid}, Amount: {amount}")  # Dodane logowanie
        uid, amount = int(uid), float(amount)
        user_balances[uid] = user_balances.get(uid, 0.0) + amount
        print(f"Updated balance for UID {uid}: {user_balances[uid]}")  # Dodane logowanie
        await update.message.reply_text(f"✅ Dodano {amount:.2f} zł do użytkownika {uid}.")
    
    except ValueError as ve:
        print(f"ValueError in add_balance: {ve}")  # Dodane logowanie
        await update.message.reply_text("❌ Błąd formatu. Upewnij się, że wiadomość zawiera identyfikator użytkownika i kwotę oddzielone spacją.")
    
    except Exception as e:
        print(f"Error in add_balance: {e}")  # Dodane logowanie
        await update.message.reply_text("❌ Wystąpił błąd podczas przetwarzania.")
    
    return ConversationHandler.END