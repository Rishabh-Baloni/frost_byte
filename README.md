# ❄️ FrostByte Weather Bot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://telegram.org/)
[![Deploy to Render](https://img.shields.io/badge/Deploy-Render-purple.svg)](https://render.com)

A comprehensive Telegram weather bot with advanced features including weather graphs, city comparisons, and location-based forecasts. Optimized for deployment on Render's free tier.

## 🎯 Quick Demo

1. **Send a city name** → Get instant weather report
2. **Share location** → Get weather for your current location  
3. **Use `/forecast London`** → Get 3-day weather forecast
4. **Use `/compare London Paris`** → Compare weather between cities
5. **Use `/forecastgraph Tokyo`** → Get visual weather graph

## 🚀 Features

### 🌤️ Weather Information
- **Current Weather**: Temperature, humidity, wind speed, visibility
- **Detailed Reports**: Feels-like temperature, min/max temps, sunrise/sunset
- **Air Quality**: Real-time air quality index with descriptive categories
- **Location Support**: Share your location for instant local weather

### 📊 Advanced Features
- **3-Day Forecasts**: Detailed weather predictions with timestamps
- **Weather Graphs**: Visual temperature charts with matplotlib
- **City Comparisons**: Side-by-side weather comparison between cities
- **Unit Conversion**: Switch between Celsius and Fahrenheit
- **Interactive Buttons**: Easy-to-use inline keyboard interface

### 🔧 Technical Features
- **Auto-Wake System**: Prevents Render free tier from sleeping
- **Health Checks**: HTTP endpoint for deployment monitoring
- **Error Handling**: Comprehensive error management and user feedback
- **Production Logging**: Structured logging for debugging and monitoring

## 🛠️ Technology Stack

- **Python 3.8+**
- **python-telegram-bot 21.7** - Telegram Bot API wrapper
- **requests 2.32.3** - HTTP requests for weather API
- **matplotlib 3.9.2** - Weather graph generation
- **python-dotenv 1.1.0** - Environment variable management
- **Flask 3.0.0** - Web server for health checks

## 📋 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/Rishabh-Baloni/frost_byte.git
cd frost_byte
```

### 2. Local Development Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Copy `.env.example` to `.env` and configure:
```env
TELEGRAM_TOKEN=your_telegram_bot_token_from_botfather
WEATHER_API_KEY=your_openweathermap_api_key
WEBHOOK_URL=https://your-app-name.onrender.com  # For production only
WEBHOOK_PORT=10000  # For production only
```

### 4. Get API Keys

**Telegram Bot Token:**
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create new bot with `/newbot`
3. Copy the provided token

**OpenWeatherMap API Key:**
1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get free API key from your dashboard
3. Copy the API key

### 5. Run Locally
```bash
python webhook_app.py
```

## 🌐 Deploy to Render

### 1. Connect Repository
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" → "Web Service"
3. Connect your GitHub repository

### 2. Configure Service
```yaml
# Build Command
pip install -r requirements.txt

# Start Command
python webhook_app.py

# Environment Variables
TELEGRAM_TOKEN=your_telegram_bot_token_here
WEATHER_API_KEY=your_openweathermap_api_key_here
WEBHOOK_URL=https://your-app-name.onrender.com
WEBHOOK_PORT=10000
```

### 3. Advanced Settings
- **Plan**: Free
- **Region**: Choose closest to your users
- **Runtime**: Python 3
- **Auto-Deploy**: Yes (recommended)

## 🤖 Bot Commands

### Basic Commands
- `/start` - Initialize bot and see welcome message with interactive buttons
- `/help` - Show detailed help and all available commands

### Weather Commands
```
/weather <city>           # Get current weather for any city
/forecast <city>          # Get 3-day weather forecast
/forecastgraph <city>     # Generate visual weather graph
/compare <city1> <city2>  # Compare weather between two cities
/unit <celsius|fahrenheit> # Set temperature unit preference
```

### Usage Examples
```
/weather London
/forecast New York
/forecastgraph Tokyo
/compare London Paris
/unit fahrenheit
```

### Interactive Features
- **Send city name**: Get instant weather (no command needed)
- **Share location**: Get weather for your current coordinates
- **Inline buttons**: Use interactive menu from `/start` command

## 🔧 Architecture

### Weather Data Processing
```python
# Comprehensive weather information
- Current conditions with detailed metrics
- Air quality index with health categories
- Sunrise/sunset times with local timezone
- Wind speed and visibility data
```

### Auto-Wake System
```python
# Prevents Render free tier from sleeping
def run_web_server():
    """HTTP health check endpoint"""
    # Lightweight server on port 10000
    # Responds to /health and / endpoints
```

### Error Handling
```python
# Comprehensive error management
- API timeout handling (10 second limit)
- Invalid city name detection
- Network error recovery
- User-friendly error messages
```

## 📊 Features Overview

### Weather Information
- **Temperature**: Current, feels-like, min/max with unit conversion
- **Conditions**: Weather description, humidity, visibility
- **Wind**: Speed and direction information
- **Air Quality**: AQI with descriptive categories (Good/Fair/Poor)
- **Astronomy**: Sunrise and sunset times

### Advanced Features
- **Forecasts**: 3-day predictions with 3-hour intervals
- **Graphs**: Temperature trend visualization with matplotlib
- **Comparisons**: Side-by-side city weather analysis
- **Location**: GPS coordinate-based weather lookup
- **Units**: Celsius/Fahrenheit temperature switching

## 🐛 Troubleshooting

### Common Issues

**1. Bot Not Responding**
```bash
# Check environment variables
echo $TELEGRAM_TOKEN
echo $WEATHER_API_KEY

# Verify bot token with BotFather
# Check Render deployment logs
```

**2. Weather API Errors**
```bash
# Verify API key is active
# Check OpenWeatherMap quota limits
# Ensure city names are spelled correctly
```

**3. Graph Generation Fails**
```bash
# Check matplotlib dependencies
# Verify sufficient memory on Render
# Check forecast data availability
```

**4. Location Services**
```bash
# Ensure location sharing is enabled
# Check coordinate format validity
# Verify API supports coordinate lookup
```

## 🚀 Deployment Status

✅ **Production Ready**
- Telegram Bot API v21.7 compatibility confirmed
- OpenWeatherMap API integration tested
- Render free tier optimization complete
- Auto-wake system implemented
- Health check endpoints active
- Error handling and logging configured

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Rishabh Baloni**
- GitHub: [@Rishabh-Baloni](https://github.com/Rishabh-Baloni)
- Telegram: [@your-telegram](https://t.me/your-telegram)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⭐ Support

If you found this project helpful, please give it a ⭐ on GitHub!

---

**Built with ❄️ for comprehensive weather information on Telegram**
