import logging

# Global variable to store current user ID
current_user_id = None

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city using wttr.in API.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error message.
    """
    try:
        logger.info(f"Getting weather for city: {city}")

        # Import and use weather utility module
        from .utils.weather_utils import fetch_weather_data_sync, format_weather_response

        # Get weather data from wttr.in API
        weather_data = fetch_weather_data_sync(city)

        if weather_data["status"] == "success":
            # Format the response nicely
            formatted_response = format_weather_response(weather_data)
            result = {
                "status": "success",
                "results": formatted_response
            }
        else:
            # Return error message
            result = {
                "status": "error",
                "error_message": weather_data.get("error_message", "天氣查詢失敗")
            }

        logger.info(f"Weather query completed for {city}: {result['status']}")
        return result

    except Exception as e:
        logger.error(f"Error getting weather for {city}: {str(e)}")
        return {
            "status": "error",
            "error_message": f"Failed to get weather for {city}: {str(e)}"
        }
