"""
Bubble templates for LINE Bot.
Flex Message layouts for rich content display (raw dict format).
"""


class BubbleTemplates:
    """Bubble container templates returning raw dicts for Flex Messages"""

    @staticmethod
    def build_manual_carousel() -> dict:
        """Build the all-manuals carousel dict (single source of truth)."""
        from ..config.env_config import settings
        base = (settings.static_base_url or "").rstrip('/')
        return {
            "type": "carousel",
            "contents": [
                BubbleTemplates.pdf_download("13頻脈輪機", "下載手冊", f"{base}/images/manual_13feqs.pdf"),
                BubbleTemplates.pdf_download("舒曼波/γ波/雙頻機", "下載手冊", f"{base}/images/manual_others.pdf", wrap=True),
                BubbleTemplates.pdf_download("生命頻率指南", "下載指南", f"{base}/images/manual_frequency_guide.pdf"),
            ]
        }

    @staticmethod
    def pdf_download(title: str, button_label: str, pdf_url: str, wrap: bool = False) -> dict:
        """Create a micro bubble with a title and PDF download button."""
        text_node = {
            "type": "text", "text": title, "weight": "bold",
            "size": "md", "color": "#1976D2", "align": "center"
        }
        if wrap:
            text_node["wrap"] = True
        return {
            "type": "bubble", "size": "micro",
            "body": {"type": "box", "layout": "vertical", "contents": [text_node]},
            "footer": {"type": "box", "layout": "vertical", "contents": [
                {"type": "button", "style": "primary",
                 "action": {"type": "uri", "label": button_label, "uri": pdf_url}}
            ]}
        }

    @staticmethod
    def app_download(image_url: str, title: str, app_name: str,
                     description: str, button_label: str, store_url: str) -> dict:
        """Create a bubble with hero image, app info, and store download button."""
        return {
            "type": "bubble",
            "hero": {
                "type": "image", "url": image_url, "size": "full",
                "aspectRatio": "20:13", "aspectMode": "cover"
            },
            "body": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "text", "text": title, "weight": "bold", "size": "lg", "color": "#2C3E50"},
                    {"type": "text", "text": app_name, "size": "sm", "color": "#7F8C8D", "margin": "sm"},
                    {"type": "text", "text": description, "size": "xs", "color": "#888888", "margin": "md", "wrap": True}
                ]
            },
            "footer": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "button", "style": "primary",
                     "action": {"type": "uri", "label": button_label, "uri": store_url}}
                ]
            }
        }
