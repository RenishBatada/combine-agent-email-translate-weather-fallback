import os 
from dotenv import load_dotenv
load_dotenv()

import requests

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather_by_city(city: str) -> dict:
    """
    Get current weather data by city name.

    Parameters:
        city (str): City name (e.g., "London").

    Returns:
        dict: Weather data as JSON.
    """
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def get_weather_by_coordinates(lat: float, lon: float) -> dict:
    """
    Get current weather data using latitude and longitude.

    Parameters:
        lat (float): Latitude.
        lon (float): Longitude.

    Returns:
        dict: Weather data as JSON.
    """
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def get_weather_by_zip(zip_code: str, country_code: str = "us") -> dict:
    """
    Get current weather data using ZIP code and optional country code.

    Parameters:
        zip_code (str): ZIP or postal code.
        country_code (str): Country code (default is "us").

    Returns:
        dict: Weather data as JSON.
    """
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&appid={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def get_air_pollution_data(lat: float, lon: float) -> dict:
    """
    Get real-time air pollution data by coordinates.

    Parameters:
        lat (float): Latitude.
        lon (float): Longitude.

    Returns:
        dict: Air quality data as JSON.
    """
    try:
        url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    city = "Ahmedabad"
    lat = 23.0225
    lon = 72.5714
    zip_code = "380001"
    country_code = "in"

    print(f"\n🔹 Weather by City: {city}")
    print(get_weather_by_city(city))

    print(f"\n🔹 Weather by Coordinates: lat={lat}, lon={lon}")
    print(get_weather_by_coordinates(lat, lon))

    print(f"\n🔹 Weather by ZIP Code: {zip_code}, {country_code}")
    print(get_weather_by_zip(zip_code, country_code))

    print(f"\n🔹 Air Pollution by Coordinates: lat={lat}, lon={lon}")
    print(get_air_pollution_data(lat, lon))

    