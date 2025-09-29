"""
Quick Reply utilities for LINE Bot.
Provides various quick reply templates for different scenarios.
"""
from typing import List, Dict, Any, Optional
from linebot.models import (
    QuickReply, QuickReplyButton, MessageAction, PostbackAction,
    URIAction, LocationAction, CameraAction, CameraRollAction
)


class QuickReplyTemplates:
    """Collection of Quick Reply templates for different use cases"""

    @staticmethod
    def weather_cities() -> QuickReply:
        """
        Quick reply for popular weather cities.

        Returns:
            QuickReply: Weather cities quick reply
        """
        cities = [
            {"name": "台北", "emoji": "🏙️"},
            {"name": "高雄", "emoji": "🌃"},
            {"name": "台中", "emoji": "🏢"},
            {"name": "東京", "emoji": "🗼"},
            {"name": "首爾", "emoji": "🏰"},
            {"name": "新加坡", "emoji": "🏖️"},
            {"name": "倫敦", "emoji": "🎡"},
            {"name": "紐約", "emoji": "🗽"},
            {"name": "巴黎", "emoji": "🗼"},
            {"name": "其他城市", "emoji": "🌍"}
        ]

        quick_reply_buttons = []
        for city in cities:
            if city["name"] == "其他城市":
                # Special button for custom city input
                quick_reply_buttons.append(
                    QuickReplyButton(
                        action=MessageAction(
                            label=f"{city['emoji']} {city['name']}",
                            text="請輸入城市名稱"
                        )
                    )
                )
            else:
                quick_reply_buttons.append(
                    QuickReplyButton(
                        action=MessageAction(
                            label=f"{city['emoji']} {city['name']}",
                            text=f"{city['name']}天氣"
                        )
                    )
                )

        return QuickReply(items=quick_reply_buttons)

    @staticmethod
    def main_menu() -> QuickReply:
        """
        Main menu quick reply options.

        Returns:
            QuickReply: Main menu options
        """
        menu_items = [
            {"label": "🌤️ 天氣查詢", "text": "天氣查詢"},
            {"label": "📋 服務選單", "text": "選單"},
            {"label": "❓ 使用說明", "text": "幫助"},
            {"label": "💬 智能對話", "text": "你好"}
        ]

        quick_reply_buttons = []
        for item in menu_items:
            quick_reply_buttons.append(
                QuickReplyButton(
                    action=MessageAction(
                        label=item["label"],
                        text=item["text"]
                    )
                )
            )

        return QuickReply(items=quick_reply_buttons)

    @staticmethod
    def yes_no_confirmation() -> QuickReply:
        """
        Yes/No confirmation quick reply.

        Returns:
            QuickReply: Yes/No options
        """
        quick_reply_buttons = [
            QuickReplyButton(
                action=PostbackAction(
                    label="✅ 是",
                    data="action=confirm&value=yes"
                )
            ),
            QuickReplyButton(
                action=PostbackAction(
                    label="❌ 否",
                    data="action=confirm&value=no"
                )
            )
        ]

        return QuickReply(items=quick_reply_buttons)

    @staticmethod
    def weather_actions(city: str) -> QuickReply:
        """
        Weather-related action buttons for a specific city.

        Args:
            city: City name

        Returns:
            QuickReply: Weather action options
        """
        actions = [
            {"label": "🔄 更新天氣", "text": f"{city}天氣"},
            {"label": "📍 其他城市", "text": "天氣查詢"},
            {"label": "📊 詳細預報", "data": f"action=forecast&city={city}"},
            {"label": "🏠 回主選單", "text": "選單"}
        ]

        quick_reply_buttons = []
        for action in actions:
            if "data" in action:
                # Use postback for actions that need data processing
                quick_reply_buttons.append(
                    QuickReplyButton(
                        action=PostbackAction(
                            label=action["label"],
                            data=action["data"]
                        )
                    )
                )
            else:
                # Use message action for simple text responses
                quick_reply_buttons.append(
                    QuickReplyButton(
                        action=MessageAction(
                            label=action["label"],
                            text=action["text"]
                        )
                    )
                )

        return QuickReply(items=quick_reply_buttons)

    @staticmethod
    def location_sharing() -> QuickReply:
        """
        Location sharing quick reply.

        Returns:
            QuickReply: Location sharing options
        """
        quick_reply_buttons = [
            QuickReplyButton(
                action=LocationAction(label="📍 分享位置")
            ),
            QuickReplyButton(
                action=MessageAction(
                    label="✏️ 手動輸入",
                    text="請輸入城市名稱"
                )
            ),
            QuickReplyButton(
                action=MessageAction(
                    label="🌍 熱門城市",
                    text="熱門城市"
                )
            )
        ]

        return QuickReply(items=quick_reply_buttons)

    @staticmethod
    def error_recovery() -> QuickReply:
        """
        Error recovery options.

        Returns:
            QuickReply: Error recovery options
        """
        quick_reply_buttons = [
            QuickReplyButton(
                action=MessageAction(
                    label="🔄 重試",
                    text="重試"
                )
            ),
            QuickReplyButton(
                action=MessageAction(
                    label="🏠 回主選單",
                    text="選單"
                )
            ),
            QuickReplyButton(
                action=MessageAction(
                    label="❓ 說明",
                    text="幫助"
                )
            )
        ]

        return QuickReply(items=quick_reply_buttons)

    @staticmethod
    def feedback_options() -> QuickReply:
        """
        Feedback and rating options.

        Returns:
            QuickReply: Feedback options
        """
        quick_reply_buttons = [
            QuickReplyButton(
                action=PostbackAction(
                    label="⭐⭐⭐⭐⭐ 很好",
                    data="action=feedback&rating=5"
                )
            ),
            QuickReplyButton(
                action=PostbackAction(
                    label="⭐⭐⭐⭐ 不錯",
                    data="action=feedback&rating=4"
                )
            ),
            QuickReplyButton(
                action=PostbackAction(
                    label="⭐⭐⭐ 普通",
                    data="action=feedback&rating=3"
                )
            ),
            QuickReplyButton(
                action=PostbackAction(
                    label="⭐⭐ 不佳",
                    data="action=feedback&rating=2"
                )
            ),
            QuickReplyButton(
                action=PostbackAction(
                    label="⭐ 很差",
                    data="action=feedback&rating=1"
                )
            )
        ]

        return QuickReply(items=quick_reply_buttons)

    @staticmethod
    def custom_quick_reply(items: List[Dict[str, Any]]) -> QuickReply:
        """
        Create custom quick reply from item list.

        Args:
            items: List of quick reply items
                   Format: [{"label": "text", "action": "message|postback|uri", "value": "..."}]

        Returns:
            QuickReply: Custom quick reply
        """
        quick_reply_buttons = []

        for item in items:
            label = item.get("label", "")
            action_type = item.get("action", "message")
            value = item.get("value", "")

            if action_type == "message":
                action = MessageAction(label=label, text=value)
            elif action_type == "postback":
                action = PostbackAction(label=label, data=value)
            elif action_type == "uri":
                action = URIAction(label=label, uri=value)
            else:
                # Default to message action
                action = MessageAction(label=label, text=value)

            quick_reply_buttons.append(QuickReplyButton(action=action))

        return QuickReply(items=quick_reply_buttons)