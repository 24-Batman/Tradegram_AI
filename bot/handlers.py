import logging
from telegram import Update
from telegram.ext import ContextTypes
from utils import setup_logging

logger = logging.getLogger(__name__)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle non-command messages"""
    try:
        message = update.message.text
        logger.info(f"Received message: {message}")
        
        # Guide users to use commands
        response = (
            "I work best with commands! Try these:\n"
            "/market - Get market analysis\n"
            "/help - See all commands"
        )
        await update.message.reply_text(response)

    except Exception as e:
        logger.error(f"Error in message handler: {str(e)}")
        await error_handler(update, context)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors in the bot"""
    logger.error(f"Update {update} caused error {context.error}")
    
    error_message = "Sorry, something went wrong. Please try again later."
    if update and update.effective_message:
        await update.effective_message.reply_text(error_message) 