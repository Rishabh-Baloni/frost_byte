"""
Weather utility functions for FrostByte Weather Bot
"""

import os
import requests
import matplotlib.pyplot as plt
from datetime import datetime

def get_weather(city, units="metric"):
    """Get current weather for a city"""
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}"
    
    try:
        response = requests.get(url, timeout=10)
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

            # Air quality information
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
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"

def get_air_quality(lat, lon):
    """Get air quality for coordinates"""
    api_key = os.getenv("WEATHER_API_KEY")
    air_quality_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    
    try:
        response = requests.get(air_quality_url, timeout=10)
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
    except Exception:
        return "Air quality data unavailable."

def get_forecast(city, days=3, units="metric"):
    """Get weather forecast for a city"""
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={units}&cnt={days * 8}"
    
    try:
        response = requests.get(url, timeout=10)
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
    except Exception as e:
        return f"Error fetching forecast: {str(e)}"

def generate_weather_graph(city, units="metric"):
    """Generate weather graph from forecast data"""
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={units}&cnt=24"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            raise Exception("Could not fetch forecast data")
        
        data = response.json()
        times = [datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%m/%d %H:%M") for entry in data["list"]]
        temperatures = [entry["main"]["temp"] for entry in data["list"]]
        
        plt.figure(figsize=(12, 6))
        plt.plot(times, temperatures, marker="o", linewidth=2, markersize=4)
        plt.xticks(rotation=45, ha="right", fontsize=8)
        plt.xlabel("Time")
        plt.ylabel(f"Temperature ({'°C' if units == 'metric' else '°F'})")
        plt.title(f"24-Hour Temperature Forecast for {city}")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        graph_path = f"{city.replace(' ', '_')}_forecast.png"
        plt.savefig(graph_path, dpi=150, bbox_inches='tight')
        plt.close()
        return graph_path
    except Exception as e:
        raise Exception(f"Error generating graph: {str(e)}")

def compare_cities(city1, city2, units="metric"):
    """Compare weather between two cities"""
    try:
        weather1 = get_weather_data(city1, units)
        weather2 = get_weather_data(city2, units)
        
        if "Error" in weather1 or "Error" in weather2:
            return "Could not fetch weather data for one or both cities."
        
        unit_symbol = "°C" if units == "metric" else "°F"
        
        comparison = f"**{city1}** vs **{city2}**\n\n"
        comparison += f"🌡️ Temperature: {weather1['temp']}{unit_symbol} vs {weather2['temp']}{unit_symbol}\n"
        comparison += f"🌤️ Weather: {weather1['weather']} vs {weather2['weather']}\n"
        comparison += f"💧 Humidity: {weather1['humidity']}% vs {weather2['humidity']}%\n"
        comparison += f"💨 Wind: {weather1['wind_speed']} m/s vs {weather2['wind_speed']} m/s\n"
        
        temp_diff = abs(weather1['temp'] - weather2['temp'])
        warmer_city = city1 if weather1['temp'] > weather2['temp'] else city2
        comparison += f"\n🔥 {warmer_city} is {temp_diff:.1f}{unit_symbol} warmer"
        
        return comparison
    except Exception as e:
        return f"Error comparing cities: {str(e)}"

def get_weather_data(city, units="metric"):
    """Get weather data as dictionary"""
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}"
    
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        return {
            'temp': data["main"]["temp"],
            'weather': data["weather"][0]["description"],
            'humidity': data["main"]["humidity"],
            'wind_speed': data["wind"]["speed"]
        }
    else:
        return {"Error": "City not found"}

def get_weather_by_coords(lat, lon, units="metric"):
    """Get weather by coordinates"""
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={units}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            city_name = data["name"]
            
            unit_symbol = "°C" if units == "metric" else "°F"
            
            return (
                f"📍 Location: {city_name}\n"
                f"Weather: {weather}\n"
                f"Temperature: {temp}{unit_symbol} (Feels like: {feels_like}{unit_symbol})\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind_speed} m/s"
            )
        else:
            return "Sorry, couldn't get weather for your location."
    except Exception as e:
        return f"Error fetching weather: {str(e)}"