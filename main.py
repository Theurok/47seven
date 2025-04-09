from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
from handlers.start import start
from handlers.admin_panel import admin_panel, callback_handler
from handlers.add_balance import add_balance
from handlers.remove_balance import remove_balance
from handlers.msg_all import msg_all
from handlers.blik import blik
from handlers.button import button
from handlers.konto import konto
from handlers.historia import historia
from handlers.zgloszenie import przyjmij_zgloszenie
from handlers.admin_reply import admin_reply_prompt, admin_send_reply
from config import TOKEN, ZGLOSZENIE_TEKST, ADMIN_ODPOWIEDZ, DODAJ_BALANCE, USUN_BALANCE, WIADOMOSC_ALL

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Handler for the start command
    app.add_handler(CommandHandler("start", start))

    # Handler for the admin panel command
    app.add_handler(CommandHandler("admin", admin_panel))

    # ConversationHandler for admin panel actions
    admin_panel_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(callback_handler)],
        states={
            DODAJ_BALANCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_balance)],
            USUN_BALANCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_balance)],
            WIADOMOSC_ALL: [MessageHandler(filters.TEXT & ~filters.COMMAND, msg_all)],
        },
        fallbacks=[],
    )
    app.add_handler(admin_panel_conv_handler)

    # ConversationHandler for admin replies
    admin_reply_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_reply_prompt, pattern=r"^reply_\d+$")],
        states={
            ADMIN_ODPOWIEDZ: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_send_reply)],
        },
        fallbacks=[],
    )
    app.add_handler(admin_reply_conv_handler)

    # ConversationHandler for handling submissions
    zgloszenie_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("zgloszenie", przyjmij_zgloszenie)],
        states={
            ZGLOSZENIE_TEKST: [MessageHandler(filters.TEXT & ~filters.COMMAND, przyjmij_zgloszenie)],
        },
        fallbacks=[],
    )
    app.add_handler(zgloszenie_conv_handler)

    # Handlers for other commands
    app.add_handler(CommandHandler("blik", blik))
    app.add_handler(CommandHandler("konto", konto))
    app.add_handler(CommandHandler("historia", historia))
    app.add_handler(CallbackQueryHandler(button))

    # Start polling updates
    app.run_polling()

if __name__ == "__main__":
    main()