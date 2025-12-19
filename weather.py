#!/usr/bin/env python3
"""Fetch current weather and 7-day forecast for any city."""

import json
import sys
import urllib.request
import urllib.parse
from datetime import datetime


def get_coordinates(city: str) -> tuple[float, float, str]:
    """Get latitude/longitude for a city using Open-Meteo geocoding API."""
    params = urllib.parse.urlencode({"name": city, "count": 1})
    url = f"https://geocoding-api.open-meteo.com/v1/search?{params}"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())

    if "results" not in data or not data["results"]:
        raise ValueError(f"City not found: {city}")

    result = data["results"][0]
    return result["latitude"], result["longitude"], result["name"]


def get_weather(lat: float, lon: float) -> dict:
    """Fetch current weather and 7-day forecast from Open-Meteo API."""
    params = urllib.parse.urlencode({
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "timezone": "auto"
    })
    url = f"https://api.open-meteo.com/v1/forecast?{params}"

    with urllib.request.urlopen(url) as response:
        return json.loads(response.read())


def weather_description(code: int) -> str:
    """Convert WMO weather code to human-readable description."""
    codes = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
        80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
        95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
    }
    return codes.get(code, "Unknown")


def format_day(date_str: str) -> str:
    """Format date string as day name."""
    date = datetime.strptime(date_str, "%Y-%m-%d")
    if date.date() == datetime.now().date():
        return "Today"
    return date.strftime("%a %m/%d")


def main():
    city = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "New York"

    try:
        lat, lon, name = get_coordinates(city)
        weather = get_weather(lat, lon)
        current = weather["current"]
        daily = weather["daily"]

        print(f"\n  Weather for {name}")
        print(f"  {'─' * 40}")
        print(f"  Now: {weather_description(current['weather_code'])}")
        print(f"  Temperature: {current['temperature_2m']}°F")
        print(f"  Humidity: {current['relative_humidity_2m']}%")
        print(f"  Wind: {current['wind_speed_10m']} mph")

        print(f"\n  7-Day Forecast")
        print(f"  {'─' * 40}")
        for i in range(7):
            day = format_day(daily["time"][i])
            high = int(daily["temperature_2m_max"][i])
            low = int(daily["temperature_2m_min"][i])
            precip = daily["precipitation_probability_max"][i]
            desc = weather_description(daily["weather_code"][i])
            print(f"  {day:<10} {high:>3}°/{low:<3}°  {precip:>3}% rain  {desc}")
        print()

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to fetch weather: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
