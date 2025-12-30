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
                text="👋 您好！歡迎使用 VibPath 智能客服！\n\n我是 AI 客服阿弦，可以為您介紹產品、公司資訊或顯示服務選單。\n\n💡 提醒：若不需要 AI 回覆，可點選下方「🤖 AI開關」或輸入「AI開關」來開啟/關閉。"
                # Removed quick_reply from welcome message
            ),
            self.create_service_menu()
        ]
        return messages


    def create_quick_reply_basic(self) -> QuickReply:
        """
        Create basic quick reply with general options (公司介紹、AI開關等).

        Returns:
            QuickReply: Basic quick reply buttons
        """
        services = [
            {"label": "🏢 公司介紹", "action_type": "postback", "data": "show_company_intro"},
            {"label": "🛒 查看產品", "action_type": "postback", "data": "show_frequency_products"},
            {"label": "📋 選單", "action_type": "postback", "data": "show_service_menu"},
            {"label": "🤖 AI開關", "action_type": "postback", "data": "toggle_ai_reply"},
            {"label": "📖 更多產品", "action_type": "postback", "data": "show_product_details"}
        ]

        quick_reply_buttons = []
        for service in services:
            if service["action_type"] == "postback":
                quick_reply_buttons.append(
                    QuickReplyButton(
                        action=PostbackAction(
                            label=service["label"],
                            data=service["data"]
                        )
                    )
                )
            elif service["action_type"] == "message":
                quick_reply_buttons.append(
                    QuickReplyButton(
                        action=MessageAction(
                            label=service["label"],
                            text=service["text"]
                        )
                    )
                )

        return QuickReply(items=quick_reply_buttons)

    def create_quick_reply_products(self) -> QuickReply:
        """
        Create product-focused quick reply (產品細節).

        Returns:
            QuickReply: Product detail quick reply buttons
        """
        services = [
            {"label": "🎵 商品原理", "action_type": "postback", "data": "explain_frequency"},
            {"label": "🌍 舒曼波", "action_type": "postback", "data": "explain_7_83hz"},
            {"label": "🕉️ 13頻脈輪", "action_type": "postback", "data": "explain_13Freq"},
            {"label": "⚡ γ波40Hz", "action_type": "postback", "data": "explain_40hz"},
            {"label": "🔄 α/θ雙頻", "action_type": "postback", "data": "explain_double_freq"},
            {"label": "🤖 AI開關", "action_type": "postback", "data": "toggle_ai_reply"},
            {"label": "◀️ 返回基本", "action_type": "postback", "data": "show_basic_menu"}
        ]

        quick_reply_buttons = []
        for service in services:
            if service["action_type"] == "postback":
                quick_reply_buttons.append(
                    QuickReplyButton(
                        action=PostbackAction(
                            label=service["label"],
                            data=service["data"]
                        )
                    )
                )

        return QuickReply(items=quick_reply_buttons)

    def create_quick_reply_detailed(self) -> QuickReply:
        """
        Create detailed quick reply with more postback options.
        (保留此方法作為預設，使用基本版)

        Returns:
            QuickReply: Quick reply with detailed service explanations
        """
        return self.create_quick_reply_basic()

    def create_help_message(self) -> TextSendMessage:
        """
        Create help message.

        Returns:
            TextSendMessage: Help message
        """
        help_text = """🤖 VibPath 智能客服使用說明

🎵 商品服務：
• 輸入「商品介紹」或「服務項目」查看產品
• 專業商品技術

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
            quick_reply=self.create_quick_reply_detailed()
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

    def create_manual_download_card(self, request_host: str = None) -> FlexSendMessage:
        """
        Create manual download cards carousel.

        Args:
            request_host: Request host for dynamic URL generation

        Returns:
            FlexSendMessage: Manual download carousel with two cards
        """
        from vibpath_bot.tools.ai_tools import show_manual_download
        result = show_manual_download()
        return FlexSendMessage(alt_text=result["alt_text"], contents=result["content"])


    def detect_message_type(self, text: str) -> str:
        """
        Detect the type of user message.

        Args:
            text: User input text

        Returns:
            str: Message type ('menu', 'help', 'frequency', 'business', 'manual', 'general')
        """
        text_lower = text.lower()

        # Manual/Document keywords - check first for specificity
        manual_keywords = ['手冊', '說明書', '規格', '使用手冊', '產品手冊', '操作手冊', '說明文件']
        if any(keyword in text_lower for keyword in manual_keywords):
            return 'manual'

        # Product introduction keywords - more specific matching
        frequency_keywords = ['商品介紹', '產品介紹', '服務項目']
        if any(keyword in text_lower for keyword in frequency_keywords):
            return 'frequency'

        # Business introduction keywords
        business_keywords = ['公司介紹', '關於我們', '企業簡介', '主業', '業務介紹', '公司']
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
        # Use Flex Message for menu, frequency, business, manual, and error
        flex_types = ['menu', 'error', 'frequency', 'business', 'manual']
        return message_type in flex_types