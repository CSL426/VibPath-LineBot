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
from ..templates.flex_templates import FlexMessageTemplates
from ..templates.custom_templates import BusinessTemplates
from ..utils.image_manager import default_flex_builder

logger = logging.getLogger(__name__)


class MessageHandler:
    """Handles different types of LINE Bot messages and responses"""

    def __init__(self):
        self.flex_templates = FlexMessageTemplates()
        self.business_templates = BusinessTemplates()


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
            TextSendMessage(
                text="🤖 歡迎使用 VibPath 智能客服！\n\n🎵 專業頻率治療服務\n🏢 企業諮詢服務\n💬 智能對話助手",
                quick_reply=self.create_quick_reply_services()
            ),
            self.create_service_menu()
        ]
        return messages

    def create_quick_reply_services(self) -> QuickReply:
        """
        Create quick reply for VibPath services with mixed actions.

        Returns:
            QuickReply: Quick reply with service options (message + postback actions)
        """
        services = [
            {"label": "🏢 公司介紹", "action_type": "message", "text": "公司介紹"},
            {"label": "🎵 頻率治療", "action_type": "message", "text": "頻率治療"},
            {"label": "📋 選單", "action_type": "message", "text": "選單"},
            {"label": "💡 快速解說", "action_type": "postback", "data": "explain_frequency", "text": "頻率治療原理說明"}
        ]

        quick_reply_buttons = []
        for service in services:
            if service["action_type"] == "message":
                quick_reply_buttons.append(
                    QuickReplyButton(
                        action=MessageAction(
                            label=service["label"],
                            text=service["text"]
                        )
                    )
                )
            elif service["action_type"] == "postback":
                quick_reply_buttons.append(
                    QuickReplyButton(
                        action=PostbackAction(
                            label=service["label"],
                            data=service["data"],
                            text=service["text"]
                        )
                    )
                )

        return QuickReply(items=quick_reply_buttons)

    def create_quick_reply_detailed(self) -> QuickReply:
        """
        Create detailed quick reply with more postback options.

        Returns:
            QuickReply: Quick reply with detailed service explanations
        """
        services = [
            {"label": "🌍 7.83Hz", "action_type": "postback", "data": "explain_7_83hz", "text": "7.83Hz 舒曼共振說明"},
            {"label": "🧠 13Hz", "action_type": "postback", "data": "explain_13Freq", "text": "13Hz α波頻率說明"},
            {"label": "⚡ 40Hz", "action_type": "postback", "data": "explain_40hz", "text": "40Hz γ波頻率說明"},
            {"label": "🔄 雙頻", "action_type": "postback", "data": "explain_double_freq", "text": "雙頻複合治療說明"},
            {"label": "🏢 公司", "action_type": "postback", "data": "explain_company", "text": "VibPath 公司介紹"},
            {"label": "🛒 購買", "action_type": "message", "text": "頻率治療"}
        ]

        quick_reply_buttons = []
        for service in services:
            if service["action_type"] == "message":
                quick_reply_buttons.append(
                    QuickReplyButton(
                        action=MessageAction(
                            label=service["label"],
                            text=service["text"]
                        )
                    )
                )
            elif service["action_type"] == "postback":
                quick_reply_buttons.append(
                    QuickReplyButton(
                        action=PostbackAction(
                            label=service["label"],
                            data=service["data"],
                            text=service["text"]
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

🎵 頻率治療服務：
• 輸入「頻率治療」或「服務項目」查看療程
• 輸入「四夜」查看四種頻率服務
• 專業頻率治療技術

🏢 企業服務：
• 輸入「公司介紹」了解我們的服務
• 輸入「關於我們」查看企業資訊

💬 智能對話：
• 直接輸入問題，AI 會為您解答
• 支援繁體中文對話

🔧 其他功能：
• 輸入「選單」顯示服務選單
• 輸入「幫助」顯示此說明

有任何問題都可以直接詢問我！"""

        return TextSendMessage(
            text=help_text,
            quick_reply=self.create_quick_reply_services()
        )

    def create_frequency_services_carousel(self, request_host: str = None) -> FlexSendMessage:
        """
        Create frequency therapy services carousel.

        Args:
            request_host: Request host for dynamic URL generation

        Returns:
            FlexSendMessage: Frequency services carousel
        """
        return self.business_templates.frequency_services_carousel(request_host)

    def create_company_introduction(self, request_host: str = None) -> FlexSendMessage:
        """
        Create company introduction message.

        Args:
            request_host: Request host for dynamic URL generation

        Returns:
            FlexSendMessage: Company introduction
        """
        return self.business_templates.company_introduction_with_homepage(request_host)


    def detect_message_type(self, text: str) -> str:
        """
        Detect the type of user message.

        Args:
            text: User input text

        Returns:
            str: Message type ('menu', 'help', 'frequency', 'business', 'general')
        """
        text_lower = text.lower()

        # Frequency therapy keywords
        frequency_keywords = ['頻率', '赫茲', 'hz', '療程', '四夜', '服務項目', '頻率治療']
        if any(keyword in text_lower for keyword in frequency_keywords):
            return 'frequency'

        # Business introduction keywords
        business_keywords = ['公司介紹', '關於我們', '企業簡介', '主業', '業務介紹']
        if any(keyword in text_lower for keyword in business_keywords):
            return 'business'

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
        # Use Flex Message for menu, frequency, business, and error
        flex_types = ['menu', 'error', 'frequency', 'business']
        return message_type in flex_types