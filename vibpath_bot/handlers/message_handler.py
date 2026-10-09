"""
LINE Bot message handler for different types of responses.
Handles text, flex messages, quick replies, and other LINE-specific features.
"""
import logging
from typing import Union, List, Optional
from linebot.models import TextSendMessage, FlexSendMessage
from ..templates.flex_templates import FlexMessageTemplates
from ..templates.custom_templates import BusinessTemplates
from .quick_reply import QuickReplyTemplates
from ..config.keywords_config import keywords_config
from ..config.env_config import settings
from ..services.decision_service import decision_service

logger = logging.getLogger(__name__)

# Intents that change state need DECISION_ACTION_MIN_CONFIDENCE
ACTION_INTENTS = {'ai_on', 'ai_off'}


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
            ),
            self.create_service_menu()
        ]
        return messages


    def create_quick_reply_basic(self):
        """Create basic quick reply with general options."""
        return QuickReplyTemplates.custom_quick_reply([
            {"label": "🏢 公司介紹", "action": "postback", "value": "show_company_intro"},
            {"label": "🛒 查看產品", "action": "postback", "value": "show_frequency_products"},
            {"label": "📋 選單", "action": "postback", "value": "show_service_menu"},
            {"label": "🤖 AI開關", "action": "postback", "value": "toggle_ai_reply"},
            {"label": "📖 更多產品", "action": "postback", "value": "show_product_details"},
        ])

    def create_quick_reply_products(self):
        """Create product-focused quick reply."""
        return QuickReplyTemplates.custom_quick_reply([
            {"label": "🎵 商品原理", "action": "postback", "value": "explain_frequency"},
            {"label": "🌍 舒曼波", "action": "postback", "value": "explain_7_83hz"},
            {"label": "🕉️ 13頻脈輪", "action": "postback", "value": "explain_13Freq"},
            {"label": "⚡ γ波40Hz", "action": "postback", "value": "explain_40hz"},
            {"label": "🔄 α/θ雙頻", "action": "postback", "value": "explain_double_freq"},
            {"label": "🔧 客製頻率", "action": "postback", "value": "explain_pulse_gen"},
            {"label": "🎛️ 複合式頻率", "action": "postback", "value": "explain_composite_freq"},
            {"label": "🎚️ 十頻儀", "action": "postback", "value": "explain_ten_freq"},
            {"label": "🤖 AI開關", "action": "postback", "value": "toggle_ai_reply"},
            {"label": "◀️ 返回基本", "action": "postback", "value": "show_basic_menu"},
        ])

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
            quick_reply=self.create_quick_reply_basic()
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
            FlexSendMessage: Manual download carousel with all manual cards
        """
        from ..templates.bubble_templates import BubbleTemplates
        return FlexSendMessage(
            alt_text="產品手冊下載",
            contents=BubbleTemplates.build_manual_carousel()
        )


    def detect_message_type(self, text: str) -> str:
        """
        Detect the type of user message.

        Args:
            text: User input text

        Returns:
            str: Message type ('menu', 'help', 'frequency', 'business', 'manual', 'general')
        """
        # Check keywords in order of specificity
        if keywords_config.contains_manual_keyword(text):
            return 'manual'
        if keywords_config.contains_product_keyword(text):
            return 'frequency'
        if keywords_config.contains_company_keyword(text):
            return 'business'
        if keywords_config.contains_menu_keyword(text):
            return 'menu'
        if keywords_config.contains_help_keyword(text):
            return 'help'
        return 'general'

    def match_exact_keyword(self, text: str) -> Optional[str]:
        """Return message type when the whole message is a keyword (e.g. 「選單」)."""
        msg = text.strip().lower()
        if msg in ('ai開關', 'ai設定'):
            return 'ai_toggle'
        if msg in ('ai狀態', 'ai status'):
            return 'ai_status'
        for message_type, keywords in (
            ('manual', keywords_config.manual_keywords),
            ('frequency', keywords_config.product_keywords),
            ('business', keywords_config.company_keywords),
            ('menu', keywords_config.menu_keywords),
            ('help', keywords_config.help_keywords),
        ):
            if msg in keywords:
                return message_type
        return None

    async def classify_message_type(self, text: str, keyword_fallback: bool = True) -> str:
        """
        First-layer intent routing: exact keyword first, then the decision model.

        Decision answers below DECISION_MIN_CONFIDENCE are treated as 'general' so that
        uncertain messages go to the AI agent instead of a canned card.
        If the decision API is unavailable, substring keywords are used when keyword_fallback
        is True; otherwise the message is 'general'.
        """
        exact = self.match_exact_keyword(text)
        if exact:
            return exact

        result = await decision_service.classify_intent(text)
        if result is None:
            return self.detect_message_type(text) if keyword_fallback else 'general'

        intent, confidence = result
        logger.info(f"Decision intent: {intent} ({confidence:.2f}) for '{text[:30]}'")
        min_confidence = (
            settings.decision_action_min_confidence if intent in ACTION_INTENTS
            else settings.decision_min_confidence
        )
        if confidence < min_confidence:
            return 'general'
        return intent

    def should_use_flex_message(self, message_type: str) -> bool:
        """Determine whether to use Flex Message for response."""
        return message_type in {'menu', 'error', 'frequency', 'business', 'manual'}
