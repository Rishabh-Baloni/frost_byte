#!/usr/bin/env python3
"""
FrostByte Weather Bot - Entry Point
A powerful Telegram weather bot with webhook support for Render deployment.
"""

import os
import sys
import logging
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from bot.weather_bot import start_simple_bot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure production logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class HealthCheckHandler(BaseHTTPRequestHandler):
    """Simple HTTP handler for Render health checks"""
    
    def do_GET(self):
        if self.path == '/health' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'FrostByte Weather Bot is running!')
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress HTTP server logs to reduce noise
        pass

def run_web_server():
    """Run a simple web server for Render's port requirements"""
    port = int(os.environ.get('PORT', 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    logger.info(f"🌐 Health check server started on port {port}")
    server.serve_forever()

def main():
    """Main entry point for the bot"""
    try:
        # Check if bot token is provided
        bot_token = os.getenv('TELEGRAM_TOKEN')
        if not bot_token:
            logger.error("❌ TELEGRAM_TOKEN environment variable not set!")
            logger.error("Please set your Telegram bot token from @BotFather")
            sys.exit(1)
        
        # Check weather API key
        weather_api_key = os.getenv('WEATHER_API_KEY')
        if not weather_api_key:
            logger.error("❌ WEATHER_API_KEY environment variable not set!")
            logger.error("Please set your OpenWeatherMap API key")
            sys.exit(1)
        
        # Start web server in a separate thread for Render
        web_thread = Thread(target=run_web_server, daemon=True)
        web_thread.start()
        
        logger.info("🚀 Starting FrostByte Weather Bot...")
        
        start_simple_bot()
        
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()