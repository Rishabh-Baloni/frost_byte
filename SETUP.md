# Quick Setup Guide

## 1. Get API Keys
- **Telegram Bot Token**: Message [@BotFather](https://t.me/BotFather) on Telegram
- **Weather API Key**: Sign up at [OpenWeatherMap](https://openweathermap.org/api)

## 2. Environment Setup
Copy `.env.example` to `.env` and add your keys:
```
TELEGRAM_TOKEN=your_telegram_bot_token_here
WEATHER_API_KEY=your_openweathermap_api_key_here
```

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4. Run the Bot
```bash
python main.py
```

## 5. Deploy to Render (Optional)
- Use `webhook_app.py` for production deployment
- Set environment variables in Render dashboard
- Use `render.yaml` for automatic deployment