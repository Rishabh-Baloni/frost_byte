import logging
import os
import requests
import asyncio
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

# Configure Flask app
app = Flask(__name__)

# Initialize bot on first request
_initialized = False

def ensure_bot_initialized():
    """Ensure the bot is initialized before processing requests"""
    global telegram_app, _initialized
    if not _initialized:
        setup_telegram_app()
        _initialized = True

# Environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Your public HTTPS URL
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8443"))

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global application instance
telegram_app = None

# Weather API functions (unchanged from original)
def get_weather(city, units):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units={units}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Current weather details
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        humidity = data["main"]["humidity"]
        visibility = data.get("visibility", 0) / 1000  # Convert to kilometers
        wind_speed = data["wind"]["speed"]

        # Sunrise and sunset times
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M:%S')
        sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime('%H:%M:%S')
        
        # Temperature unit symbol
        unit_symbol = "°C" if units == "metric" else "°F"

        # Air quality information (requires another API call)
        lat, lon = data["coord"]["lat"], data["coord"]["lon"]
        air_quality = get_air_quality(lat, lon)

        # Format and return detailed weather information
        return (
            f"Weather: {weather}\n"
            f"Temperature: {temp}{unit_symbol} (Feels like: {feels_like}{unit_symbol})\n"
            f"Min/Max Temperature: {temp_min}{unit_symbol} / {temp_max}{unit_symbol}\n"
            f"Humidity: {humidity}%\n"
            f"Visibility: {visibility} km\n"
            f"Wind Speed: {wind_speed} m/s\n"
            f"Sunrise: {sunrise}\n"
            f"Sunset: {sunset}\n\n"
            f"Air Quality: {air_quality}"
        )
    else:
        return "Sorry, I couldn't find that city. Please make sure the name is correct."

def get_air_quality(lat, lon):
    air_quality_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
    response = requests.get(air_quality_url)
    if response.status_code == 200:
        data = response.json()
        aqi = data["list"][0]["main"]["aqi"]
        
        # Map AQI levels to descriptive categories
        aqi_levels = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }
        return aqi_levels.get(aqi, "Unknown")
    else:
        return "Air quality data unavailable."

def get_forecast(city, days=3, units="metric"):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units={units}&cnt={days * 8}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast = f"Weather Forecast for {city}:\n"
        for entry in data["list"]:
            time = entry["dt_txt"]
            weather = entry["weather"][0]["description"]
            temp = entry["main"]["temp"]
            forecast += f"Time: {time} \n Weather: {weather} \n Temp: {temp}° \n\n"
        return forecast
    else:
        return "Sorry, I couldn't fetch the forecast. Please try again later."

def generate_weather_graph(forecast_data, city):
    # Extract data for plotting
    times = [entry["dt_txt"] for entry in forecast_data["list"]]
    temperatures = [entry["main"]["temp"] for entry in forecast_data["list"]]

    # Plot the data
    plt.figure(figsize=(10, 5))
    plt.plot(times, temperatures, marker="o", label="Temperature")
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.title(f"Temperature Trend for {city}")
    plt.legend()
    plt.tight_layout()

    # Save the graph to a file
    graph_path = f"{city}_forecast.png"
    plt.savefig(graph_path)
    plt.close()
    return graph_path

# Command handlers (unchanged from original)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi! I'm a weather bot. Use /weather <city> to get the weather, or /forecast <city> to get the forecast.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Here are the commands you can use:\n\n"
        "/start - Start interacting with the bot.\n"
        "/help - Show this help message with all commands.\n"
        "/weather <city> - Get the current weather for the specified city.\nExample: /weather London.\n"
        "/forecast <city> - Get a 3-day weather forecast for the specified city.\nExample: /forecast London.\n"
        "/unit <celsius|fahrenheit> - Set your preferred temperature unit.\nExample: /unit celsius.\n"
        "/compare <city1> <city2> - Compare the current weather between two cities.\nExample: /compare London Paris.\n"
        "Additionally, share your location to get the current weather for where you are."
    )
    await update.message.reply_text(help_text)

