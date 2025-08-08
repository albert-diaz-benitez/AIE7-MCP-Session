#!/usr/bin/env python3
import os
from dotenv import load_dotenv

load_dotenv()

"""
Test script for the WeatherService class
"""

from weather_service import WeatherService

def test_weather_service():
    """Test the weather service with different cities"""
    
    # Create weather service instance
    weather_service = WeatherService(os.getenv("WEATHER_API_KEY"))
    
    # Test city
    test_city = "Barcelona"

    print("🌤️  Testing Weather Service")
    print("=" * 50)
    print(f"\n📍 Testing weather for: {test_city}")
    print("-" * 30)
    
    # Get weather information
    weather = weather_service.get_weather(test_city)
    
    if weather:
        print(weather_service.format_weather_report(weather))
    else:
        print(f"❌ Could not get weather for {test_city}")
    
    print()

if __name__ == "__main__":
    test_weather_service() 