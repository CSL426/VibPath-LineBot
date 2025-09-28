"""
LINE Bot message handler for different types of responses.
Handles text, flex messages, quick replies, and other LINE-specific features.
"""
import logging
from typing import Union, List, Optional
from linebot.models import (
    TextSendMessage, FlexSendMessage, QuickReply, QuickReplyButton,
    MessageAction, PostbackAction, URIAction
)
from .flex_templates import FlexMessageTemplates

logger = logging.getLogger(__name__)


class MessageHandler:
    """Handles different types of LINE Bot messages and responses"""

    def __init__(self):
        self.flex_templates = FlexMessageTemplates()

    def create_weather_response(self, weather_data: dict, use_flex: bool = True) -> Union[TextSendMessage, FlexSendMessage]:
        """
        Create weather response message.

        Args:
            weather_data: Weather information dictionary
            use_flex: Whether to use Flex Message or plain text

        Returns:
            LINE message object
        """
        try:
            if use_flex and weather_data.get("status") == "success":
                # Use Flex Message for successful weather data
                return self.flex_templates.weather_card(weather_data)
            else:
                # Fallback to text message
                if weather_data.get("status") == "success":
                    from multi_tool_agent.utils.weather_utils import format_weather_response
                    text = format_weather_response(weather_data)
                else:
                    text = weather_data.get("error_message", "天氣查詢失敗")

                return TextSendMessage(text=text)

        except Exception as e:
            logger.error(f"Error creating weather response: {e}")
            return TextSendMessage(text="抱歉，無法顯示天氣資訊")

    def create_service_menu(self) -> FlexSendMessage:
        """
        Create service menu message.

        Returns:
            FlexSendMessage: Service menu
        """
        return self.flex_templates.service_menu()

    def create_error_message(self, error_text: str, use_flex: bool = True) -> Union[TextSendMessage, FlexSendMessage]:
        """
        Create error message.

        Args:
            error_text: Error message text
            use_flex: Whether to use Flex Message

        Returns:
            LINE message object
        """
        if use_flex:
            return self.flex_templates.error_message(error_text)
        else:
            return TextSendMessage(text=f"❌ {error_text}")

    def create_welcome_message(self) -> List[Union[TextSendMessage, FlexSendMessage]]:
        """
        Create welcome message sequence.

        Returns:
            List of LINE messages
        """
        messages = [
            TextSendMessage(text="🤖 歡迎使用 VibPath 智能客服！"),
            self.create_service_menu()
        ]
        return messages

    def create_quick_reply_cities(self) -> QuickReply:
        """
        Create quick reply for popular cities.

        Returns:
            QuickReply: Quick reply with city options
        """
        cities = ["台北", "高雄", "台中", "東京", "首爾", "新加坡", "倫敦", "紐約"]

        quick_reply_buttons = []
        for city in cities:
            quick_reply_buttons.append(
                QuickReplyButton(
                    action=MessageAction(
                        label=f"🌤️ {city}",
                        text=f"{city}天氣"
                    )
                )
            )

        return QuickReply(items=quick_reply_buttons)

    def create_help_message(self) -> TextSendMessage:
        """
        Create help message.

        Returns:
            TextSendMessage: Help message
        """
        help_text = """🤖 VibPath 智能客服使用說明

🌤️ 天氣查詢：
• 輸入「台北天氣」查詢台北天氣
• 輸入「東京天氣如何」查詢東京天氣
• 支援全球城市查詢

💬 智能對話：
• 直接輸入問題，AI 會為您解答
• 支援繁體中文對話

🔧 其他功能：
• 輸入「選單」顯示服務選單
• 輸入「幫助」顯示此說明

有任何問題都可以直接詢問我！"""

        return TextSendMessage(text=help_text)

    def detect_message_type(self, text: str) -> str:
        """
        Detect the type of user message.

        Args:
            text: User input text

        Returns:
            str: Message type ('weather', 'menu', 'help', 'general')
        """
        text_lower = text.lower()

        # Weather keywords
        weather_keywords = ['天氣', 'weather', '氣溫', '溫度', '下雨', '晴天', '陰天']
        if any(keyword in text_lower for keyword in weather_keywords):
            return 'weather'

        # Menu keywords
        menu_keywords = ['選單', 'menu', '服務', '功能']
        if any(keyword in text_lower for keyword in menu_keywords):
            return 'menu'

        # Help keywords
        help_keywords = ['幫助', 'help', '說明', '使用方法', '怎麼用']
        if any(keyword in text_lower for keyword in help_keywords):
            return 'help'

        # Default to general conversation
        return 'general'

    def should_use_flex_message(self, message_type: str) -> bool:
        """
        Determine whether to use Flex Message for response.

        Args:
            message_type: Type of message

        Returns:
            bool: Whether to use Flex Message
        """
        # Use Flex Message for weather and menu
        flex_types = ['weather', 'menu', 'error']
        return message_type in flex_types