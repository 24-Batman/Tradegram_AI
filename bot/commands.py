from telegram import Update
from telegram.ext import ContextTypes
import sys
from pathlib import Path

# Add the project root directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from agent.agent import TradingAgent
from data.logs.logger import setup_logger
from .utils import format_price_data
from typing import Dict, Any
from config.settings import settings

logger = setup_logger(__name__)
trading_agent = TradingAgent()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    welcome_message = (
        "🤖 Welcome to TradeMateAI!\n\n"
        "I can help you with:\n"
        "📊 Market Analysis\n"
        "📈 Trading Signals\n"
        "📰 Sentiment Analysis\n\n"
        "Use /help to see all available commands."
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = (
        "Available commands:\n\n"
        "/market <symbol> - Get market analysis\n"
        "/sentiment <symbol> - Get sentiment analysis\n"
        "/trade <symbol> - Get trading signals\n"
        "/settings - View/update settings\n"
        "/help - Show this help message"
    )
    await update.message.reply_text(help_text)

async def market_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /market command"""
    try:
        if not context.args:
            await update.message.reply_text("Please provide a trading pair symbol (e.g., /market BTC/USD)")
            return
            
        symbol = context.args[0].upper()
        analysis = await trading_agent.analyze_market(symbol)
        
        if analysis:
            response = (
                f"📊 Market Analysis for {symbol}\n\n"
                f"💰 Price: ${analysis['price']:,.2f}\n"
                f"📈 24h Change: {analysis['change_24h']:+.2f}%\n"
                f"📊 Volume: ${analysis['volume']:,.0f}\n"
                f"📰 Sentiment: {analysis['sentiment']}\n"
                f"🎯 Confidence: {analysis['confidence']:.2f}\n"
                f"📝 Recommendation: {analysis['recommendation']}"
            )
        else:
            response = f"❌ Failed to analyze market for {symbol}"
            
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error in market command: {str(e)}")
        await update.message.reply_text("❌ An error occurred while analyzing the market")

async def sentiment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /sentiment command"""
    try:
        if not context.args:
            await update.message.reply_text("Please provide a symbol (e.g., /sentiment BTC)")
            return
            
        symbol = context.args[0].upper()
        sentiment = await trading_agent.analyze_sentiment(symbol)
        
        if sentiment:
            response = (
                f"📰 Sentiment Analysis for {symbol}\n\n"
                f"Overall: {sentiment['sentiment']}\n"
                f"Confidence: {sentiment['confidence']:.2f}\n"
                f"Sources: {len(sentiment['sources'])}"
            )
        else:
            response = f"❌ Failed to analyze sentiment for {symbol}"
            
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error in sentiment command: {str(e)}")
        await update.message.reply_text("❌ An error occurred while analyzing sentiment")

async def trade_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /trade command for trading signals"""
    try:
        if not context.args:
            await update.message.reply_text("Please provide a symbol (e.g., /trade BTC/USD)")
            return
            
        symbol = context.args[0].upper()
        signal = await trading_agent.generate_trade_signal(symbol)
        
        if signal:            
            response = (
                f"🎯 Trading Signal for {symbol}\n\n"
                f"Signal: {signal.recommendation.value}\n"
                f"Confidence: {signal.confidence:.2f}\n"
                f"Indicators: {', '.join(signal.indicators or ['No indicators'])}\n"
                f"Time: {signal.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}"
            )
        else:
            response = f"❌ No trading signals available for {symbol}"
            
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error in trade command: {str(e)}")
        await update.message.reply_text("❌ An error occurred while generating trading signals")

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /settings command"""
    try:
        # Get current settings
        current_settings = {
            "Trading": {
                "Min Amount": f"${settings.MIN_TRADE_AMOUNT:,.4f}",
                "Max Amount": f"${settings.MAX_TRADE_AMOUNT:,.2f}",
                "Default Timeframe": settings.DEFAULT_TIMEFRAME
            },
            "Analysis": {
                "Sentiment Model": settings.SENTIMENT_MODEL,
                "Pattern Model": settings.PATTERN_MODEL
            }
        }
        
        # Format settings message
        response = "⚙️ Current Settings:\n\n"
        for category, values in current_settings.items():
            response += f"📌 {category}:\n"
            for key, value in values.items():
                response += f"  • {key}: {value}\n"
            response += "\n"
            
        response += "Use /help to see available commands."
        
        await update.message.reply_text(response)
        
    except Exception as e:
        logger.error(f"Error in settings command: {str(e)}")
        await update.message.reply_text("❌ Failed to retrieve settings")

# Similar implementations for snipe_command, report_command, and settings_command... 