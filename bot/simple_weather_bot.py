"""FrostByte Weather Bot - Complete Implementation"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from utils.weather_utils import get_weather, get_forecast, generate_weather_graph, compare_cities, get_weather_by_coords

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Welcome to FrostByte Weather Bot!\n\n"
        "I can help you get weather information for any city.\n\n"
        "Commands:\n"
        "/weather <city> - Get current weather\n"
        "/forecast <city> - Get 3-day forecast\n"
        "/forecastgraph <city> - Get weather graph\n"
        "/compare <city1> <city2> - Compare cities\n"
        "/unit <celsius|fahrenheit> - Set temperature unit\n"
        "/help - Show this help message\n\n"
        "Just send me a city name or share your location!"
    )
    
    keyboard = [
        [InlineKeyboardButton("Current Weather", callback_data="weather")],
        [InlineKeyboardButton("Forecast", callback_data="forecast")],
        [InlineKeyboardButton("Weather Graph", callback_data="graph")],
        [InlineKeyboardButton("Compare Cities", callback_data="compare")],
        [InlineKeyboardButton("Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "FrostByte Weather Bot Help\n\n"
        "Available Commands:\n"
        "/start - Start the bot\n"
        "/weather <city> - Get current weather for a city\n"
        "/forecast <city> - Get 3-day weather forecast\n"
        "/forecastgraph <city> - Get weather graph\n"
        "/compare <city1> <city2> - Compare cities\n"
        "/unit <celsius|fahrenheit> - Set temperature unit\n"
        "/help - Show this help message\n\n"
        "Examples:\n"
        "/weather London\n"
        "/forecast New York\n"
        "/compare London Paris\n\n"
        "You can also send me a city name or share your location!"
    )
    await update.message.reply_text(help_text)

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Please provide a city name.\nExample: /weather London"
        )
        return
    
    city = " ".join(context.args)
    units = context.user_data.get('units', 'metric')
    await update.message.reply_text(f"Getting weather for {city}...")
    
    weather_info = get_weather(city, units=units)
    await update.message.reply_text(f"**Weather in {city}**\n\n{weather_info}", parse_mode='Markdown')

async def forecast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Please provide a city name.\nExample: /forecast London"
        )
        return
    
    city = " ".join(context.args)
    units = context.user_data.get('units', 'metric')
    await update.message.reply_text(f"Getting forecast for {city}...")
    
    forecast_info = get_forecast(city, units=units)
    await update.message.reply_text(f"**3-Day Forecast for {city}**\n\n{forecast_info}", parse_mode='Markdown')

async def forecastgraph_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Please provide a city name.\nExample: /forecastgraph London"
        )
        return
    
    city = " ".join(context.args)
    units = context.user_data.get('units', 'metric')
    await update.message.reply_text(f"Generating weather graph for {city}...")
    
    try:
        graph_path = generate_weather_graph(city, units=units)
        with open(graph_path, 'rb') as photo:
            await update.message.reply_photo(photo=photo, caption=f"Weather forecast graph for {city}")
        os.remove(graph_path)
    except Exception as e:
        await update.message.reply_text(f"Sorry, couldn't generate graph: {str(e)}")

async def compare_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "Please provide two city names.\nExample: /compare London Paris"
        )
        return
    
    city1 = context.args[0]
    city2 = " ".join(context.args[1:])
    units = context.user_data.get('units', 'metric')
    await update.message.reply_text(f"Comparing weather between {city1} and {city2}...")
    
    comparison = compare_cities(city1, city2, units=units)
    await update.message.reply_text(f"**Weather Comparison**\n\n{comparison}", parse_mode='Markdown')

async def unit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        current_unit = context.user_data.get('units', 'metric')
        unit_name = 'Celsius' if current_unit == 'metric' else 'Fahrenheit'
        await update.message.reply_text(
            f"Current unit: {unit_name}\n\nTo change: /unit celsius or /unit fahrenheit"
        )
        return
    
    unit_arg = context.args[0].lower()
    if unit_arg in ['celsius', 'c', 'metric']:
        context.user_data['units'] = 'metric'
        await update.message.reply_text("Temperature unit set to Celsius")
    elif unit_arg in ['fahrenheit', 'f', 'imperial']:
        context.user_data['units'] = 'imperial'
        await update.message.reply_text("Temperature unit set to Fahrenheit")
    else:
        await update.message.reply_text("Please use: /unit celsius or /unit fahrenheit")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text.strip()
    
    if len(city) < 2 or any(char.isdigit() for char in city):
        await update.message.reply_text(
            "Please send a valid city name or use /help for available commands."
        )
        return
    
    units = context.user_data.get('units', 'metric')
    await update.message.reply_text(f"Getting weather for {city}...")
    weather_info = get_weather(city, units=units)
    await update.message.reply_text(f"**Weather in {city}**\n\n{weather_info}", parse_mode='Markdown')

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    lat, lon = location.latitude, location.longitude
    units = context.user_data.get('units', 'metric')
    
    await update.message.reply_text("Getting weather for your location...")
    
    try:
        weather_info = get_weather_by_coords(lat, lon, units=units)
        await update.message.reply_text(f"**Weather at your location**\n\n{weather_info}", parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"Sorry, couldn't get weather for your location: {str(e)}")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "weather":
        await query.edit_message_text(
            "To get current weather, use:\n/weather <city name>\n\nExample: /weather London"
        )
    elif query.data == "forecast":
        await query.edit_message_text(
            "To get weather forecast, use:\n/forecast <city name>\n\nExample: /forecast New York"
        )
    elif query.data == "graph":
        await query.edit_message_text(
            "To get weather graph, use:\n/forecastgraph <city name>\n\nExample: /forecastgraph Tokyo"
        )
    elif query.data == "compare":
        await query.edit_message_text(
            "To compare cities, use:\n/compare <city1> <city2>\n\nExample: /compare London Paris"
        )
    elif query.data == "help":
        help_text = (
            "FrostByte Weather Bot Help\n\n"
            "Available Commands:\n"
            "/start - Start the bot\n"
            "/weather <city> - Get current weather\n"
            "/forecast <city> - Get 3-day forecast\n"
            "/forecastgraph <city> - Get weather graph\n"
            "/compare <city1> <city2> - Compare cities\n"
            "/unit <celsius|fahrenheit> - Set temperature unit\n"
            "/help - Show this help\n\n"
            "You can also send me a city name or share your location!"
        )
        await query.edit_message_text(help_text)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.message:
        await update.message.reply_text(
            "Sorry, something went wrong. Please try again later."
        )

def start_simple_bot():
    bot_token = os.getenv('TELEGRAM_TOKEN')
    if not bot_token:
        logger.error("TELEGRAM_TOKEN not found in environment variables")
        return
    
    logger.info("Starting FrostByte Weather Bot...")
    
    application = Application.builder().token(bot_token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("weather", weather_command))
    application.add_handler(CommandHandler("forecast", forecast_command))
    application.add_handler(CommandHandler("forecastgraph", forecastgraph_command))
    application.add_handler(CommandHandler("compare", compare_command))
    application.add_handler(CommandHandler("unit", unit_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))
    application.add_error_handler(error_handler)
    
    logger.info("Bot handlers registered successfully")
    
    try:
        application.run_polling(drop_pending_updates=True)
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        raise