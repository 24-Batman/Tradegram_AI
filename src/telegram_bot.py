import os
from dotenv import load_dotenv
load_dotenv()
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
from telegram.ext import Application

# Load configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: CallbackContext) -> None:
    """Send welcome message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\! Welcome to TradeMateAI Bot\!',
        reply_markup=ReplyKeyboardRemove(),
    )

async def help_command(update: Update, context: CallbackContext) -> None:
    """Send help message when the command /help is issued."""
    await update.message.reply_text('Help section coming soon!')

async def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(BOT_TOKEN).build()

    # Register commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Register message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start polling
    application.run_polling()
    print("Bot is running...")

if __name__ == '__main__':
    main() 