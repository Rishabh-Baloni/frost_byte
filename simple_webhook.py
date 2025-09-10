import logging
import os
import requests
import threading
import time
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

# Configure Flask app
app = Flask(__name__)

# Environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8443"))

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Simple weather functions
def get_weather(city, units="metric"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units={units}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        unit_symbol = "°C" if units == "metric" else "°F"
        return f"Weather: {weather}\nTemperature: {temp}{unit_symbol}"
    else:
        return "Sorry, I couldn't find that city."

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, json=data)

def process_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    
    if text.startswith("/start"):
        send_message(chat_id, "Hi! I'm a weather bot. Use /weather <city> to get weather.")
    
    elif text.startswith("/help"):
        help_text = (
            "Commands:\n"
            "/weather <city> - Get weather\n"
            "/unit celsius - Set to Celsius\n"
            "/unit fahrenheit - Set to Fahrenheit\n"
            "/compare <city1> <city2> - Compare cities"
        )
        send_message(chat_id, help_text)
    
    elif text.startswith("/weather"):
        parts = text.split()
        if len(parts) > 1:
            city = " ".join(parts[1:])
            weather_info = get_weather(city)
            send_message(chat_id, weather_info)
        else:
            send_message(chat_id, "Please specify a city. Example: /weather London")
    
    elif text.startswith("/unit"):
        parts = text.split()
        if len(parts) > 1:
            unit = parts[1].lower()
            if unit in ["celsius", "fahrenheit"]:
                send_message(chat_id, f"✅ Unit set to {unit.capitalize()} for this session.")
            else:
                send_message(chat_id, "❌ Please specify either 'celsius' or 'fahrenheit'.")
        else:
            send_message(chat_id, "❌ Please specify a unit: /unit celsius or /unit fahrenheit.")
    
    elif text.startswith("/compare"):
        parts = text.split()
        if len(parts) >= 3:
            city1, city2 = parts[1], parts[2]
            weather1 = get_weather(city1)
            weather2 = get_weather(city2)
            comparison = f"🌤️ Weather Comparison\n\n📍 {city1.title()}:\n{weather1}\n\n📍 {city2.title()}:\n{weather2}"
            send_message(chat_id, comparison)
        else:
            send_message(chat_id, "❌ Please specify two cities. Example: /compare London Paris")
    
    else:
        # Try to get weather for city name directly
        if text and not text.startswith("/"):
            weather_info = get_weather(text)
            send_message(chat_id, weather_info)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'running',
        'bot_name': 'FrostByte Weather Bot',
        'webhook_url': f"{WEBHOOK_URL}/webhook" if WEBHOOK_URL else None
    }), 200

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = request.get_json()
        if update and "message" in update:
            message = update["message"]
            logger.info(f"Received message: {message.get('text', 'N/A')}")
            process_message(message)
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    try:
        webhook_url = f"{WEBHOOK_URL}/webhook"
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
        data = {"url": webhook_url}
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            logger.info(f"Webhook set successfully to {webhook_url}")
            return jsonify({
                'status': 'success',
                'message': f'Webhook set to {webhook_url}'
            }), 200
        else:
            return jsonify({'error': 'Failed to set webhook'}), 500
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

def auto_wake():
    """Auto-wake function to prevent Render free tier from sleeping"""
    while True:
        try:
            time.sleep(840)  # 14 minutes
            if WEBHOOK_URL:
                requests.get(f"{WEBHOOK_URL}/health", timeout=10)
                logger.info("Auto-wake ping sent")
        except Exception as e:
            logger.error(f"Auto-wake error: {e}")

if __name__ == '__main__':
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
    
    # Start auto-wake system
    wake_thread = threading.Thread(target=auto_wake, daemon=True)
    wake_thread.start()
    logger.info("Auto-wake system started")
    
    logger.info("Starting simple webhook server")
    
    # Run Flask app
    port = int(os.environ.get('PORT', WEBHOOK_PORT))
    app.run(host='0.0.0.0', port=port, debug=False)