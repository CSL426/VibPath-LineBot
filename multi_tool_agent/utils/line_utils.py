"""
LINE Bot utility functions including loading animations and messaging helpers.
"""
import logging
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)

# Global variable to store LINE Bot API instance
line_bot_api_instance = None


def set_line_bot_api(api_instance):
    """Set LINE Bot API instance for loading animation and other utilities"""
    global line_bot_api_instance
    line_bot_api_instance = api_instance
    logger.info("LINE Bot API instance set successfully")


async def before_reply_display_loading_animation(user_id: str, loading_seconds: int = 60):
    """
    Display loading animation (typing indicator) before replying to user.

    Args:
        user_id (str): LINE user ID
        loading_seconds (int): Duration to show loading animation (max 60 seconds)
    """
    try:
        if not line_bot_api_instance:
            logger.warning("LINE Bot API instance not set, skipping loading animation")
            return

        from linebot.models import SenderAction

        logger.info(f"Displaying loading animation for user {user_id} for {loading_seconds} seconds")

        # Send initial typing indicator
        await line_bot_api_instance.push_message(
            user_id,
            SenderAction(action="typing")
        )

        # Keep showing typing indicator periodically (every 5 seconds, max 60 seconds)
        animation_duration = min(loading_seconds, 60)
        intervals = animation_duration // 5

        for i in range(intervals):
            await asyncio.sleep(5)
            try:
                await line_bot_api_instance.push_message(
                    user_id,
                    SenderAction(action="typing")
                )
                logger.debug(f"Typing indicator sent {i+1}/{intervals}")
            except Exception as e:
                logger.error(f"Error sending typing indicator: {e}")
                break

    except Exception as e:
        logger.error(f"Loading animation display failed: {e}")


async def send_typing_indicator(user_id: str):
    """
    Send a single typing indicator to user.

    Args:
        user_id (str): LINE user ID
    """
    try:
        if not line_bot_api_instance:
            logger.warning("LINE Bot API instance not set")
            return False

        from linebot.models import SenderAction

        await line_bot_api_instance.push_message(
            user_id,
            SenderAction(action="typing")
        )
        return True

    except Exception as e:
        logger.error(f"Failed to send typing indicator: {e}")
        return False


def validate_line_api():
    """Check if LINE Bot API instance is properly set"""
    return line_bot_api_instance is not None