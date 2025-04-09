from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from config import user_balances, transaction_history, notifications_enabled, ZGLOSZENIE_TEKST, DODAJ_BALANCE, USUN_BALANCE, WIADOMOSC_ALL, ADMIN_ID

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global notifications_enabled

    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("accept_") or data.startswith("reject_"):
        action, user_id_str, kwota_str = data.split("_")
        user_id = int(user_id_str)
        kwota = float(kwota_str)
        profit = round(kwota * 0.20, 2)
        saldo = round(kwota - profit, 2)

        username = (await context.bot.get_chat(user_id)).username or user_id
        admin_user = query.from_user

        if action == "accept":
            user_balances[user_id] = user_balances.get(user_id, 0) + saldo
            transaction_history.setdefault(user_id, []).append(f"+{saldo:.2f} zł (BLIK)")
            if notifications_enabled:
                await context.bot.send_message(user_id, f"✅ Twój kod BLIK został zaakceptowany. Dodano {saldo:.2f} zł do konta.")
            status_text = "✅ *ZAAKCEPTOWANO*"
        else:
            await context.bot.send_message(user_id, "❌ Twój kod BLIK został odrzucony.")
            status_text = "❌ *ODRZUCONO*"

        updated_msg = (
            "💰 *NOWA WPŁATA BLIK*\n\n"
            f"👤 *User*: @{username}\n"
            f"💳 *Kwota*: {kwota:.2f} PLN\n"
            f"📉 *Do wypłaty (po 20% prowizji)*: {saldo:.2f} PLN\n"
            f"📈 *Profit*: {profit:.2f} PLN\n"
            "🔢 *Kod BLIK*: ❌ UKRYTY DLA BEZPIECZEŃSTWA\n\n"
            f"{status_text}\n"
            f"👷 *Wykonał*: @{admin_user.username or admin_user.first_name}"
        )
        await query.edit_message_text(updated_msg, parse_mode=ParseMode.MARKDOWN)

    elif data == 'konto':
        uid = query.from_user.id
        saldo = user_balances.get(uid, 0.0)
        keyboard = [
            [InlineKeyboardButton("💸 Wypłać", callback_data='wyplata')],
            [InlineKeyboardButton("🔙 Powrót do menu", callback_data="menu")]
        ]
        await query.edit_message_text(f"💰 Twoje saldo: {saldo:.2f} zł", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'wyplata':
        user = query.from_user
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"💸 @{user.username} poprosił o wypłatę.")
        await query.edit_message_text("💸 Prośba o wypłatę wysłana.")

    elif data == 'blik':
        await query.edit_message_text("Użyj: /blik <kod> <kwota>", parse_mode='Markdown')

    elif data == 'fee':
        keyboard = [[InlineKeyboardButton("🔙 Powrót do menu", callback_data="menu")]]
        await query.edit_message_text("💸 Prowizja to 20%.", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'zgloszenie':
        await query.edit_message_text("✏️ Podaj treść zgłoszenia.")
        return ZGLOSZENIE_TEKST

    elif data == 'menu':
        await query.edit_message_text("Wybierz jedną z opcji:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("BLIK 🐝", callback_data='blik'),
             InlineKeyboardButton("Fee 📄", callback_data='fee'),
             InlineKeyboardButton("Konto 💰", callback_data='konto')],
            [InlineKeyboardButton("Utwórz zgłoszenie 📝", callback_data='zgloszenie')]
        ]))

    elif data == "toggle_notifs":
        notifications_enabled = not notifications_enabled
        await query.edit_message_text(f"🔔 Powiadomienia {'włączone' if notifications_enabled else 'wyłączone'}.")

    elif data == "add_balance":
        await query.edit_message_text("✏️ Podaj ID użytkownika i kwotę do dodania (np. 123456 50.0):")
        return DODAJ_BALANCE

    elif data == "remove_balance":
        await query.edit_message_text("✏️ Podaj ID użytkownika i kwotę do usunięcia (np. 123456 20.0):")
        return USUN_BALANCE

    elif data == "msg_all":
        await query.edit_message_text("✏️ Podaj wiadomość do wysłania wszystkim użytkownikom:")
        return WIADOMOSC_ALL