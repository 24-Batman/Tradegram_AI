import logging
from telegram import Update
from telegram.ext import ContextTypes
from utils import format_price_data, fetch_market_data
from agent.agent import TradingAgent

logger = logging.getLogger(__name__)
trading_agent = TradingAgent()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    welcome_message = (
        "🤖 Welcome to TradeMateAI! 📊\n\n"
        "I'm your AI-powered trading assistant. Here's what I can do:\n"
        "• Analyze market trends\n"
        "• Provide sentiment analysis\n"
        "• Monitor token launches\n"
        "• Generate trade reports\n\n"
        "Use /help to see all available commands!"
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command"""
    help_text = (
        "📚 Available Commands:\n\n"
        "/market <symbol> - Get real-time market analysis\n"
        "/sentiment <symbol> - Get AI sentiment analysis\n"
        "/snipe <token> - Monitor token launch\n"
        "/report - Generate trading report\n"
        "/help - Show this help message"
    )
    await update.message.reply_text(help_text)

async def market_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /market command"""
    try:
        if not context.args:
            await update.message.reply_text("Please provide a symbol. Example: /market BTC")
            return

        symbol = context.args[0].upper()
        market_data = await fetch_market_data(symbol)
        formatted_data = format_price_data(market_data)
        await update.message.reply_text(formatted_data)

    except Exception as e:
        logger.error(f"Error in market command: {str(e)}")
        await update.message.reply_text("Sorry, I couldn't fetch the market data. Please try again later.")

# Similar implementations for sentiment_command, snipe_command, and report_command... 