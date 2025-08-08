import requests
import json
from typing import Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class WeatherInfo:
    """Data class to hold weather information"""
    city: str
    country: str
    temperature: int
    weather_description: str
    humidity: int
    wind_speed: int
    wind_direction: str
    pressure: int
    feels_like: int
    visibility: int
    uv_index: int
    local_time: str
    weather_icon: str


class WeatherService:
    """Service class to interact with Weatherstack API"""
    
    def __init__(self, api_key: str = "b3d490c8de0e3ede82dea4a6a3978603"):
        """
        Initialize the weather service with API key
        
        Args:
            api_key: Weatherstack API key
        """
        self.api_key = api_key
        self.base_url = "http://api.weatherstack.com/current"
    
    def get_weather(self, city_name: str) -> Optional[WeatherInfo]:
        """
        Get current weather information for a city
        
        Args:
            city_name: Name of the city to get weather for
            
        Returns:
            WeatherInfo object with weather data or None if request fails
        """
        try:
            # Prepare the request parameters
            params = {
                'access_key': self.api_key,
                'query': city_name
            }
            
            # Make the API request
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Parse the JSON response
            data = response.json()
            
            # Check if the request was successful
            if 'error' in data:
                print(f"API Error: {data['error']['info']}")
                return None
            
            # Extract weather information
            location = data['location']
            current = data['current']
            
            # Create and return WeatherInfo object
            weather_info = WeatherInfo(
                city=location['name'],
                country=location['country'],
                temperature=current['temperature'],
                weather_description=current['weather_descriptions'][0],
                humidity=current['humidity'],
                wind_speed=current['wind_speed'],
                wind_direction=current['wind_dir'],
                pressure=current['pressure'],
                feels_like=current['feelslike'],
                visibility=current['visibility'],
                uv_index=current['uv_index'],
                local_time=location['localtime'],
                weather_icon=current['weather_icons'][0] if current['weather_icons'] else ""
            )
            
            return weather_info
            
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
        except (KeyError, IndexError) as e:
            print(f"Data parsing error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def get_weather_raw(self, city_name: str) -> Optional[Dict[str, Any]]:
        """
        Get raw weather data from the API
        
        Args:
            city_name: Name of the city to get weather for
            
        Returns:
            Raw JSON response as dictionary or None if request fails
        """
        try:
            params = {
                'access_key': self.api_key,
                'query': city_name
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if 'error' in data:
                print(f"API Error: {data['error']['info']}")
                return None
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def format_weather_report(self, weather_info: WeatherInfo) -> str:
        """
        Format weather information into a readable report
        
        Args:
            weather_info: WeatherInfo object
            
        Returns:
            Formatted weather report string
        """
        if not weather_info:
            return "Weather information not available."
        
        report = f"""
🌤️  Weather Report for {weather_info.city}, {weather_info.country}
📍 Local Time: {weather_info.local_time}

🌡️  Temperature: {weather_info.temperature}°C (Feels like: {weather_info.feels_like}°C)
☁️  Conditions: {weather_info.weather_description}
💧 Humidity: {weather_info.humidity}%
💨 Wind: {weather_info.wind_speed} km/h {weather_info.wind_direction}
🌡️  Pressure: {weather_info.pressure} mb
👁️  Visibility: {weather_info.visibility} km
☀️  UV Index: {weather_info.uv_index}
        """
        
        return report.strip()


# Example usage
if __name__ == "__main__":
    # Create weather service instance
    weather_service = WeatherService()
    
    # Test with a city
    city = "New York"
    weather = weather_service.get_weather(city)
    
    if weather:
        print(weather_service.format_weather_report(weather))
    else:
        print(f"Could not get weather for {city}") 