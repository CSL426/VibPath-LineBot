"""
Action handlers for LINE Bot postback and other actions.
Handles user interactions from Flex Messages, Quick Replies, and Rich Menus.
"""
import logging
from typing import Dict, Any, Optional, Callable
from urllib.parse import parse_qs
from linebot.models import PostbackEvent, MessageEvent, FollowEvent, UnfollowEvent

logger = logging.getLogger(__name__)


class ActionRouter:
    """Routes postback actions to appropriate handlers"""

    def __init__(self):
        self.handlers: Dict[str, Callable] = {}
        self.default_handler: Optional[Callable] = None

    def register_handler(self, action: str, handler: Callable):
        """
        Register an action handler.

        Args:
            action: Action identifier
            handler: Handler function
        """
        self.handlers[action] = handler
        logger.info(f"Registered handler for action: {action}")

    def register_default_handler(self, handler: Callable):
        """
        Register default handler for unknown actions.

        Args:
            handler: Default handler function
        """
        self.default_handler = handler
        logger.info("Registered default action handler")

    def handle_postback(self, postback_data: str, user_id: str, event) -> Any:
        """
        Route postback action to appropriate handler.

        Args:
            postback_data: Postback data string
            user_id: LINE user ID
            event: LINE postback event

        Returns:
            Handler result
        """
        try:
            # Parse postback data
            parsed_data = self.parse_postback_data(postback_data)
            action = parsed_data.get("action")

            if not action:
                logger.warning(f"No action found in postback data: {postback_data}")
                return self._handle_unknown_action(postback_data, user_id, event)

            # Route to specific handler
            if action in self.handlers:
                logger.info(f"Handling action: {action} for user: {user_id}")
                return self.handlers[action](parsed_data, user_id, event)
            else:
                logger.warning(f"No handler for action: {action}")
                return self._handle_unknown_action(postback_data, user_id, event)

        except Exception as e:
            logger.error(f"Error handling postback: {e}")
            return self._handle_error(postback_data, user_id, event, e)

    def parse_postback_data(self, postback_data: str) -> Dict[str, Any]:
        """
        Parse postback data string into dictionary.

        Args:
            postback_data: Postback data string (e.g., "action=weather&city=taipei")

        Returns:
            Dict: Parsed data
        """
        try:
            # Parse URL-encoded data
            parsed = parse_qs(postback_data)

            # Convert lists to single values
            result = {}
            for key, values in parsed.items():
                result[key] = values[0] if values else ""

            return result

        except Exception as e:
            logger.error(f"Error parsing postback data: {e}")
            return {"raw_data": postback_data}

    def _handle_unknown_action(self, postback_data: str, user_id: str, event) -> Any:
        """Handle unknown actions"""
        if self.default_handler:
            return self.default_handler(postback_data, user_id, event)
        else:
            logger.warning(f"Unknown action and no default handler: {postback_data}")
            return {"status": "error", "message": "Unknown action"}

    def _handle_error(self, postback_data: str, user_id: str, event, error: Exception) -> Any:
        """Handle errors in action processing"""
        logger.error(f"Action processing error: {error}")
        return {"status": "error", "message": "Action processing failed"}


