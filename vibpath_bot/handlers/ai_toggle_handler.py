"""
AI Toggle Handler
Handles AI reply on/off toggle requests from Quick Reply buttons
"""
from linebot.models import TextSendMessage
from vibpath_bot.services.user_preference_service import user_preference_service


class AIToggleHandler:
    """Handler for AI reply toggle functionality"""

    @staticmethod
    def handle_toggle(user_id: str) -> TextSendMessage:
        """
        Handle AI reply toggle request

        Args:
            user_id: LINE user ID

        Returns:
            TextSendMessage: Response message with quick reply
        """
        # Import here to avoid circular import
        from .message_handler import MessageHandler

        # Toggle AI reply status
        new_status = user_preference_service.toggle_ai_reply(user_id)

        if new_status:
            message_text = (
                "✅ AI 自動回覆已開啟\n\n"
                "我會使用 AI 來回答您的問題。\n"
                "如需關閉，請再次點擊此按鈕。"
            )
        else:
            message_text = (
                "⏸️ AI 自動回覆已關閉\n\n"
                "我將不會使用 AI 自動回答問題。\n"
                "您仍然可以使用快速回覆按鈕查看服務資訊。\n"
                "如需開啟，請再次點擊此按鈕。"
            )

        # Add quick reply buttons
        handler = MessageHandler()
        return TextSendMessage(
            text=message_text,
            quick_reply=handler.create_quick_reply_basic()
        )

    @staticmethod
    def get_status(user_id: str) -> TextSendMessage:
        """
        Get current AI reply status

        Args:
            user_id: LINE user ID

        Returns:
            TextSendMessage: Status message with quick reply
        """
        # Import here to avoid circular import
        from .message_handler import MessageHandler

        is_enabled = user_preference_service.is_ai_reply_enabled(user_id)

        if is_enabled:
            message_text = (
                "ℹ️ AI 自動回覆狀態\n\n"
                "目前狀態：✅ 已開啟\n\n"
                "我會使用 AI 來回答您的問題。"
            )
        else:
            message_text = (
                "ℹ️ AI 自動回覆狀態\n\n"
                "目前狀態：⏸️ 已關閉\n\n"
                "我將不會使用 AI 自動回答問題。"
            )

        # Add quick reply buttons
        handler = MessageHandler()
        return TextSendMessage(
            text=message_text,
            quick_reply=handler.create_quick_reply_basic()
        )


# Create handler instance
ai_toggle_handler = AIToggleHandler()
