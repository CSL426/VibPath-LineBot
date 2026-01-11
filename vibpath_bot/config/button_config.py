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
                        label="蝦皮賣場",
                        uri="https://shopee.tw/baba1018"
                    ),
                    ButtonAction(
                        type="uri",
                        label="全家好賣+",
                        uri="https://famistore.famiport.com.tw/users/5806400"
                    ),
                    ButtonAction(
                        type="uri",
                        label="7-11 IOpen Mall",
                        uri="https://mall.iopenmall.tw/099753/"
                    ),
                    ButtonAction(
                        type="postback",
                        label="🎵 產品介紹",
                        data="show_frequency_products"
                    ),
                    ButtonAction(
                        type="postback",
                        label="📖 詳細介紹",
                        data="explain_company"
                    )
                ]
            ),
            "frequency_services": ButtonGroup(
                template_id="frequency_services",
                buttons=[
                    ButtonAction(
                        type="postback",
                        label="產品介紹",
                        data="explain_frequency"
                    )
                ]
            ),
            "service_7_83hz": ButtonGroup(
                template_id="service_7_83hz",
                buttons=[
                    ButtonAction(
                        type="uri",
                        label="蝦皮購買",
                        uri="https://tw.shp.ee/1d1RBDe"
                    ),
                    ButtonAction(
                        type="uri",
                        label="全家好賣+",
                        uri="https://famistore.famiport.com.tw/users/5806400/merchandise/4060258"
                    ),
                    ButtonAction(
                        type="uri",
                        label="7-11 IOpen Mall",
                        uri="https://mall.iopenmall.tw/099753/index.php?action=product_detail&prod_no=P9975313544882"
                    ),
                    ButtonAction(
                        type="postback",
                        label="產品介紹",
                        data="explain_7_83hz"
                    )
                ]
            ),
            "service_13Freq": ButtonGroup(
                template_id="service_13Freq",
                buttons=[
                    ButtonAction(
                        type="uri",
                        label="蝦皮購買",
                        uri="https://tw.shp.ee/jm7cdmq"
                    ),
                    ButtonAction(
                        type="uri",
                        label="全家好賣+",
                        uri="https://famistore.famiport.com.tw/users/5806400/merchandise/4060309"
                    ),
                    ButtonAction(
                        type="uri",
                        label="7-11 IOpen Mall",
                        uri="https://mall.iopenmall.tw/099753/index.php?action=product_detail&prod_no=P9975313544847"
                    ),
                    ButtonAction(
                        type="postback",
                        label="產品介紹",
                        data="explain_13Freq"
                    )
                ]
            ),
            "service_40hz": ButtonGroup(
                template_id="service_40hz",
                buttons=[
                    ButtonAction(
                        type="uri",
                        label="蝦皮購買",
                        uri="https://tw.shp.ee/GJc8Yru"
                    ),
                    ButtonAction(
                        type="uri",
                        label="全家好賣+",
                        uri="https://famistore.famiport.com.tw/users/5806400/merchandise/4060293"
                    ),
                    ButtonAction(
                        type="uri",
                        label="7-11 IOpen Mall",
                        uri="https://mall.iopenmall.tw/099753/index.php?action=product_detail&prod_no=P9975313544673"
                    ),
                    ButtonAction(
                        type="postback",
                        label="產品介紹",
                        data="explain_40hz"
                    )
                ]
            ),
            "service_double_freq": ButtonGroup(
                template_id="service_double_freq",
                buttons=[
                    ButtonAction(
                        type="uri",
                        label="蝦皮購買",
                        uri="https://tw.shp.ee/ciUiZfy"
                    ),
                    ButtonAction(
                        type="uri",
                        label="全家好賣+",
                        uri="https://famistore.famiport.com.tw/users/5806400/merchandise/4060278"
                    ),
                    ButtonAction(
                        type="uri",
                        label="7-11 IOpen Mall",
                        uri="https://mall.iopenmall.tw/099753/index.php?action=product_detail&prod_no=P9975313544545"
                    ),
                    ButtonAction(
                        type="postback",
                        label="產品介紹",
                        data="explain_double_freq"
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