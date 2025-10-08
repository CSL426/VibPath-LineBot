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
        "content": flex_msg.contents,  # 返回contents而不是整個FlexSendMessage
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
        "content": flex_msg.contents,  # 返回contents而不是整個FlexSendMessage
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
        "content": flex_msg.contents,  # 返回contents而不是整個FlexSendMessage
        "alt_text": "VibPath 服務選單"
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
    "show_product_details": show_product_details
}