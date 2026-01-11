from langchain_community.tools import StructuredTool
from dotenv import load_dotenv
from models import Gemini
import requests
from requests.exceptions import RequestException
from pydanticClass import GetLoactionToolInput, CityDetails
import os

load_dotenv()

def getLocationDetailApi(location:str)-> dict:
    geoCodingApiUrl = "http://api.openweathermap.org/geo/1.0/direct"
    openWeatherApiKey = ""

    try:
        openWeatherApiKey = os.getenv("OPEN_WEATHER_API_KEY")
    except Exception as e:
        print("Could not find Open Weather Api Key:", str(e))
        return f"Could not find Open Weather Api Key! Please set it in the environment variables."

    payload = {
        'q': location,
        'limit': 1,
        'appid': openWeatherApiKey
    }

    try:
        r = requests.get(geoCodingApiUrl, params=payload)
        r.raise_for_status()
        data = r.json()
        if len(data) == 0:
            return f"No location details found for '{location}'."
        
        location_info = {
            "name": data[0].get("name", ""),
            "country": data[0].get("country", ""),
            "state": data[0].get("state", ""),
            "latitude": data[0].get("lat", 0.0),
            "longitude": data[0].get("lon", 0.0)
        }

        return location_info  # Return the first matching location
    except RequestException as e:
        print("Error fetching location details:", str(e))
        return f"Error fetching location details: {str(e)}"
    
getLocationDetailTool = StructuredTool.from_function(
    func=getLocationDetailApi,
    name="get_location_details",
    description="Use this tool to get detailed information about a location including its name, country, state (if applicable), latitude, and longitude.",
    args_schema=GetLoactionToolInput
)

def getWeatherDetailApi(
    name: str,
    latitude: float,
    longitude: float
) -> dict:

    openWeatherApiUrl = "https://api.openweathermap.org/data/2.5/weather"
    openWeatherApiKey = os.getenv("OPEN_WEATHER_API_KEY")

    if not openWeatherApiKey:
        return {
            "ok": False,
            "error": "OPEN_WEATHER_API_KEY not set",
            "location": name,
            "data": None
        }

    payload = {
        "lat": latitude,
        "lon": longitude,
        "appid": openWeatherApiKey,
        "units": "metric"
    }

    try:
        r = requests.get(openWeatherApiUrl, params=payload, timeout=10)
        r.raise_for_status()
        currentWeather = r.json()

        if not currentWeather:
            return {
                "ok": False,
                "error": "No weather data returned",
                "location": name,
                "data": None
            }

        return {
            "ok": True,
            "error": None,
            "location": name,
            "coordinates": {
                "lat": latitude,
                "lon": longitude
            },
            "data": {
                "temperature": currentWeather["main"]["temp"],
                "feels_like": currentWeather["main"]["feels_like"],
                "humidity": currentWeather["main"]["humidity"],
                "pressure": currentWeather["main"]["pressure"],
                "weather": currentWeather["weather"][0]["description"],
                "wind_speed": currentWeather["wind"]["speed"],
                "clouds": currentWeather["clouds"]["all"],
                "raw": currentWeather
            }
        }

    except RequestException as e:
        return {
            "ok": False,
            "error": f"Weather API request failed: {str(e)}",
            "location": name,
            "data": None
        }



