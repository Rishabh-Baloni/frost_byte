# 🌤️ FrostByte Weather Bot

A powerful Telegram weather bot that provides real-time weather information, forecasts, air quality data, and weather graphs. Built with Flask webhooks for production deployment on Render.

## ✨ Features

- **Current Weather**: Get detailed weather information for any city
- **Weather Forecasts**: 3-day weather forecasts with hourly data
- **Air Quality**: Real-time air quality information
- **Weather Graphs**: Visual temperature trends with matplotlib
- **City Comparison**: Compare weather between two cities
- **Location-based Weather**: Share your location for local weather
- **Unit Conversion**: Switch between Celsius and Fahrenheit
- **Production Ready**: Webhook-based deployment on Render

## 🚀 Quick Start

### Prerequisites

1. **Telegram Bot Token**: Get from [@BotFather](https://t.me/BotFather)
2. **OpenWeatherMap API Key**: Get from [OpenWeatherMap](https://openweathermap.org/api)
3. **Render Account**: Sign up at [render.com](https://render.com)

### Deployment on Render

1. **Fork/Clone this repository** to your GitHub account

2. **Deploy to Render**:
   - Go to [dashboard.render.com](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - **Name**: `frostbyte-weather-bot`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python webhook_app.py`

3. **Set Environment Variables** in Render dashboard:
   ```
   TELEGRAM_TOKEN=your_telegram_bot_token
   WEATHER_API_KEY=your_openweathermap_api_key
   WEBHOOK_URL=https://your-app-name.onrender.com
   WEBHOOK_PORT=10000
   ```

4. **Activate Webhook**:
   - Visit: `https://your-app-name.onrender.com/set_webhook`
   - Or use: `curl -X POST https://your-app-name.onrender.com/set_webhook`

5. **Test Your Bot**:
   - Open Telegram and find your bot
   - Send `/start` to begin

## 📋 Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Start the bot | `/start` |
| `/help` | Show help message | `/help` |
| `/weather <city>` | Get current weather | `/weather London` |
| `/forecast <city>` | Get 3-day forecast | `/forecast Paris` |
| `/unit <celsius\|fahrenheit>` | Set temperature unit | `/unit celsius` |
| `/compare <city1> <city2>` | Compare cities | `/compare London Paris` |
| `/forecastgraph <city>` | Get weather graph | `/forecastgraph Tokyo` |

## 🌍 Location-based Weather

Share your location in Telegram to get weather information for your current location.

## 🏗️ Project Structure

```
FrostByte/
├── webhook_app.py          # Main Flask webhook application
├── requirements.txt        # Python dependencies
├── Procfile               # Render deployment configuration
├── render.yaml            # Render service configuration
├── README.md              # This file
└── RENDER_DEPLOYMENT.md   # Detailed deployment guide
```

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with bot info |
| `/health` | GET | Health check |
| `/webhook` | POST | Telegram webhook endpoint |
| `/set_webhook` | GET/POST | Set webhook URL |
| `/delete_webhook` | GET/POST | Remove webhook |
| `/webhook_info` | GET | Get webhook status |

## 🌐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_TOKEN` | Your Telegram bot token | Yes |
| `WEATHER_API_KEY` | OpenWeatherMap API key | Yes |
| `WEBHOOK_URL` | Your Render app URL | Yes |
| `WEBHOOK_PORT` | Port (10000 for Render) | No |

## 📊 Weather Data Sources

- **Current Weather**: OpenWeatherMap Current Weather API
- **Forecasts**: OpenWeatherMap 5-day Forecast API
- **Air Quality**: OpenWeatherMap Air Pollution API
- **Location Data**: Telegram location sharing

## 🔒 Security Features

- Environment variable protection
- HTTPS-only webhook communication
- Input validation and sanitization
- Error handling and logging

## 📈 Performance

- Asynchronous webhook processing
- Efficient API caching
- Optimized weather data parsing
- Minimal response times

## 🛠️ Technologies Used

- **Python 3.13+**
- **Flask** - Web framework
- **python-telegram-bot** - Telegram Bot API
- **requests** - HTTP client
- **matplotlib** - Weather graphs
- **python-dotenv** - Environment management

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

- **Documentation**: Check `RENDER_DEPLOYMENT.md` for detailed deployment instructions
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Telegram**: Contact the bot directly for help

## 🎯 Roadmap

- [ ] Multi-language support
- [ ] Weather alerts and notifications
- [ ] Historical weather data
- [ ] More weather visualization options
- [ ] Integration with other weather APIs

---

**Happy Weather Tracking! 🌤️**