class DefaultActionHandlers:
    """Default action handlers for common LINE Bot interactions"""

    def __init__(self, message_handler, line_bot_api):
        """
        Initialize default handlers.

        Args:
            message_handler: MessageHandler instance
            line_bot_api: LINE Bot API instance
        """
        self.message_handler = message_handler
        self.line_bot_api = line_bot_api

    async def handle_weather_detail(self, data: Dict[str, Any], user_id: str, event) -> Dict[str, Any]:
        """
        Handle weather detail requests.

        Args:
            data: Parsed postback data
            user_id: LINE user ID
            event: LINE event

        Returns:
            Dict: Response data
        """
        try:
            city = data.get("city", "")
            date = data.get("date", "")

            # TODO: Implement detailed weather logic
            response_text = f"📊 {city} {date} 的詳細天氣資訊\n\n⏰ 這個功能正在開發中..."

            # Reply with text message
            from linebot.models import TextSendMessage
            reply_msg = TextSendMessage(text=response_text)
            await self.line_bot_api.reply_message(event.reply_token, reply_msg)

            return {"status": "success", "action": "weather_detail"}

        except Exception as e:
            logger.error(f"Error in weather detail handler: {e}")
            return {"status": "error", "message": str(e)}

    async def handle_feedback(self, data: Dict[str, Any], user_id: str, event) -> Dict[str, Any]:
        """
        Handle user feedback.

        Args:
            data: Parsed postback data
            user_id: LINE user ID
            event: LINE event

        Returns:
            Dict: Response data
        """
        try:
            rating = data.get("rating", "")

            # TODO: Store feedback in database
            logger.info(f"User {user_id} gave rating: {rating}")

            response_text = f"⭐ 感謝您的評分：{rating} 星！\n您的意見對我們很重要。"

            # Reply with text message
            from linebot.models import TextSendMessage
            reply_msg = TextSendMessage(text=response_text)
            await self.line_bot_api.reply_message(event.reply_token, reply_msg)

            return {"status": "success", "action": "feedback", "rating": rating}

        except Exception as e:
            logger.error(f"Error in feedback handler: {e}")
            return {"status": "error", "message": str(e)}

    async def handle_location_weather(self, data: Dict[str, Any], user_id: str, event) -> Dict[str, Any]:
        """
        Handle location-based weather requests.

        Args:
            data: Parsed postback data
            user_id: LINE user ID
            event: LINE event

        Returns:
            Dict: Response data
        """
        try:
            # Send location sharing request
            from linebot.models import TextSendMessage
            from .quick_reply import QuickReplyTemplates

            reply_msg = TextSendMessage(
                text="📍 請選擇您要查詢天氣的方式：",
                quick_reply=QuickReplyTemplates.location_sharing()
            )
            await self.line_bot_api.reply_message(event.reply_token, reply_msg)

            return {"status": "success", "action": "location_weather"}

        except Exception as e:
            logger.error(f"Error in location weather handler: {e}")
            return {"status": "error", "message": str(e)}

    async def handle_confirm(self, data: Dict[str, Any], user_id: str, event) -> Dict[str, Any]:
        """
        Handle confirmation responses.

        Args:
            data: Parsed postback data
            user_id: LINE user ID
            event: LINE event

        Returns:
            Dict: Response data
        """
        try:
            value = data.get("value", "")

            if value == "yes":
                response_text = "✅ 已確認您的選擇。"
            elif value == "no":
                response_text = "❌ 已取消操作。"
            else:
                response_text = "🤔 未知的確認狀態。"

            # Reply with text message
            from linebot.models import TextSendMessage
            reply_msg = TextSendMessage(text=response_text)
            await self.line_bot_api.reply_message(event.reply_token, reply_msg)

            return {"status": "success", "action": "confirm", "value": value}

        except Exception as e:
            logger.error(f"Error in confirm handler: {e}")
            return {"status": "error", "message": str(e)}

    async def default_postback_handler(self, postback_data: str, user_id: str, event) -> Dict[str, Any]:
        """
        Default handler for unknown postback actions.

        Args:
            postback_data: Raw postback data
            user_id: LINE user ID
            event: LINE event

        Returns:
            Dict: Response data
        """
        try:
            logger.info(f"Unknown postback action: {postback_data}")

            response_text = "🤖 抱歉，我不理解這個操作。\n請使用選單或輸入文字與我對話。"

            # Reply with text message and main menu
            from linebot.models import TextSendMessage
            from .quick_reply import QuickReplyTemplates

            reply_msg = TextSendMessage(
                text=response_text,
                quick_reply=QuickReplyTemplates.main_menu()
            )
            await self.line_bot_api.reply_message(event.reply_token, reply_msg)

            return {"status": "warning", "action": "unknown", "data": postback_data}

        except Exception as e:
            logger.error(f"Error in default postback handler: {e}")
            return {"status": "error", "message": str(e)}


def setup_action_router(message_handler, line_bot_api) -> ActionRouter:
    """
    Setup action router with default handlers.

    Args:
        message_handler: MessageHandler instance
        line_bot_api: LINE Bot API instance

    Returns:
        ActionRouter: Configured router
    """
    router = ActionRouter()
    handlers = DefaultActionHandlers(message_handler, line_bot_api)

    # Register default handlers
    router.register_handler("weather_detail", handlers.handle_weather_detail)
    router.register_handler("feedback", handlers.handle_feedback)
    router.register_handler("location_weather", handlers.handle_location_weather)
    router.register_handler("confirm", handlers.handle_confirm)

    # Register default handler
    router.register_default_handler(handlers.default_postback_handler)

    return router