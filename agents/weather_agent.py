from tool.whether import get_weather_by_city, get_weather_by_coordinates, get_weather_by_zip, get_air_pollution_data
from .base_agent import BaseAgent
from typing import Dict, Any, Optional, List, Tuple
import json


class WeatherAgent(BaseAgent):
    def __init__(self, api_key: str):
        super().__init__(api_key)

    def _get_system_prompt(self) -> str:
        return """You are a weather information assistant. Your task is to extract location information from user queries and provide real-time weather data.

Rules:
1. For any weather-related query, you must:
   a) Extract the location (city, coordinates, or ZIP code)
   b) Return ONLY a JSON response in this format:
      {
        "location_type": "city|coordinates|zip",
        "location": "city_name" or {"lat": float, "lon": float} or "zip_code",
        "country_code": "country_code_if_zip" (only for zip queries)
      }
2. If no location is provided in the query, ask the user for a location
3. If the query is not about weather, return: {"error": "not_weather_query"}

Example responses:
For "What's the weather in London?":
{"location_type": "city", "location": "London"}

For "Check weather at 40.7128,-74.0060":
{"location_type": "coordinates", "location": {"lat": 40.7128, "lon": -74.0060}}

For "Get weather for ZIP 10001, US":
{"location_type": "zip", "location": "10001", "country_code": "us"}
"""

    def _kelvin_to_celsius(self, kelvin: float) -> float:
        return round(kelvin - 273.15, 2)

    def _kelvin_to_fahrenheit(self, kelvin: float) -> float:
        return round((kelvin - 273.15) * 9/5 + 32, 2)

    def _format_weather_response(self, data: Dict[str, Any]) -> str:
        if "error" in data:
            return f" Error getting weather data: {data['error']}"

        temp_k = data["main"]["temp"]
        temp_c = self._kelvin_to_celsius(temp_k)
        temp_f = self._kelvin_to_fahrenheit(temp_k)
        
        response = [
            f" Current weather in {data['name']}:",
            f"- Temperature: {temp_c}°C ({temp_f}°F)",
            f"- Conditions: {data['weather'][0]['description'].capitalize()}",
            f"- Humidity: {data['main']['humidity']}%",
            f"- Wind: {data['wind']['speed']} m/s"
        ]
        return "\n".join(response)

    def _format_air_quality_response(self, data: Dict[str, Any]) -> str:
        if "error" in data:
            return f" Error getting air quality data: {data['error']}"

        aqi_levels = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }
        
        aqi = data["list"][0]["main"]["aqi"]
        components = data["list"][0]["components"]
        
        response = [
            " Current Air Quality:",
            f"- Air Quality Index: {aqi_levels.get(aqi, 'Unknown')}",
            f"- CO: {components.get('co', 'N/A')} μg/m³",
            f"- NO2: {components.get('no2', 'N/A')} μg/m³",
            f"- PM2.5: {components.get('pm2_5', 'N/A')} μg/m³",
            f"- PM10: {components.get('pm10', 'N/A')} μg/m³"
        ]
        return "\n".join(response)

    def process(self, query: str, chat_history: List[Tuple] = None) -> str:
        """Process weather-related queries using real-time data."""
        # First, use LLM to extract location information
        messages = [
            {"role": "system", "content": self._get_system_prompt()},
            {"role": "user", "content": query}
        ]
        
        try:
            response = self.llm.invoke(messages)
            location_data = json.loads(response.content)
            
            if "error" in location_data:
                return "I can only help with weather-related queries. Please ask about weather or air quality for a specific location."
                
            if location_data["location_type"] == "city":
                data = get_weather_by_city(location_data["location"])
                return self._format_weather_response(data)
                
            elif location_data["location_type"] == "coordinates":
                coords = location_data["location"]
                if "air" in query.lower() and ("quality" in query.lower() or "pollution" in query.lower()):
                    data = get_air_pollution_data(coords["lat"], coords["lon"])
                    return self._format_air_quality_response(data)
                else:
                    data = get_weather_by_coordinates(coords["lat"], coords["lon"])
                    return self._format_weather_response(data)
                    
            elif location_data["location_type"] == "zip":
                data = get_weather_by_zip(location_data["location"], location_data.get("country_code", "us"))
                return self._format_weather_response(data)
                
            return "I couldn't understand the location in your query. Please specify a city, coordinates, or ZIP code."
            
        except Exception as e:
            return f" Error processing your request: {str(e)}"
