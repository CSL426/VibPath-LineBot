
"""
LINE Bot utility functions including loading animations and messaging helpers.
"""
import logging

from linebot.v3.messaging import AsyncMessagingApi, ShowLoadingAnimationRequest

logger = logging.getLogger(__name__)

# Global variable to store LINE Bot API instance
line_bot_api_instance: AsyncMessagingApi = None


def set_line_bot_api(api_instance):
    """Set LINE Bot API instance for loading animation and other utilities"""
    global line_bot_api_instance
    line_bot_api_instance = api_instance
    logger.info("LINE Bot API instance set successfully")


async def display_loading_animation(user_id: str, loading_seconds: int = 20):
    """
    Displays a loading animation in the chat.
    This feature is only available for one-on-one chats.

    Args:
        user_id (str): The user's ID for the one-on-one chat.
        loading_seconds (int): The duration of the animation in seconds (5-60).
    """
    if line_bot_api_instance is None:
        logger.warning("LINE Bot API not initialized, skipping loading animation.")
        return

    # Ensure loading_seconds is within the allowed range (5-60 seconds)
    validated_seconds = max(5, min(loading_seconds, 60))

    try:
        await line_bot_api_instance.show_loading_animation(
            ShowLoadingAnimationRequest(chat_id=user_id, loading_seconds=validated_seconds)
        )

    except Exception as e:
        logger.error(f"An unexpected error occurred while displaying loading animation: {e}")


def validate_line_api():
    """Check if LINE Bot API instance is properly set"""
    return line_bot_api_instance is not None


async def before_reply_display_loading_animation(user_id: str, loading_seconds: int = 20):
    """
    Alias for display_loading_animation for backward compatibility.
    Displays a loading animation before AI reply.

    Args:
        user_id (str): The user's ID for the one-on-one chat.
        loading_seconds (int): The duration of the animation in seconds (5-60).
    """
    await display_loading_animation(user_id, loading_seconds)
