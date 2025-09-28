"""
Bubble and Carousel templates for LINE Bot.
Advanced Flex Message layouts for rich content display.
"""
from typing import List, Dict, Any, Optional
from linebot.models import (
    FlexSendMessage, BubbleContainer, CarouselContainer,
    BoxComponent, TextComponent, ImageComponent, ButtonComponent,
    SeparatorComponent, SpacerComponent
)


class BubbleTemplates:
    """Advanced Bubble container templates for complex layouts"""

    @staticmethod
    def news_article(article_data: Dict[str, Any]) -> BubbleContainer:
        """
        Create a news article bubble.

        Args:
            article_data: Dictionary containing article information

        Returns:
            BubbleContainer: News article bubble
        """
        return BubbleContainer(
            hero=ImageComponent(
                url=article_data.get("image_url", "https://via.placeholder.com/1024x640/CCCCCC/FFFFFF?text=News"),
                size="full",
                aspect_ratio="20:13",
                aspect_mode="cover"
            ),
            body=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(
                        text=article_data.get("title", "新聞標題"),
                        weight="bold",
                        size="xl",
                        wrap=True
                    ),
                    TextComponent(
                        text=article_data.get("summary", "新聞摘要..."),
                        size="sm",
                        color="#666666",
                        margin="md",
                        wrap=True
                    ),
                    SeparatorComponent(margin="xl"),
                    BoxComponent(
                        layout="horizontal",
                        margin="md",
                        contents=[
                            TextComponent(
                                text=f"📅 {article_data.get('date', '今天')}",
                                size="xs",
                                color="#aaaaaa",
                                flex=1
                            ),
                            TextComponent(
                                text=f"🏷️ {article_data.get('category', '一般')}",
                                size="xs",
                                color="#aaaaaa",
                                flex=1,
                                align="end"
                            )
                        ]
                    )
                ]
            ),
            footer=BoxComponent(
                layout="vertical",
                spacing="sm",
                contents=[
                    ButtonComponent(
                        style="primary",
                        height="sm",
                        action={
                            "type": "uri",
                            "label": "閱讀全文",
                            "uri": article_data.get("url", "https://example.com")
                        }
                    ),
                    ButtonComponent(
                        style="secondary",
                        height="sm",
                        action={
                            "type": "postback",
                            "label": "分享文章",
                            "data": f"action=share&article_id={article_data.get('id', '')}"
                        }
                    )
                ]
            )
        )

    @staticmethod
    def product_card(product_data: Dict[str, Any]) -> BubbleContainer:
        """
        Create a product showcase bubble.

        Args:
            product_data: Dictionary containing product information

        Returns:
            BubbleContainer: Product card bubble
        """
        return BubbleContainer(
            hero=ImageComponent(
                url=product_data.get("image_url", "https://via.placeholder.com/1024x640/E0E0E0/FFFFFF?text=Product"),
                size="full",
                aspect_ratio="20:13",
                aspect_mode="cover"
            ),
            body=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(
                        text=product_data.get("name", "產品名稱"),
                        weight="bold",
                        size="xl",
                        wrap=True
                    ),
                    BoxComponent(
                        layout="horizontal",
                        margin="md",
                        contents=[
                            TextComponent(
                                text=f"💰 ${product_data.get('price', '0')}",
                                size="lg",
                                color="#FF5551",
                                weight="bold",
                                flex=1
                            ),
                            TextComponent(
                                text=f"⭐ {product_data.get('rating', '0')} ({product_data.get('reviews', '0')}評價)",
                                size="sm",
                                color="#666666",
                                flex=2,
                                align="end"
                            )
                        ]
                    ),
                    TextComponent(
                        text=product_data.get("description", "產品描述..."),
                        size="sm",
                        color="#666666",
                        margin="md",
                        wrap=True
                    ),
                    SeparatorComponent(margin="xl"),
                    BoxComponent(
                        layout="vertical",
                        margin="md",
                        spacing="sm",
                        contents=[
                            BoxComponent(
                                layout="horizontal",
                                contents=[
                                    TextComponent(text="📦 庫存", size="sm", color="#666666", flex=1),
                                    TextComponent(
                                        text=product_data.get("stock", "有庫存"),
                                        size="sm",
                                        flex=2,
                                        align="end"
                                    )
                                ]
                            ),
                            BoxComponent(
                                layout="horizontal",
                                contents=[
                                    TextComponent(text="🚚 配送", size="sm", color="#666666", flex=1),
                                    TextComponent(
                                        text=product_data.get("shipping", "免費配送"),
                                        size="sm",
                                        flex=2,
                                        align="end"
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            footer=BoxComponent(
                layout="vertical",
                spacing="sm",
                contents=[
                    ButtonComponent(
                        style="primary",
                        action={
                            "type": "postback",
                            "label": "🛒 加入購物車",
                            "data": f"action=add_cart&product_id={product_data.get('id', '')}"
                        }
                    ),
                    ButtonComponent(
                        style="secondary",
                        action={
                            "type": "uri",
                            "label": "📋 查看詳情",
                            "uri": product_data.get("url", "https://example.com")
                        }
                    )
                ]
            )
        )

    @staticmethod
    def event_card(event_data: Dict[str, Any]) -> BubbleContainer:
        """
        Create an event information bubble.

        Args:
            event_data: Dictionary containing event information

        Returns:
            BubbleContainer: Event card bubble
        """
        return BubbleContainer(
            hero=ImageComponent(
                url=event_data.get("image_url", "https://via.placeholder.com/1024x640/4CAF50/FFFFFF?text=Event"),
                size="full",
                aspect_ratio="20:13",
                aspect_mode="cover"
            ),
            body=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(
                        text=event_data.get("title", "活動標題"),
                        weight="bold",
                        size="xl",
                        wrap=True
                    ),
                    BoxComponent(
                        layout="vertical",
                        margin="lg",
                        spacing="sm",
                        contents=[
                            BoxComponent(
                                layout="horizontal",
                                contents=[
                                    TextComponent(text="📅", size="sm", flex=0),
                                    TextComponent(
                                        text=event_data.get("date", "活動日期"),
                                        size="sm",
                                        color="#666666",
                                        flex=4,
                                        margin="sm"
                                    )
                                ]
                            ),
                            BoxComponent(
                                layout="horizontal",
                                contents=[
                                    TextComponent(text="📍", size="sm", flex=0),
                                    TextComponent(
                                        text=event_data.get("location", "活動地點"),
                                        size="sm",
                                        color="#666666",
                                        flex=4,
                                        margin="sm"
                                    )
                                ]
                            ),
                            BoxComponent(
                                layout="horizontal",
                                contents=[
                                    TextComponent(text="💰", size="sm", flex=0),
                                    TextComponent(
                                        text=event_data.get("price", "免費"),
                                        size="sm",
                                        color="#666666",
                                        flex=4,
                                        margin="sm"
                                    )
                                ]
                            )
                        ]
                    ),
                    SeparatorComponent(margin="xl"),
                    TextComponent(
                        text=event_data.get("description", "活動描述..."),
                        size="sm",
                        color="#666666",
                        margin="md",
                        wrap=True
                    )
                ]
            ),
            footer=BoxComponent(
                layout="vertical",
                spacing="sm",
                contents=[
                    ButtonComponent(
                        style="primary",
                        action={
                            "type": "postback",
                            "label": "🎫 立即報名",
                            "data": f"action=register&event_id={event_data.get('id', '')}"
                        }
                    ),
                    ButtonComponent(
                        style="secondary",
                        action={
                            "type": "uri",
                            "label": "ℹ️ 更多資訊",
                            "uri": event_data.get("url", "https://example.com")
                        }
                    )
                ]
            )
        )


class CarouselTemplates:
    """Carousel container templates for multiple items display"""

    @staticmethod
    def weather_forecast_carousel(forecast_data: List[Dict[str, Any]]) -> FlexSendMessage:
        """
        Create a weather forecast carousel.

        Args:
            forecast_data: List of daily weather data

        Returns:
            FlexSendMessage: Weather forecast carousel
        """
        bubbles = []

        for day_data in forecast_data[:10]:  # Limit to 10 items for carousel
            bubble = BubbleContainer(
                body=BoxComponent(
                    layout="vertical",
                    contents=[
                        TextComponent(
                            text=day_data.get("date", "今天"),
                            weight="bold",
                            size="md",
                            align="center"
                        ),
                        TextComponent(
                            text=f"🌡️ {day_data.get('temp_high', '0')}° / {day_data.get('temp_low', '0')}°",
                            size="sm",
                            align="center",
                            margin="md"
                        ),
                        TextComponent(
                            text=day_data.get("condition", "晴天"),
                            size="xs",
                            color="#666666",
                            align="center",
                            margin="sm"
                        ),
                        TextComponent(
                            text=f"💧 {day_data.get('rain_chance', '0')}%",
                            size="xs",
                            color="#666666",
                            align="center",
                            margin="sm"
                        )
                    ]
                ),
                footer=BoxComponent(
                    layout="vertical",
                    contents=[
                        ButtonComponent(
                            style="secondary",
                            height="sm",
                            action={
                                "type": "postback",
                                "label": "詳細",
                                "data": f"action=weather_detail&date={day_data.get('date', '')}"
                            }
                        )
                    ]
                )
            )
            bubbles.append(bubble)

        carousel = CarouselContainer(contents=bubbles)
        return FlexSendMessage(alt_text="天氣預報", contents=carousel)

    @staticmethod
    def product_showcase_carousel(products: List[Dict[str, Any]]) -> FlexSendMessage:
        """
        Create a product showcase carousel.

        Args:
            products: List of product data

        Returns:
            FlexSendMessage: Product showcase carousel
        """
        bubbles = []

        for product in products[:10]:  # Limit to 10 items
            bubble = BubbleTemplates.product_card(product)
            bubbles.append(bubble)

        carousel = CarouselContainer(contents=bubbles)
        return FlexSendMessage(alt_text="商品展示", contents=carousel)

    @staticmethod
    def news_carousel(articles: List[Dict[str, Any]]) -> FlexSendMessage:
        """
        Create a news articles carousel.

        Args:
            articles: List of news article data

        Returns:
            FlexSendMessage: News carousel
        """
        bubbles = []

        for article in articles[:10]:  # Limit to 10 items
            bubble = BubbleTemplates.news_article(article)
            bubbles.append(bubble)

        carousel = CarouselContainer(contents=bubbles)
        return FlexSendMessage(alt_text="新聞資訊", contents=carousel)