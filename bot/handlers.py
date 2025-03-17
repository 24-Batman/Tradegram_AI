import logging
from telegram import Update
from telegram.ext import ContextTypes
from data.logs.logger import setup_logger  # Use the centralized logger setup

logger = setup_logger(__name__)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle non-command messages"""
    try:
        # Process user message
        message = update.message.text.lower()
        
        # Add custom message handling logic here
        if "help" in message:
            await update.message.reply_text("Use /help to see available commands!")
        else:
            await update.message.reply_text("I only respond to commands. Use /help to see what I can do!")
    except Exception as e:
        logger.error(f"Error in message handler: {str(e)}")
        await update.message.reply_text("❌ Sorry, I couldn't process your message")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle bot errors"""
    logger.error(f"Update {update} caused error: {context.error}")
    
    try:
        if update and update.message:
            await update.message.reply_text(
                "❌ Sorry, something went wrong. Please try again later."
            )
    except Exception as e:
        logger.error(f"Error in error handler: {str(e)}") 