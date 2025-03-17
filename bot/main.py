import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from .commands import *

# Load the bot token from the .env file
BOT_TOKEN = os.getenv("BOT_TOKEN")



def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("market", market_command))
    application.add_handler(CommandHandler("sentiment", sentiment_command))
    application.add_handler(CommandHandler("trade", trade_command))
    application.add_handler(CommandHandler("settings", settings_command))

    application.run_polling()

if __name__ == '__main__':
    main()