async def set_unit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) > 0:
        unit = context.args[0].lower()
        if unit in ["celsius", "fahrenheit"]:
            context.user_data["units"] = "metric" if unit == "celsius" else "imperial"
            await update.message.reply_text(f"Unit set to {unit.capitalize()}.")
        else:
            await update.message.reply_text("Please specify either 'celsius' or 'fahrenheit'.")
    else:
        await update.message.reply_text("Please specify a unit: /unit celsius or /unit fahrenheit.")

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) > 0:
        city = ' '.join(context.args)
        units = context.user_data.get("units", "metric")
        weather_info = get_weather(city, units)
        await update.message.reply_text(weather_info)
    else:
        await update.message.reply_text("Please specify a city. Example: /weather London")

async def forecast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) > 0:
        city = ' '.join(context.args)
        forecast_info = get_forecast(city)
        await update.message.reply_text(forecast_info)
    else:
        await update.message.reply_text("Please specify a city. Example: /forecast London")

async def compare(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) >= 2:
        city1, city2 = ' '.join(context.args[:-1]), context.args[-1]
        units = context.user_data.get("units", "metric")
        weather_city1 = get_weather(city1, units)
        weather_city2 = get_weather(city2, units)
        comparison_message = f"Weather Comparison:\n\n{city1}:\n{weather_city1}\n\n{city2}:\n{weather_city2}"
        await update.message.reply_text(comparison_message)
    else:
        await update.message.reply_text("Please specify two cities to compare. Example: /compare London Paris")

async def forecast_graph(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) > 0:
        city = ' '.join(context.args)
        units = context.user_data.get("units", "metric")
        
        # Get forecast data
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units={units}&cnt=24"
        response = requests.get(url)
        if response.status_code == 200:
            forecast_data = response.json()
            # Generate and send the graph
            graph_path = generate_weather_graph(forecast_data, city)
            await update.message.reply_photo(photo=open(graph_path, "rb"))
            os.remove(graph_path)  # Clean up the file after sending
        else:
            await update.message.reply_text("Sorry, I couldn't fetch the forecast data.")
    else:
        await update.message.reply_text("Please specify a city. Example: /forecastgraph London")

async def location_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    location = update.message.location
    if location:
        lat, lon = location.latitude, location.longitude
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            await update.message.reply_text(f"Weather at your location: {weather}\nTemperature: {temp}°C")
        else:
            await update.message.reply_text("Sorry, I couldn't fetch the weather for your location.")
    else:
        await update.message.reply_text("Please share your location to get weather updates.")

