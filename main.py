import logging
from telegram import Update
from datetime import datetime
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()

# Your API keys
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define a function to get weather info from OpenWeatherMap
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
    
# Function to get air quality information
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

# Define a function to get weather forecasts (3-day or 7-day)
def get_forecast(city, days=3, units="metric"):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units={units}&cnt={days * 8}"  # 8 data points per day
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

# Function to generate a graph for weather data
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

# Define the start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi! I’m a weather bot. Use /weather <city> to get the weather, or /forecast <city> to get the forecast.")

# Define the help command
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

# Default to metric units if user hasn't set preference
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

# Define the weather command
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) > 0:
        city = ' '.join(context.args)
        units = context.user_data.get("units", "metric")  # Default to metric if no preference set
        weather_info = get_weather(city, units)
        await update.message.reply_text(weather_info)
    else:
        await update.message.reply_text("Please specify a city. Example: /weather London")

# Define the forecast command
async def forecast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) > 0:
        city = ' '.join(context.args)
        forecast_info = get_forecast(city)
        await update.message.reply_text(forecast_info)
    else:
        await update.message.reply_text("Please specify a city. Example: /forecast London")

# Define the compare command
async def compare(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) >= 2:
        # Get the cities from the command arguments
        city1, city2 = ' '.join(context.args[:-1]), context.args[-1]
        units = context.user_data.get("units", "metric")  # Default to metric if no preference set
        # Get weather information for both cities
        weather_city1 = get_weather(city1, units)
        weather_city2 = get_weather(city2, units)
        # Format the comparison message
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

# Handle user location for weather
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

# Main function to set up handlers
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(CommandHandler("forecast", forecast))
    app.add_handler(CommandHandler("unit", set_unit))
    app.add_handler(CommandHandler("forecastgraph", forecast_graph))
    app.add_handler(CommandHandler("compare", compare))

    # Location-based weather handler
    app.add_handler(MessageHandler(filters.LOCATION, location_weather))

    # Start the Bot
    app.run_polling()

if __name__ == "__main__":
    main()