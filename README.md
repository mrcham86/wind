# Wind

A simple command-line weather app that shows current conditions and a 7-day forecast for any city.

## Features

- Current temperature, humidity, and wind speed
- 7-day forecast with highs, lows, and rain probability
- Works with any city worldwide
- No API key required

## Requirements

- Python 3.10 or higher

## Usage

```bash
# Get weather for a specific city
python3 weather.py Denver

# Cities with spaces need quotes
python3 weather.py "New York"
python3 weather.py "Los Angeles"

# Default (New York) if no city provided
python3 weather.py
```

## Example Output

```
  Weather for Denver
  ────────────────────────────────────────
  Now: Clear sky
  Temperature: 35.1°F
  Humidity: 18%
  Wind: 5.0 mph

  7-Day Forecast
  ────────────────────────────────────────
  Today       50°/33°    0% rain  Partly cloudy
  Fri 12/19   68°/34°    1% rain  Overcast
  Sat 12/20   58°/41°   24% rain  Overcast
  ...
```

## Environment Variables

None required. This app uses the free [Open-Meteo API](https://open-meteo.com/) which doesn't need an API key.

## License

MIT
