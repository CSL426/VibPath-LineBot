"""
Button configuration management for LINE Bot.
Centralized system for managing buttons, links, and postback actions.
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


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
# Platform Configuration
# =============================================================================

PLATFORM_CONFIG = {
    "shopee": {
        "label": "蝦皮購買",
        "store_label": "蝦皮賣場",
        "base_url": "https://shopee.tw/baba1018",
    },
    "familymart": {
        "label": "全家好賣+",
        "base_url": "https://famistore.famiport.com.tw/users/5806400",
    },
    "seven_eleven": {
        "label": "7-11 IOpen Mall",
        "base_url": "https://mall.iopenmall.tw/099753/",
        "product_url_template": "https://mall.iopenmall.tw/099753/index.php?action=product_detail&prod_no={product_id}",
    },
}

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
}


# =============================================================================
# Helper Functions
# =============================================================================

def build_platform_url(platform: str, product_path: str) -> str:
    """Build full URL for a platform and product."""
    if platform not in PLATFORM_CONFIG:
        raise ValueError(f"Unknown platform: {platform}")

    config = PLATFORM_CONFIG[platform]

    if platform == "shopee":
        return product_path
    elif platform == "familymart":
        return f"{config['base_url']}/{product_path}"
    elif platform == "seven_eleven":
        return config["product_url_template"].format(product_id=product_path)

    raise ValueError(f"No URL build rule for platform: {platform}")


def create_platform_buttons(product_urls: Dict[str, str]) -> List[ButtonAction]:
    """Create platform purchase buttons for a product."""
    buttons = []
    for platform in ["shopee", "familymart", "seven_eleven"]:
        if platform in product_urls:
            config = PLATFORM_CONFIG[platform]
            buttons.append(
                ButtonAction(
                    type="uri",
                    label=config["label"],
                    uri=build_platform_url(platform, product_urls[platform])
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
            label=PLATFORM_CONFIG["shopee"]["store_label"],
            uri=PLATFORM_CONFIG["shopee"]["base_url"]
        ),
        ButtonAction(
            type="uri",
            label=PLATFORM_CONFIG["familymart"]["label"],
            uri=PLATFORM_CONFIG["familymart"]["base_url"]
        ),
        ButtonAction(
            type="uri",
            label=PLATFORM_CONFIG["seven_eleven"]["label"],
            uri=PLATFORM_CONFIG["seven_eleven"]["base_url"]
        ),
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
