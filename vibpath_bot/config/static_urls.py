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
        self.base_url = base_url or os.getenv("STATIC_BASE_URL", "https://storage.googleapis.com/vibpath-static") or self._get_service_url()

    def get_image_url(self, image_path: str, request_host: str = None) -> str:
        """
        Get full URL for image asset.

        Args:
            image_path: Relative path to image
            request_host: Host from current request (e.g., 'service-project.region.run.app')

        Returns:
            str: Full image URL
        """
        # Priority 1: Use explicit base_url if set
        if self.base_url:
            # If using GCS, path structure is different
            if "storage.googleapis.com" in self.base_url:
                return f"{self.base_url.rstrip('/')}/images/{image_path}"
            else:
                return f"{self.base_url.rstrip('/')}/static/images/{image_path}"

        # Priority 2: Use request host if provided
        if request_host:
            protocol = "https" if "run.app" in request_host or "localhost" not in request_host else "http"
            return f"{protocol}://{request_host}/static/images/{image_path}"

        # Priority 3: Try to get from environment
        service_url = self._get_service_url()
        if service_url:
            return f"{service_url}/static/images/{image_path}"

        # Fallback: Use placeholder
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

    def _get_service_url(self) -> str:
        """
        Get the service URL from Cloud Run environment or request context.

        Returns:
            str: Service URL or empty string
        """
        # Method 1: Try Cloud Run environment variables
        service_name = os.getenv("K_SERVICE")
        if service_name:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "vibpath")
            region = os.getenv("GOOGLE_CLOUD_REGION", "asia-east1")
            return f"https://{service_name}-{project_id}.{region}.run.app"

        # Method 2: Check for PORT environment (Cloud Run sets PORT=8080)
        port = os.getenv("PORT")
        if port == "8080":
            # We're in Cloud Run, but K_SERVICE might not be set
            # Return empty string to force using placeholder images
            return ""

        # Method 3: Local development
        port = os.getenv("PORT", "8080")
        return f"http://localhost:{port}"


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