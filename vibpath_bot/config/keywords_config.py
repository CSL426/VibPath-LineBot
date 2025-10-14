"""
Keywords configuration for message detection
Centralized management of all keyword patterns
"""
from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class KeywordsConfig:
    """Configuration for message keyword detection"""

    # AI-related keywords (trigger response when AI is disabled)
    ai_keywords: List[str] = field(default_factory=lambda: [
        'ai',
        '阿弦',
        '客服',
        '機器人',
        'bot',
        '你是誰',
        '你好',
        '在嗎',
        '嗨',
        'hi',
        'hello',
        '幫忙',
        '請問'
    ])

    # Menu related keywords
    menu_keywords: List[str] = field(default_factory=lambda: [
        '選單',
        'menu',
        '功能',
        '服務'
    ])

    # Help related keywords
    help_keywords: List[str] = field(default_factory=lambda: [
        '幫助',
        'help',
        '說明',
        '使用方法'
    ])

    # Product related keywords
    product_keywords: List[str] = field(default_factory=lambda: [
        '商品',
        '產品',
        '商品介紹',
        '產品介紹',
        '購買',
        '價格'
    ])

    # Company related keywords
    company_keywords: List[str] = field(default_factory=lambda: [
        '公司',
        '關於我們',
        '公司介紹',
        '企業'
    ])

    def contains_ai_keyword(self, message: str) -> bool:
        """
        Check if message contains any AI-related keyword

        Args:
            message: User message text

        Returns:
            bool: True if contains AI keyword
        """
        msg_lower = message.lower()
        return any(keyword.lower() in msg_lower for keyword in self.ai_keywords)

    def contains_menu_keyword(self, message: str) -> bool:
        """Check if message contains menu keyword"""
        msg_lower = message.lower()
        return any(keyword.lower() in msg_lower for keyword in self.menu_keywords)

    def contains_help_keyword(self, message: str) -> bool:
        """Check if message contains help keyword"""
        msg_lower = message.lower()
        return any(keyword.lower() in msg_lower for keyword in self.help_keywords)

    def contains_product_keyword(self, message: str) -> bool:
        """Check if message contains product keyword"""
        msg_lower = message.lower()
        return any(keyword.lower() in msg_lower for keyword in self.product_keywords)

    def contains_company_keyword(self, message: str) -> bool:
        """Check if message contains company keyword"""
        msg_lower = message.lower()
        return any(keyword.lower() in msg_lower for keyword in self.company_keywords)


# Global instance (frozen dataclass ensures immutability)
keywords_config = KeywordsConfig()
