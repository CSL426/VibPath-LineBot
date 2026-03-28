"""
Button configuration management for LINE Bot.
Centralized system for managing buttons, links, and postback actions.
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from .static_urls import PLATFORM_URLS, build_platform_product_url


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


# =============================================================================
# Product Registry
# =============================================================================

PRODUCT_REGISTRY = {
    "7_83hz": {
        "template_id": "service_7_83hz",
        "explain_data": "explain_7_83hz",
        "urls": {
            "shopee": "https://tw.shp.ee/1d1RBDe",
            "familymart": "merchandise/4060258",
            "seven_eleven": "P9975313544882",
        },
    },
    "13Freq": {
        "template_id": "service_13Freq",
        "explain_data": "explain_13Freq",
        "urls": {
            "shopee": "https://tw.shp.ee/jm7cdmq",
            "familymart": "merchandise/4060309",
            "seven_eleven": "P9975313544847",
        },
    },
    "40hz": {
        "template_id": "service_40hz",
        "explain_data": "explain_40hz",
        "urls": {
            "shopee": "https://tw.shp.ee/GJc8Yru",
            "familymart": "merchandise/4060293",
            "seven_eleven": "P9975313544673",
        },
    },
    "double_freq": {
        "template_id": "service_double_freq",
        "explain_data": "explain_double_freq",
        "urls": {
            "shopee": "https://tw.shp.ee/ciUiZfy",
            "familymart": "merchandise/4060278",
            "seven_eleven": "P9975313544545",
        },
    },
    "pulse_gen": {
        "template_id": "service_pulse_gen",
        "explain_data": "explain_pulse_gen",
        "urls": {
            "shopee": "https://shopee.tw/product/15192070/44379328891/",
            "familymart": "merchandise/4217824",
            "seven_eleven": "P9975314571867",
        },
    },
}


# =============================================================================
# Helper Functions
# =============================================================================

def create_platform_buttons(product_urls: Dict[str, str]) -> List[ButtonAction]:
    """Create platform purchase buttons for a product."""
    buttons = []
    for platform in PLATFORM_URLS:
        if platform in product_urls:
            config = PLATFORM_URLS[platform]
            buttons.append(
                ButtonAction(
                    type="uri",
                    label=config["product_label"],
                    uri=build_platform_product_url(platform, product_urls[platform])
                )
            )
    return buttons


def create_product_button_group(product_key: str) -> ButtonGroup:
    """Create a complete button group for a product."""
    product = PRODUCT_REGISTRY[product_key]
    buttons = create_platform_buttons(product["urls"])
    buttons.append(
        ButtonAction(
            type="postback",
            label="產品介紹",
            data=product["explain_data"]
        )
    )
    return ButtonGroup(template_id=product["template_id"], buttons=buttons)


def create_store_buttons() -> List[ButtonAction]:
    """Create buttons linking to main store pages."""
    return [
        ButtonAction(
            type="uri",
            label=PLATFORM_URLS[platform]["store_label"],
            uri=PLATFORM_URLS[platform]["store_url"]
        )
        for platform in PLATFORM_URLS
    ]


# =============================================================================
# Button Configuration Manager
# =============================================================================

class ButtonConfigManager:
    """Manages button configurations for all templates"""

    def __init__(self):
        self.configurations = self._initialize_configurations()

    def _initialize_configurations(self) -> Dict[str, ButtonGroup]:
        """Initialize default button configurations"""
        configs: Dict[str, ButtonGroup] = {}

        # Company introduction with store links
        configs["company_introduction"] = ButtonGroup(
            template_id="company_introduction",
            buttons=[
                *create_store_buttons(),
                ButtonAction(
                    type="postback",
                    label="產品介紹",
                    data="show_frequency_products"
                ),
                ButtonAction(
                    type="postback",
                    label="詳細介紹",
                    data="explain_company"
                )
            ]
        )

        # Frequency services
        configs["frequency_services"] = ButtonGroup(
            template_id="frequency_services",
            buttons=[
                ButtonAction(
                    type="postback",
                    label="產品介紹",
                    data="explain_frequency"
                )
            ]
        )

        # Generate product button groups from registry
        for product_key in PRODUCT_REGISTRY:
            group = create_product_button_group(product_key)
            configs[group.template_id] = group

        return configs

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

    def add_product(self, product_key: str, template_id: str, explain_data: str,
                    urls: Dict[str, str]):
        """
        Add a new product to the configuration.

        Args:
            product_key: Unique product identifier
            template_id: Template ID for the button group
            explain_data: Postback data for product explanation
            urls: Platform URLs dict, e.g. {"shopee": "...", "familymart": "...", "seven_eleven": "..."}
        """
        product_entry = {
            "template_id": template_id,
            "explain_data": explain_data,
            "urls": urls,
        }
        PRODUCT_REGISTRY[product_key] = product_entry
        group = create_product_button_group(product_key)
        self.configurations[group.template_id] = group


# Default button configuration manager instance
button_config_manager = ButtonConfigManager()
