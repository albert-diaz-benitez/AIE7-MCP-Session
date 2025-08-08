from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os
from dice_roller import DiceRoller
from weather_service import WeatherService

load_dotenv()

mcp = FastMCP("mcp-server")
client = TavilyClient(os.getenv("TAVILY_API_KEY"))
weather_service = WeatherService()

@mcp.tool()
def web_search(query: str) -> str:
    """Search the web for information about the given query"""
    search_results = client.get_search_context(query=query)
    return search_results

@mcp.tool()
def roll_dice(notation: str, num_rolls: int = 1) -> str:
    """Roll the dice with the given notation"""
    roller = DiceRoller(notation, num_rolls)
    return str(roller)

"""
Add your own tool here, and then use it through Cursor!
"""
@mcp.tool()
def weather_search(city_name: str) -> str:
    """Get current weather information for a city using the Weatherstack API"""
    weather_info = weather_service.get_weather(city_name)
    if weather_info:
        return weather_service.format_weather_report(weather_info)
    else:
        return f"Could not get weather information for {city_name}. Please check the city name and try again."

if __name__ == "__main__":
    mcp.run(transport="stdio")