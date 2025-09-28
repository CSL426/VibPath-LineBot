"""
Static URL management for LINE Bot assets.
Provides utilities for managing static resources like images, Rich Menu assets, etc.
"""
import os
from typing import Optional


class StaticURLManager:
    """Manages URLs for static assets"""

    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize static URL manager.

        Args:
            base_url: Base URL for static assets (e.g., CDN URL)
        """
        self.base_url = base_url or os.getenv("STATIC_BASE_URL", "")

    def get_image_url(self, image_path: str) -> str:
        """
        Get full URL for image asset.

        Args:
            image_path: Relative path to image

        Returns:
            str: Full image URL
        """
        if self.base_url:
            return f"{self.base_url.rstrip('/')}/static/images/{image_path}"
        else:
            # Fallback to placeholder or local path
            return f"https://via.placeholder.com/1024x640/CCCCCC/FFFFFF?text={image_path.replace('/', '+')}"

    def get_rich_menu_url(self, menu_name: str) -> str:
        """
        Get URL for Rich Menu image.

        Args:
            menu_name: Rich Menu image name

        Returns:
            str: Rich Menu image URL
        """
        if self.base_url:
            return f"{self.base_url.rstrip('/')}/static/rich_menu/{menu_name}"
        else:
            return f"https://via.placeholder.com/2500x1686/4CAF50/FFFFFF?text={menu_name}"

    def get_weather_icon_url(self, condition: str) -> str:
        """
        Get weather condition icon URL.

        Args:
            condition: Weather condition (e.g., "sunny", "rainy", "cloudy")

        Returns:
            str: Weather icon URL
        """
        condition_icons = {
            "clear": "weather/sunny.png",
            "sunny": "weather/sunny.png",
            "partly cloudy": "weather/partly_cloudy.png",
            "cloudy": "weather/cloudy.png",
            "overcast": "weather/overcast.png",
            "rainy": "weather/rainy.png",
            "light rain": "weather/light_rain.png",
            "heavy rain": "weather/heavy_rain.png",
            "snow": "weather/snow.png",
            "thunderstorm": "weather/thunderstorm.png",
            "fog": "weather/fog.png",
            "windy": "weather/windy.png"
        }

        icon_path = condition_icons.get(condition.lower(), "weather/default.png")
        return self.get_image_url(icon_path)

    def get_service_icon_url(self, service: str) -> str:
        """
        Get service icon URL.

        Args:
            service: Service name

        Returns:
            str: Service icon URL
        """
        service_icons = {
            "weather": "icons/weather.png",
            "chat": "icons/chat.png",
            "help": "icons/help.png",
            "menu": "icons/menu.png",
            "feedback": "icons/feedback.png",
            "location": "icons/location.png"
        }

        icon_path = service_icons.get(service.lower(), "icons/default.png")
        return self.get_image_url(icon_path)


# Default static URL manager instance
static_url_manager = StaticURLManager()


# Convenience functions
def get_weather_background_url(condition: str = "default") -> str:
    """Get weather background image URL"""
    backgrounds = {
        "clear": "backgrounds/sunny_sky.jpg",
        "sunny": "backgrounds/sunny_sky.jpg",
        "cloudy": "backgrounds/cloudy_sky.jpg",
        "rainy": "backgrounds/rainy_sky.jpg",
        "snow": "backgrounds/snowy_sky.jpg",
        "night": "backgrounds/night_sky.jpg",
        "default": "backgrounds/default_weather.jpg"
    }

    bg_path = backgrounds.get(condition.lower(), backgrounds["default"])
    return static_url_manager.get_image_url(bg_path)


def get_placeholder_image_url(width: int = 1024, height: int = 640, text: str = "Image") -> str:
    """Get placeholder image URL"""
    return f"https://via.placeholder.com/{width}x{height}/E0E0E0/666666?text={text.replace(' ', '+')}"


def get_rich_menu_template_urls() -> dict:
    """Get all Rich Menu template URLs"""
    return {
        "main_menu": static_url_manager.get_rich_menu_url("main_menu.png"),
        "weather_menu": static_url_manager.get_rich_menu_url("weather_menu.png"),
        "simple_menu": static_url_manager.get_rich_menu_url("simple_menu.png")
    }