"""
LINE Bot Flex Message templates for various content types.
Provides reusable templates for weather, general info, menus, etc.
"""
from typing import Dict, Any, List, Optional
from linebot.models import FlexSendMessage, BubbleContainer, CarouselContainer


class FlexMessageTemplates:
    """Collection of Flex Message templates for LINE Bot"""

    @staticmethod
    def weather_card(weather_data: Dict[str, Any]) -> FlexSendMessage:
        """
        Create a weather information Flex Message card.

        Args:
            weather_data: Dictionary containing weather information

        Returns:
            FlexSendMessage: Formatted weather card
        """
        data = weather_data.get('data', {})
        city = data.get('city', 'Unknown')
        country = data.get('country', '')
        location = f"{city}, {country}" if country else city

        bubble = BubbleContainer(
            direction='ltr',
            hero={
                "type": "image",
                "url": "https://via.placeholder.com/1024x640/87CEEB/FFFFFF?text=Weather",  # TODO: 替換為實際天氣圖片
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            body={
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"🌤️ {location}",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#1976D2"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "🌡️ 溫度",
                                        "color": "#666666",
                                        "size": "sm",
                                        "flex": 2
                                    },
                                    {
                                        "type": "text",
                                        "text": f"{data.get('temperature', 'N/A')} ({data.get('temperature_f', 'N/A')})",
                                        "wrap": True,
                                        "color": "#333333",
                                        "size": "sm",
                                        "flex": 3
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "☁️ 天氣",
                                        "color": "#666666",
                                        "size": "sm",
                                        "flex": 2
                                    },
                                    {
                                        "type": "text",
                                        "text": data.get('condition', 'N/A'),
                                        "wrap": True,
                                        "color": "#333333",
                                        "size": "sm",
                                        "flex": 3
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "💧 濕度",
                                        "color": "#666666",
                                        "size": "sm",
                                        "flex": 2
                                    },
                                    {
                                        "type": "text",
                                        "text": data.get('humidity', 'N/A'),
                                        "wrap": True,
                                        "color": "#333333",
                                        "size": "sm",
                                        "flex": 3
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "🌬️ 風速",
                                        "color": "#666666",
                                        "size": "sm",
                                        "flex": 2
                                    },
                                    {
                                        "type": "text",
                                        "text": f"{data.get('wind_speed', 'N/A')} ({data.get('wind_direction', 'N/A')})",
                                        "wrap": True,
                                        "color": "#333333",
                                        "size": "sm",
                                        "flex": 3
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            footer={
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "🔄 更新天氣",
                            "text": f"{city}天氣"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "action": {
                            "type": "uri",
                            "label": "📊 詳細資訊",
                            "uri": f"https://wttr.in/{city}"
                        }
                    }
                ]
            }
        )

        return FlexSendMessage(alt_text=f"{location} 天氣資訊", contents=bubble)

    @staticmethod
    def service_menu() -> FlexSendMessage:
        """
        Create a service menu Flex Message.

        Returns:
            FlexSendMessage: Service menu card
        """
        bubble = BubbleContainer(
            hero={
                "type": "image",
                "url": "https://via.placeholder.com/1024x640/4CAF50/FFFFFF?text=VibPath+Services",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            body={
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🤖 VibPath 智能客服",
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
                                        "text": "🌤️",
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
                                                "text": "天氣查詢",
                                                "weight": "bold",
                                                "size": "md"
                                            },
                                            {
                                                "type": "text",
                                                "text": "查詢全球城市即時天氣",
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
                                                "text": "智能對話",
                                                "weight": "bold",
                                                "size": "md"
                                            },
                                            {
                                                "type": "text",
                                                "text": "AI 助手為您解答問題",
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
            footer={
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "action": {
                            "type": "message",
                            "label": "🌤️ 查詢天氣",
                            "text": "台北天氣"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "action": {
                            "type": "message",
                            "label": "💬 開始對話",
                            "text": "你好"
                        }
                    }
                ]
            }
        )

        return FlexSendMessage(alt_text="VibPath 服務選單", contents=bubble)

    @staticmethod
    def error_message(error_text: str) -> FlexSendMessage:
        """
        Create an error message Flex Message.

        Args:
            error_text: Error message to display

        Returns:
            FlexSendMessage: Error message card
        """
        bubble = BubbleContainer(
            body={
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
            footer={
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
        )

        return FlexSendMessage(alt_text="錯誤訊息", contents=bubble)

    @staticmethod
    def welcome_carousel() -> FlexSendMessage:
        """
        Create a welcome carousel with multiple service cards.

        Returns:
            FlexSendMessage: Welcome carousel
        """
        # TODO: 實現歡迎輪播卡片
        # 可以包含：服務介紹、功能展示、使用指南等
        pass

    @staticmethod
    def quick_reply_weather_cities() -> Dict[str, Any]:
        """
        Create quick reply options for popular cities.

        Returns:
            Dict: Quick reply items for weather queries
        """
        # TODO: 實現快速回覆選項
        # 可以包含：熱門城市、最近查詢、自定義城市等
        pass