"""
Rich Menu configuration utilities for LINE Bot.
Provides templates and utilities for creating and managing Rich Menus.
"""
from typing import Dict, Any, List, Optional
from linebot.models import RichMenu, RichMenuArea, RichMenuBounds, RichMenuSize
from linebot.models import MessageAction, PostbackAction, URIAction


class RichMenuTemplates:
    """Rich Menu templates for different bot functionalities"""

    @staticmethod
    def create_main_menu() -> Dict[str, Any]:
        """
        Create main service menu Rich Menu configuration.

        Returns:
            Dict: Rich Menu configuration
        """
        return {
            "size": {
                "width": 2500,
                "height": 1686
            },
            "selected": True,
            "name": "VibPath 主選單",
            "chatBarText": "選單",
            "areas": [
                {
                    "bounds": {
                        "x": 0,
                        "y": 0,
                        "width": 1250,
                        "height": 843
                    },
                    "action": {
                        "type": "message",
                        "text": "天氣查詢"
                    }
                },
                {
                    "bounds": {
                        "x": 1250,
                        "y": 0,
                        "width": 1250,
                        "height": 843
                    },
                    "action": {
                        "type": "message",
                        "text": "智能對話"
                    }
                },
                {
                    "bounds": {
                        "x": 0,
                        "y": 843,
                        "width": 833,
                        "height": 843
                    },
                    "action": {
                        "type": "message",
                        "text": "說明"
                    }
                },
                {
                    "bounds": {
                        "x": 833,
                        "y": 843,
                        "width": 834,
                        "height": 843
                    },
                    "action": {
                        "type": "postback",
                        "data": "action=feedback"
                    }
                },
                {
                    "bounds": {
                        "x": 1667,
                        "y": 843,
                        "width": 833,
                        "height": 843
                    },
                    "action": {
                        "type": "uri",
                        "uri": "https://vibpath.com"
                    }
                }
            ]
        }

    @staticmethod
    def create_weather_menu() -> Dict[str, Any]:
        """
        Create weather-focused Rich Menu configuration.

        Returns:
            Dict: Weather Rich Menu configuration
        """
        return {
            "size": {
                "width": 2500,
                "height": 1686
            },
            "selected": False,
            "name": "天氣選單",
            "chatBarText": "天氣",
            "areas": [
                {
                    "bounds": {
                        "x": 0,
                        "y": 0,
                        "width": 625,
                        "height": 843
                    },
                    "action": {
                        "type": "message",
                        "text": "台北天氣"
                    }
                },
                {
                    "bounds": {
                        "x": 625,
                        "y": 0,
                        "width": 625,
                        "height": 843
                    },
                    "action": {
                        "type": "message",
                        "text": "高雄天氣"
                    }
                },
                {
                    "bounds": {
                        "x": 1250,
                        "y": 0,
                        "width": 625,
                        "height": 843
                    },
                    "action": {
                        "type": "message",
                        "text": "台中天氣"
                    }
                },
                {
                    "bounds": {
                        "x": 1875,
                        "y": 0,
                        "width": 625,
                        "height": 843
                    },
                    "action": {
                        "type": "message",
                        "text": "東京天氣"
                    }
                },
                {
                    "bounds": {
                        "x": 0,
                        "y": 843,
                        "width": 625,
                        "height": 843
                    },
                    "action": {
                        "type": "message",
                        "text": "首爾天氣"
                    }
                },
                {
                    "bounds": {
                        "x": 625,
                        "y": 843,
                        "width": 625,
                        "height": 843
                    },
                    "action": {
                        "type": "message",
                        "text": "新加坡天氣"
                    }
                },
                {
                    "bounds": {
                        "x": 1250,
                        "y": 843,
                        "width": 625,
                        "height": 843
                    },
                    "action": {
                        "type": "postback",
                        "data": "action=location_weather"
                    }
                },
                {
                    "bounds": {
                        "x": 1875,
                        "y": 843,
                        "width": 625,
                        "height": 843
                    },
                    "action": {
                        "type": "message",
                        "text": "主選單"
                    }
                }
            ]
        }

    @staticmethod
    def create_simple_menu() -> Dict[str, Any]:
        """
        Create simple 2x2 Rich Menu configuration.

        Returns:
            Dict: Simple Rich Menu configuration
        """
        return {
            "size": {
                "width": 2500,
                "height": 1686
            },
            "selected": False,
            "name": "簡易選單",
            "chatBarText": "選單",
            "areas": [
                {
                    "bounds": {
                        "x": 0,
                        "y": 0,
                        "width": 1250,
                        "height": 843
                    },
                    "action": {
                        "type": "message",
                        "text": "🌤️ 天氣"
                    }
                },
                {
                    "bounds": {
                        "x": 1250,
                        "y": 0,
                        "width": 1250,
                        "height": 843
                    },
                    "action": {
                        "type": "message",
                        "text": "💬 對話"
                    }
                },
                {
                    "bounds": {
                        "x": 0,
                        "y": 843,
                        "width": 1250,
                        "height": 843
                    },
                    "action": {
                        "type": "message",
                        "text": "❓ 說明"
                    }
                },
                {
                    "bounds": {
                        "x": 1250,
                        "y": 843,
                        "width": 1250,
                        "height": 843
                    },
                    "action": {
                        "type": "uri",
                        "uri": "https://vibpath.com"
                    }
                }
            ]
        }


