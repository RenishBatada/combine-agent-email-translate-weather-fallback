import requests
from .base_agent import BaseAgent


class WeatherAgent(BaseAgent):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.weather_base_url = "https://api.open-meteo.com/v1/forecast"

    def _get_system_prompt(self) -> str:
        return """You are a weather information assistant. Provide ONLY current weather conditions when asked.

Rules:
1. Only provide current temperature, conditions, and basic weather info
2. Do not provide historical data or long-term forecasts unless specifically asked
3. If location is missing, ask for it
4. If the query is not about weather, respond with: "I can only help with weather-related queries."

Example response:
Current weather in [City]:
Temperature: 25°C
Conditions: Sunny
Humidity: 60%

also print nice format response
"""

    def get_weather_data(self, latitude: float, longitude: float) -> dict:
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": ["temperature_2m", "relative_humidity_2m", "weather_code"],
                "timezone": "auto",
            }
            response = requests.get(self.weather_base_url, params=params)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
