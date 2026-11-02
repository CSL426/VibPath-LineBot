"""
LINE Bot Flex Message templates for VibPath services.
Provides reusable templates for service menus, error messages, etc.
"""
from typing import Dict, Any, List, Optional
from linebot.v3.messaging import FlexContainer, FlexMessage


class FlexMessageTemplates:
    """Collection of Flex Message templates for LINE Bot"""


    @staticmethod
    def service_menu() -> FlexMessage:
        """
        Create a service menu Flex Message.

        Returns:
            FlexMessage: Service menu card
        """
        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "VibPath 智能客服 - 阿弦",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#1976D2"
                    },
                    {
                        "type": "text",
                        "text": "選擇您需要的服務",
                        "size": "md",
                        "color": "#666666",
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "xl",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "🎵",
                                        "size": "xl",
                                        "flex": 1
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "flex": 4,
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "商品介紹",
                                                "weight": "bold",
                                                "size": "md"
                                            },
                                            {
                                                "type": "text",
                                                "text": "專業產品服務介紹",
                                                "size": "sm",
                                                "color": "#666666"
                                            }
                                        ]
                                    }
                                ],
                                "spacing": "md",
                                "paddingAll": "sm"
                            },
                            {
                                "type": "separator"
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "🏢",
                                        "size": "xl",
                                        "flex": 1
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "flex": 4,
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "公司介紹",
                                                "weight": "bold",
                                                "size": "md"
                                            },
                                            {
                                                "type": "text",
                                                "text": "了解 VibPath 企業資訊",
                                                "size": "sm",
                                                "color": "#666666"
                                            }
                                        ]
                                    }
                                ],
                                "spacing": "md",
                                "paddingAll": "sm"
                            },
                            {
                                "type": "separator"
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "💬",
                                        "size": "xl",
                                        "flex": 1
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "flex": 4,
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "智能客服",
                                                "weight": "bold",
                                                "size": "md"
                                            },
                                            {
                                                "type": "text",
                                                "text": "AI 客服為您解答產品問題",
                                                "size": "sm",
                                                "color": "#666666"
                                            }
                                        ]
                                    }
                                ],
                                "spacing": "md",
                                "paddingAll": "sm"
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "action": {
                            "type": "message",
                            "label": "🎵 商品介紹",
                            "text": "商品介紹"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "action": {
                            "type": "message",
                            "label": "🏢 公司介紹",
                            "text": "公司介紹"
                        }
                    }
                ]
            }
        }

        return FlexMessage(alt_text="VibPath 服務選單", contents=FlexContainer.from_dict(bubble))

    @staticmethod
    def error_message(error_text: str) -> FlexMessage:
        """
        Create an error message Flex Message.

        Args:
            error_text: Error message to display

        Returns:
            FlexMessage: Error message card
        """
        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "❌ 發生錯誤",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#E53E3E"
                    },
                    {
                        "type": "text",
                        "text": error_text,
                        "size": "md",
                        "color": "#666666",
                        "margin": "md",
                        "wrap": True
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "secondary",
                        "action": {
                            "type": "message",
                            "label": "🔄 重試",
                            "text": "重試"
                        }
                    }
                ]
            }
        }

        return FlexMessage(alt_text="錯誤訊息", contents=FlexContainer.from_dict(bubble))

    @staticmethod
    def welcome_carousel() -> FlexMessage:
        """
        Create a welcome carousel with VibPath services.

        Returns:
            FlexMessage: Welcome carousel
        """
        # TODO: 可實現歡迎輪播卡片
        # 可以包含：產品介紹、企業簡介、使用指南等
        pass