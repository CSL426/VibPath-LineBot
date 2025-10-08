"""
Custom Flex Message templates for VibPath frequency therapy business.
Includes company introduction and frequency therapy services carousel.
"""
from typing import List, Dict, Any
from linebot.models import FlexSendMessage, BubbleContainer, CarouselContainer
from ..config.static_urls import static_url_manager
from ..config.button_config import button_config_manager


class BusinessTemplates:
    """VibPath frequency therapy business templates"""

    @staticmethod
    def company_introduction_with_homepage(request_host: str = None) -> FlexSendMessage:
        """
        Create company introduction using HomePage.png.

        Returns:
            FlexSendMessage: Company introduction card
        """
        bubble = BubbleContainer(
            hero={
                "type": "image",
                # "url": static_url_manager.get_image_url("business/HomePage.png", request_host),
                "url": "https://csl426.github.io/VibPath-LineBot/images/business/HomePage.png",
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
                        "text": "VibPath 商品介紹",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#2C3E50"
                    },
                    {
                        "type": "text",
                        "text": "專業產品服務 · 身心靈平衡體驗",
                        "size": "sm",
                        "color": "#7F8C8D",
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🎵 專業產品技術",
                                "size": "sm",
                                "color": "#34495E",
                                "margin": "sm"
                            },
                            {
                                "type": "text",
                                "text": "🔬 科學驗證頻率配方",
                                "size": "sm",
                                "color": "#34495E",
                                "margin": "sm"
                            },
                            {
                                "type": "text",
                                "text": "✨ 身心靈全面平衡",
                                "size": "sm",
                                "color": "#34495E",
                                "margin": "sm"
                            }
                        ]
                    }
                ]
            },
            footer=button_config_manager.get_footer_box("company_introduction")
        )

        return FlexSendMessage(alt_text="VibPath 公司介紹", contents=bubble)

    @staticmethod
    def frequency_services_carousel(request_host: str = None) -> FlexSendMessage:
        """
        Create frequency therapy services carousel with 4 services.

        Returns:
            FlexSendMessage: Frequency services carousel
        """
        services = [
            {
                "name": "7.83Hz 舒曼波",
                "description": "地球基礎頻率\n放鬆身心 · 減壓體驗",
                "image": "services/7.83HZ.jpg"
            },
            {
                "name": "13頻 脈輪波",
                "description": "大腦α波共振\n專注提升 · 創意啟發",
                "image": "services/13Freq.jpg"
            },
            {
                "name": "40Hz γ波",
                "description": "高頻能量激活\n意識提升 · 靈性覺醒",
                "image": "services/40HZ.jpg"
            },
            {
                "name": "雙頻 α/θ波",
                "description": "多頻率組合\n全方位體驗",
                "image": "services/DoubleFreq.jpg"
            }
        ]

        bubbles = []
        service_ids = ["service_7_83hz", "service_13Freq", "service_40hz", "service_double_freq"]

        for i, service in enumerate(services):
            bubble = BubbleContainer(
                hero={
                    "type": "image",
                    "url": static_url_manager.get_image_url(service["image"], request_host),
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
                            "text": service["name"],
                            "weight": "bold",
                            "size": "lg",
                            "color": "#2C3E50"
                        },
                        {
                            "type": "text",
                            "text": service["description"],
                            "size": "sm",
                            "color": "#7F8C8D",
                            "margin": "md",
                            "wrap": True
                        }
                    ]
                },
                footer=button_config_manager.get_footer_box(service_ids[i])
            )
            bubbles.append(bubble)

        carousel = CarouselContainer(contents=bubbles)
        return FlexSendMessage(alt_text="VibPath 商品服務", contents=carousel)