"""
Button configuration management for LINE Bot.
Centralized system for managing buttons, links, and postback actions.
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class ButtonAction:
    """Button action configuration"""
    type: str  # "uri" or "postback"
    label: str
    uri: Optional[str] = None
    data: Optional[str] = None
    text: Optional[str] = None


@dataclass
class ButtonGroup:
    """Group of buttons for a specific template"""
    template_id: str
    buttons: List[ButtonAction]


class ButtonConfigManager:
    """Manages button configurations for all templates"""

    def __init__(self):
        self.configurations = self._initialize_configurations()

    def _initialize_configurations(self) -> Dict[str, ButtonGroup]:
        """Initialize default button configurations"""
        return {
            "company_introduction": ButtonGroup(
                template_id="company_introduction",
                buttons=[
                    ButtonAction(
                        type="uri",
                        label="蝦皮首頁",
                        uri="https://shopee.tw/baba1018"  # 你可以之後修改
                    ),
                    ButtonAction(
                        type="postback",
                        label="📖 詳細介紹",
                        data="explain_company",
                        text="了解更多公司資訊"
                    )
                ]
            ),
            "frequency_services": ButtonGroup(
                template_id="frequency_services",
                buttons=[
                    ButtonAction(
                        type="postback",
                        label="產品介紹",
                        data="explain_frequency",
                        text="我想了解頻率治療原理"
                    )
                ]
            ),
            "service_7_83hz": ButtonGroup(
                template_id="service_7_83hz",
                buttons=[
                    ButtonAction(
                        type="uri",
                        label="商品蝦皮連結",
                        uri="https://tw.shp.ee/1d1RBDe"
                    ),
                    ButtonAction(
                        type="postback",
                        label="產品介紹",
                        data="explain_7_83hz",
                        text="7.83Hz 舒曼共振原理說明"
                    )
                ]
            ),
            "service_13Freq": ButtonGroup(
                template_id="service_13Freq",
                buttons=[
                    ButtonAction(
                        type="uri",
                        label="商品蝦皮連結",
                        uri="https://tw.shp.ee/jm7cdmq"
                    ),
                    ButtonAction(
                        type="postback",
                        label="產品介紹",
                        data="explain_13Freq",
                        text="13 個頻率效果說明"
                    )
                ]
            ),
            "service_40hz": ButtonGroup(
                template_id="service_40hz",
                buttons=[
                    ButtonAction(
                        type="uri",
                        label="商品蝦皮連結",
                        uri="https://tw.shp.ee/GJc8Yru"
                    ),
                    ButtonAction(
                        type="postback",
                        label="產品介紹",
                        data="explain_40hz",
                        text="40Hz γ波頻率能量說明"
                    )
                ]
            ),
            "service_double_freq": ButtonGroup(
                template_id="service_double_freq",
                buttons=[
                    ButtonAction(
                        type="uri",
                        label="💰 療程價格",
                        uri="https://tw.shp.ee/ciUiZfy"
                    ),
                    ButtonAction(
                        type="postback",
                        label="產品介紹",
                        data="explain_double_freq",
                        text="雙頻複合治療原理說明"
                    )
                ]
            )
        }

    def get_buttons(self, template_id: str) -> List[Dict[str, Any]]:
        """
        Get button configuration for a template.

        Args:
            template_id: Template identifier

        Returns:
            List of button dictionaries for LINE Bot API
        """
        config = self.configurations.get(template_id)
        if not config:
            return []

        buttons = []
        for button in config.buttons:
            if button.type == "uri":
                buttons.append({
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": button.label,
                        "uri": button.uri
                    },
                    "style": "primary" if "預約" in button.label or "官方" in button.label else "secondary",
                    "margin": "sm"
                })
            elif button.type == "postback":
                buttons.append({
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": button.label,
                        "data": button.data,
                        "text": button.text
                    },
                    "style": "secondary",
                    "margin": "sm"
                })

        return buttons

    def get_footer_box(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        Get footer box with buttons for a template.

        Args:
            template_id: Template identifier

        Returns:
            Footer box dictionary or None
        """
        buttons = self.get_buttons(template_id)
        if not buttons:
            return None

        return {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": buttons
        }

    def add_button_group(self, template_id: str, buttons: List[ButtonAction]):
        """Add or update button group for a template"""
        self.configurations[template_id] = ButtonGroup(
            template_id=template_id,
            buttons=buttons
        )

    def update_button_url(self, template_id: str, button_label: str, new_url: str):
        """Update URL for a specific button"""
        config = self.configurations.get(template_id)
        if config:
            for button in config.buttons:
                if button.label == button_label and button.type == "uri":
                    button.uri = new_url
                    break


# Default button configuration manager instance
button_config_manager = ButtonConfigManager()