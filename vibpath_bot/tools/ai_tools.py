"""
AI Agent tools for LINE Bot interactions.
Provides tools for AI to return Flex Messages and structured responses.
"""
from typing import Dict, Any, Optional
from linebot.models import FlexSendMessage


def show_company_introduction(request_host: Optional[str] = None) -> Dict[str, Any]:
    """
    Tool for AI to show company introduction Flex Message.

    Args:
        request_host: Request host for dynamic URL generation

    Returns:
        Dict with flex_message type and content
    """
    from ..templates.custom_templates import BusinessTemplates
    flex_msg = BusinessTemplates.company_introduction_with_homepage(request_host)

    return {
        "type": "flex_message",
        "content": flex_msg.contents.as_json_dict(),  # Convert to dict for serialization
        "alt_text": "VibPath 公司介紹"
    }


def show_product_catalog(request_host: Optional[str] = None) -> Dict[str, Any]:
    """
    Tool for AI to show product catalog carousel.

    Args:
        request_host: Request host for dynamic URL generation

    Returns:
        Dict with flex_message type and content
    """
    from ..templates.custom_templates import BusinessTemplates
    flex_msg = BusinessTemplates.frequency_services_carousel(request_host)

    return {
        "type": "flex_message",
        "content": flex_msg.contents.as_json_dict(),  # Convert to dict for serialization
        "alt_text": "VibPath 商品目錄"
    }


def show_service_menu(request_host: Optional[str] = None) -> Dict[str, Any]:
    """
    Tool for AI to show service menu.

    Args:
        request_host: Request host for dynamic URL generation

    Returns:
        Dict with flex_message type and content
    """
    from ..templates.flex_templates import FlexMessageTemplates
    flex_msg = FlexMessageTemplates.service_menu()

    return {
        "type": "flex_message",
        "content": flex_msg.contents.as_json_dict(),  # Convert to dict for serialization
        "alt_text": "VibPath 服務選單"
    }


def show_manual_download() -> Dict[str, Any]:
    """
    Tool for AI to show product manual download cards.
    Use when user asks about manual, documentation, specifications, or user guide.

    Returns:
        Dict with flex_message type and carousel with two manual download cards
    """
    import os
    static_base = os.getenv("STATIC_BASE_URL", "")
    pdf_url_13feqs = f"{static_base.rstrip('/')}/images/manual_13feqs.pdf"
    pdf_url_others = f"{static_base.rstrip('/')}/images/manual_others.pdf"

    carousel = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📄 13頻脈輪機",
                            "weight": "bold",
                            "size": "xl",
                            "color": "#1976D2"
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "action": {
                                "type": "uri",
                                "label": "⬇️ 下載手冊",
                                "uri": pdf_url_13feqs
                            }
                        }
                    ]
                }
            },
            {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📄 舒曼波/γ波/雙頻機",
                            "weight": "bold",
                            "size": "xl",
                            "color": "#1976D2"
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "action": {
                                "type": "uri",
                                "label": "⬇️ 下載手冊",
                                "uri": pdf_url_others
                            }
                        }
                    ]
                }
            }
        ]
    }

    return {
        "type": "flex_message",
        "content": carousel,
        "alt_text": "產品手冊下載"
    }


def show_detection_apps() -> Dict[str, Any]:
    """
    Tool for AI to show frequency detection APP cards.
    Use when user asks about checking if device is working/running.

    Returns:
        Dict with flex_message type and carousel content for iOS and Android apps
    """
    import os
    static_base = os.getenv("STATIC_BASE_URL", "")

    carousel = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": f"{static_base}/images/app/ios.jpg",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🍎 iOS 檢測 APP",
                            "weight": "bold",
                            "size": "lg",
                            "color": "#2C3E50"
                        },
                        {
                            "type": "text",
                            "text": "Sonic Tools SVM",
                            "size": "sm",
                            "color": "#7F8C8D",
                            "margin": "sm"
                        },
                        {
                            "type": "text",
                            "text": "可檢測機器發出的頻率訊號，確認設備是否正常運作",
                            "size": "xs",
                            "color": "#888888",
                            "margin": "md",
                            "wrap": True
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "action": {
                                "type": "uri",
                                "label": "前往 App Store",
                                "uri": "https://apps.apple.com/tw/app/sonic-tools-svm/id1245046029"
                            }
                        }
                    ]
                }
            },
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": f"{static_base}/images/app/android.jpg",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🤖 Android 檢測 APP",
                            "weight": "bold",
                            "size": "lg",
                            "color": "#2C3E50"
                        },
                        {
                            "type": "text",
                            "text": "Ultimate EMF Detector",
                            "size": "sm",
                            "color": "#7F8C8D",
                            "margin": "sm"
                        },
                        {
                            "type": "text",
                            "text": "可檢測機器發出的電磁場訊號，確認設備是否正常運作",
                            "size": "xs",
                            "color": "#888888",
                            "margin": "md",
                            "wrap": True
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "action": {
                                "type": "uri",
                                "label": "前往 Google Play",
                                "uri": "https://play.google.com/store/apps/details?id=com.mreprogramming.ultimateemfdetector"
                            }
                        }
                    ]
                }
            }
        ]
    }

    return {
        "type": "flex_message",
        "content": carousel,
        "alt_text": "頻率檢測 APP 下載"
    }


def show_product_details(product_type: str) -> Dict[str, Any]:
    """
    Tool for AI to show specific product details.

    Args:
        product_type: Type of product (7_83hz, 13freq, 40hz, double_freq)

    Returns:
        Dict with text response containing product details
    """
    from ..handlers.postback_handler import postback_handler

    product_map = {
        "7_83hz": "explain_7_83hz",
        "7.83hz": "explain_7_83hz",
        "舒曼波": "explain_7_83hz",
        "13freq": "explain_13Freq",
        "13頻": "explain_13Freq",
        "脈輪": "explain_13Freq",
        "40hz": "explain_40hz",
        "gamma": "explain_40hz",
        "γ波": "explain_40hz",
        "double_freq": "explain_double_freq",
        "雙頻": "explain_double_freq",
        "alpha": "explain_double_freq",
        "theta": "explain_double_freq"
    }

    explanation_key = product_map.get(product_type.lower())
    if explanation_key:
        explanation = postback_handler.get_explanation(explanation_key)
        if explanation:
            return {
                "type": "text_with_quick_reply",
                "content": explanation
            }

    return {
        "type": "text",
        "content": "抱歉，找不到該產品的詳細資訊。請使用選單查看我們的產品。"
    }


# Tool registry for Google ADK Agent
AI_TOOLS = {
    "show_company_introduction": show_company_introduction,
    "show_product_catalog": show_product_catalog,
    "show_service_menu": show_service_menu,
    "show_product_details": show_product_details,
    "show_detection_apps": show_detection_apps,
    "show_manual_download": show_manual_download
}