class RichMenuManager:
    """Utilities for managing Rich Menus"""

    def __init__(self, line_bot_api):
        """
        Initialize Rich Menu Manager.

        Args:
            line_bot_api: LINE Bot API instance
        """
        self.line_bot_api = line_bot_api

    async def create_rich_menu_from_template(self, template_config: Dict[str, Any]) -> str:
        """
        Create Rich Menu from template configuration.

        Args:
            template_config: Rich Menu configuration dictionary

        Returns:
            str: Rich Menu ID
        """
        try:
            # Convert dict to RichMenu object
            rich_menu = RichMenu(
                size=RichMenuSize(
                    width=template_config["size"]["width"],
                    height=template_config["size"]["height"]
                ),
                selected=template_config.get("selected", False),
                name=template_config["name"],
                chat_bar_text=template_config["chatBarText"],
                areas=[]
            )

            # Add areas
            for area_config in template_config["areas"]:
                bounds = area_config["bounds"]
                action_config = area_config["action"]

                # Create action based on type
                if action_config["type"] == "message":
                    action = MessageAction(text=action_config["text"])
                elif action_config["type"] == "postback":
                    action = PostbackAction(
                        data=action_config["data"],
                        text=action_config.get("text", "")
                    )
                elif action_config["type"] == "uri":
                    action = URIAction(uri=action_config["uri"])
                else:
                    continue  # Skip unknown action types

                area = RichMenuArea(
                    bounds=RichMenuBounds(
                        x=bounds["x"],
                        y=bounds["y"],
                        width=bounds["width"],
                        height=bounds["height"]
                    ),
                    action=action
                )
                rich_menu.areas.append(area)

            # Create the Rich Menu
            rich_menu_id = await self.line_bot_api.create_rich_menu(rich_menu)
            return rich_menu_id

        except Exception as e:
            print(f"Error creating Rich Menu: {e}")
            return None

    async def set_user_rich_menu(self, user_id: str, rich_menu_id: str) -> bool:
        """
        Set Rich Menu for specific user.

        Args:
            user_id: LINE user ID
            rich_menu_id: Rich Menu ID

        Returns:
            bool: Success status
        """
        try:
            await self.line_bot_api.link_rich_menu_to_user(user_id, rich_menu_id)
            return True
        except Exception as e:
            print(f"Error setting user Rich Menu: {e}")
            return False

    async def set_default_rich_menu(self, rich_menu_id: str) -> bool:
        """
        Set default Rich Menu for all users.

        Args:
            rich_menu_id: Rich Menu ID

        Returns:
            bool: Success status
        """
        try:
            await self.line_bot_api.set_default_rich_menu(rich_menu_id)
            return True
        except Exception as e:
            print(f"Error setting default Rich Menu: {e}")
            return False

    async def upload_rich_menu_image(self, rich_menu_id: str, image_path: str) -> bool:
        """
        Upload Rich Menu image.

        Args:
            rich_menu_id: Rich Menu ID
            image_path: Path to image file

        Returns:
            bool: Success status
        """
        try:
            with open(image_path, 'rb') as image_file:
                await self.line_bot_api.set_rich_menu_image(rich_menu_id, image_file)
            return True
        except Exception as e:
            print(f"Error uploading Rich Menu image: {e}")
            return False

    async def get_user_rich_menu(self, user_id: str) -> Optional[str]:
        """
        Get user's current Rich Menu ID.

        Args:
            user_id: LINE user ID

        Returns:
            Optional[str]: Rich Menu ID or None
        """
        try:
            rich_menu_id = await self.line_bot_api.get_rich_menu_id_of_user(user_id)
            return rich_menu_id
        except Exception as e:
            print(f"Error getting user Rich Menu: {e}")
            return None

    async def delete_rich_menu(self, rich_menu_id: str) -> bool:
        """
        Delete Rich Menu.

        Args:
            rich_menu_id: Rich Menu ID to delete

        Returns:
            bool: Success status
        """
        try:
            await self.line_bot_api.delete_rich_menu(rich_menu_id)
            return True
        except Exception as e:
            print(f"Error deleting Rich Menu: {e}")
            return False