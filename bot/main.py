import asyncio
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN
from commands import start_command, help_command, market_command, sentiment_command, snipe_command, report_command
from handlers import message_handler, error_handler
from utils import setup_logging

logger = logging.getLogger(__name__)

async def main():
    """Initialize and start the bot"""
    setup_logging()
    logger.info("Starting TradeMateAI bot...")

    # Initialize bot application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("market", market_command))
    application.add_handler(CommandHandler("sentiment", sentiment_command))
    application.add_handler(CommandHandler("snipe", snipe_command))
    application.add_handler(CommandHandler("report", report_command))

    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # Add error handler
    application.add_error_handler(error_handler)

    # Start the bot
    logger.info("Bot started successfully!")
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    asyncio.run(main()) 