#!/usr/bin/env python3
"""
Test script for the WeatherService class
"""

from weather_service import WeatherService

def test_weather_service():
    """Test the weather service with different cities"""
    
    # Create weather service instance
    weather_service = WeatherService()
    
    # Test cities
    test_cities = ["New York", "London", "Tokyo", "Paris", "Sydney"]
    
    print("🌤️  Testing Weather Service")
    print("=" * 50)
    
    for city in test_cities:
        print(f"\n📍 Testing weather for: {city}")
        print("-" * 30)
        
        # Get weather information
        weather = weather_service.get_weather(city)
        
        if weather:
            print(weather_service.format_weather_report(weather))
        else:
            print(f"❌ Could not get weather for {city}")
        
        print()

if __name__ == "__main__":
    test_weather_service() 