# Flask routes for webhook management
@app.route('/', methods=['GET'])
def home():
    """Home page with bot information"""
    return jsonify({
        'status': 'running',
        'bot_name': 'FrostByte Weather Bot',
        'webhook_url': f"{WEBHOOK_URL}/webhook" if WEBHOOK_URL else None,
        'endpoints': {
            'webhook': '/webhook',
            'set_webhook': '/set_webhook',
            'delete_webhook': '/delete_webhook',
            'webhook_info': '/webhook_info',
            'health': '/health'
        }
    }), 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhook updates from Telegram"""
    if request.method == 'POST':
        try:
            # Ensure bot is initialized
            ensure_bot_initialized()
            
            # Parse the incoming update
            update = Update.de_json(request.get_json(), telegram_app.bot)
            
            # Process the update using the application's event loop
            if telegram_app and telegram_app.bot:
                # Use the application's built-in update processing
                telegram_app.process_update(update)
                return jsonify({'status': 'ok'}), 200
            else:
                logger.error("Telegram application not properly initialized")
                return jsonify({'error': 'Bot not initialized'}), 500
                
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Method not allowed'}), 405

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    """Set the webhook URL with Telegram"""
    try:
        if not WEBHOOK_URL:
            return jsonify({'error': 'WEBHOOK_URL environment variable not set'}), 400
        
        # Ensure bot is initialized
        ensure_bot_initialized()
        
        webhook_url = f"{WEBHOOK_URL}/webhook"
        result = asyncio.run(telegram_app.bot.set_webhook(url=webhook_url))
        
        if result:
            logger.info(f"Webhook set successfully to {webhook_url}")
            return jsonify({
                'status': 'success',
                'message': f'Webhook set to {webhook_url}',
                'webhook_url': webhook_url
            }), 200
        else:
            return jsonify({'error': 'Failed to set webhook'}), 500
            
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/delete_webhook', methods=['GET', 'POST'])
def delete_webhook():
    """Remove the webhook from Telegram"""
    try:
        # Ensure bot is initialized
        ensure_bot_initialized()
        
        result = asyncio.run(telegram_app.bot.delete_webhook())
        
        if result:
            logger.info("Webhook deleted successfully")
            return jsonify({
                'status': 'success',
                'message': 'Webhook deleted successfully'
            }), 200
        else:
            return jsonify({'error': 'Failed to delete webhook'}), 500
            
    except Exception as e:
        logger.error(f"Error deleting webhook: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/webhook_info', methods=['GET'])
def webhook_info():
    """Get current webhook information from Telegram"""
    try:
        # Ensure bot is initialized
        ensure_bot_initialized()
        
        webhook_info = asyncio.run(telegram_app.bot.get_webhook_info())

        return jsonify({
            'status': 'success',
            'webhook_info': {
                'url': webhook_info.url,
                'has_custom_certificate': webhook_info.has_custom_certificate,
                'pending_update_count': webhook_info.pending_update_count,
                'last_error_date': webhook_info.last_error_date.isoformat() if webhook_info.last_error_date else None,
                'last_error_message': webhook_info.last_error_message,
                'max_connections': webhook_info.max_connections,
                'allowed_updates': webhook_info.allowed_updates
            }
        }), 200

    except Exception as e:
        logger.error(f"Error getting webhook info: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        return jsonify({
            'status': 'healthy',
            'bot_username': telegram_app.bot.username if telegram_app and telegram_app.bot else None,
            'webhook_url': f"{WEBHOOK_URL}/webhook" if WEBHOOK_URL else None
        }), 200
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return jsonify({
            'status': 'healthy',
            'bot_username': None,
            'webhook_url': f"{WEBHOOK_URL}/webhook" if WEBHOOK_URL else None
        }), 200

def setup_telegram_app():
    """Initialize the Telegram application with handlers"""
    global telegram_app
    
    telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Command handlers
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("help", help_command))
    telegram_app.add_handler(CommandHandler("weather", weather))
    telegram_app.add_handler(CommandHandler("forecast", forecast))
    telegram_app.add_handler(CommandHandler("unit", set_unit))
    telegram_app.add_handler(CommandHandler("forecastgraph", forecast_graph))
    telegram_app.add_handler(CommandHandler("compare", compare))

    # Location-based weather handler
    telegram_app.add_handler(MessageHandler(filters.LOCATION, location_weather))
    
    # Initialize the application
    asyncio.run(telegram_app.initialize())

def create_app():
    """Create and configure the Flask application"""
    # Validate environment variables
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN environment variable not set")
        exit(1)
    
    if not WEBHOOK_URL:
        logger.error("WEBHOOK_URL environment variable not set")
        exit(1)
    
    if not WEATHER_API_KEY:
        logger.error("WEATHER_API_KEY environment variable not set")
        exit(1)
    
    # Setup Telegram application
    setup_telegram_app()
    
    logger.info(f"Telegram application initialized successfully")
    logger.info(f"Webhook URL will be: {WEBHOOK_URL}/webhook")
    
    return app

if __name__ == '__main__':
    # Create and configure the app
    app = create_app()
    
    logger.info(f"Starting Flask webhook server on port {WEBHOOK_PORT}")
    
    # Run Flask app
    port = int(os.environ.get('PORT', WEBHOOK_PORT))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
