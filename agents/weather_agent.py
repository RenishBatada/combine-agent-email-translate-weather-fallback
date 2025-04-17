import requests
from .base_agent import BaseAgent

class WeatherAgent(BaseAgent):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.weather_base_url = "https://api.open-meteo.com/v1/forecast"

    def _get_system_prompt(self) -> str:
        return """You are a weather information assistant. Help users get accurate 
        weather information and forecasts for their locations."""

    def can_handle(self, query: str) -> bool:
        keywords = ['weather', 'temperature', 'forecast', 'rain', 'sunny']
        return any(keyword in query.lower() for keyword in keywords)

    def get_weather_data(self, latitude: float, longitude: float) -> dict:
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": ["temperature_2m", "relative_humidity_2m", "weather_code"],
                "timezone": "auto"
            }
            response = requests.get(self.weather_base_url, params=params)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
