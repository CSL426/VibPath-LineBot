"""
Weather utility functions for fetching weather data using wttr.in API.
"""
import logging
import aiohttp
import asyncio
from typing import Dict, Any

logger = logging.getLogger(__name__)


async def fetch_weather_data(city: str) -> Dict[str, Any]:
    """
    Fetch weather data for a given city using wttr.in API.

    Args:
        city (str): Name of the city

    Returns:
        dict: Weather data with status and results
    """
    try:
        logger.info(f"Fetching weather data for {city}")

        # Clean city name
        city_clean = city.strip()

        # Use wttr.in API for real weather data
        url = f"https://wttr.in/{city_clean}?format=j1"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()

                    # Extract current weather information
                    current = data['current_condition'][0]
                    location = data['nearest_area'][0]

                    temp_c = current['temp_C']
                    temp_f = current['temp_F']
                    desc = current['weatherDesc'][0]['value']
                    humidity = current['humidity']
                    wind_speed = current['windspeedKmph']
                    wind_dir = current['winddir16Point']
                    feels_like = current['FeelsLikeC']

                    area_name = location.get('areaName', [{'value': city}])[0]['value']
                    country = location.get('country', [{'value': ''}])[0]['value']

                    weather_data = {
                        "city": area_name,
                        "country": country,
                        "temperature": f"{temp_c}°C",
                        "temperature_f": f"{temp_f}°F",
                        "feels_like": f"{feels_like}°C",
                        "condition": desc,
                        "humidity": f"{humidity}%",
                        "wind_speed": f"{wind_speed} km/h",
                        "wind_direction": wind_dir
                    }

                    return {
                        "status": "success",
                        "data": weather_data
                    }
                else:
                    return {
                        "status": "error",
                        "error_message": f"無法取得 {city} 的天氣資訊，請檢查城市名稱是否正確。"
                    }

    except asyncio.TimeoutError:
        logger.error(f"Timeout error for {city}")
        return {
            "status": "error",
            "error_message": f"查詢 {city} 天氣時發生超時，請稍後再試。"
        }
    except Exception as e:
        logger.error(f"Error fetching weather for {city}: {str(e)}")
        return {
            "status": "error",
            "error_message": f"查詢 {city} 天氣時發生錯誤：{str(e)}"
        }


def fetch_weather_data_sync(city: str) -> Dict[str, Any]:
    """
    Synchronous wrapper for the async fetch_weather_data function.
    """
    return asyncio.run(fetch_weather_data(city))


def format_weather_response(weather_data: Dict[str, Any]) -> str:
    """
    Format weather data into a user-friendly response.

    Args:
        weather_data (dict): Raw weather data

    Returns:
        str: Formatted weather response
    """
    if weather_data.get("status") == "success":
        data = weather_data.get("data", {})
        city_name = data.get('city')
        country = data.get('country')
        location = f"{city_name}, {country}" if country else city_name

        return f"""🌤️ {location} 天氣資訊：
📊 天氣：{data.get('condition')}
🌡️ 溫度：{data.get('temperature')} ({data.get('temperature_f')})
🌡️ 體感：{data.get('feels_like')}
💧 濕度：{data.get('humidity')}
🌬️ 風速：{data.get('wind_speed')} ({data.get('wind_direction')})"""
    else:
        return f"❌ {weather_data.get('error_message', '天氣查詢失敗')}"