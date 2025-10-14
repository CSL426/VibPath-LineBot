
"""
LINE Bot utility functions including loading animations and messaging helpers.
"""
import logging
import os
import aiohttp
from linebot import AsyncLineBotApi

logger = logging.getLogger(__name__)

# Global variable to store LINE Bot API instance
line_bot_api_instance: AsyncLineBotApi = None


def set_line_bot_api(api_instance):
    """Set LINE Bot API instance for loading animation and other utilities"""
    global line_bot_api_instance
    line_bot_api_instance = api_instance
    logger.info("LINE Bot API instance set successfully")


async def display_loading_animation(user_id: str, loading_seconds: int = 20):
    """
    Displays a loading animation in the chat using direct API call.
    This feature is only available for one-on-one chats.

    Args:
        user_id (str): The user's ID for the one-on-one chat.
        loading_seconds (int): The duration of the animation in seconds (5-60).
    """
    # Get channel access token from environment
    channel_access_token = os.getenv("ChannelAccessToken")
    if not channel_access_token:
        logger.warning("Channel access token not found, skipping loading animation.")
        return

    # Ensure loading_seconds is within the allowed range (5-60 seconds)
    validated_seconds = max(5, min(loading_seconds, 60))

    try:
        logger.info(f"Displaying loading animation for user {user_id} for {validated_seconds} seconds.")

        # Direct API call to LINE Messaging API
        url = "https://api.line.me/v2/bot/chat/loading/start"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {channel_access_token}"
        }
        data = {
            "chatId": user_id,
            "loadingSeconds": validated_seconds
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                if response.status == 200:
                    logger.info(f"Loading animation started successfully for user {user_id}")
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to start loading animation: {response.status} - {error_text}")

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
