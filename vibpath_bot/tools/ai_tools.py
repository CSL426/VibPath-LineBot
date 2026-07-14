"""
AI Agent tools for LINE Bot interactions.
Provides tools for AI to return Flex Messages and structured responses.
"""
from typing import Dict, Any, Optional
from linebot.models import FlexSendMessage
from ..templates.bubble_templates import BubbleTemplates


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


def show_manual_download(product_type: str = "all") -> Dict[str, Any]:
    """
    Tool for AI to show product manual download cards.
    Use when user asks about manual, documentation, specifications, or user guide.

    Args:
        product_type: Which manual to show. Options:
            - "13freq" or "13頻" or "脈輪": Show only 13頻脈輪機 manual
            - "others" or "舒曼波" or "γ波" or "雙頻": Show only 舒曼波/γ波/雙頻機 manual
            - "guide" or "頻率指南" or "指南": Show only 生命頻率指南
            - "all" (default): Show all manuals

    Returns:
        Dict with flex_message type and manual download card(s)
    """
    from ..config.env_config import settings
    base = (settings.static_base_url or "").rstrip('/')

    product_lower = product_type.lower()
    if product_lower in ["13freq", "13頻", "脈輪"]:
        return {
            "type": "flex_message",
            "content": BubbleTemplates.pdf_download("13頻脈輪機", "下載手冊", f"{base}/images/manual_13feqs.pdf"),
            "alt_text": "13頻脈輪機手冊下載"
        }
    elif product_lower in ["others", "舒曼波", "γ波", "雙頻", "40hz", "7.83hz"]:
        return {
            "type": "flex_message",
            "content": BubbleTemplates.pdf_download("舒曼波/γ波/雙頻機", "下載手冊", f"{base}/images/manual_others.pdf", wrap=True),
            "alt_text": "產品手冊下載"
        }
    elif product_lower in ["guide", "頻率指南", "指南", "生命頻率"]:
        return {
            "type": "flex_message",
            "content": BubbleTemplates.pdf_download("生命頻率指南", "下載指南", f"{base}/images/manual_frequency_guide.pdf"),
            "alt_text": "生命頻率指南下載"
        }
    else:
        return {
            "type": "flex_message",
            "content": BubbleTemplates.build_manual_carousel(),
            "alt_text": "產品手冊下載"
        }


def show_detection_apps() -> Dict[str, Any]:
    """
    Tool for AI to show frequency detection APP card.
    Use when user asks about checking if device is working/running.

    Returns:
        Dict with flex_message type and Android app download card
        (iOS app is currently unavailable)
    """
    from ..config.env_config import settings
    static_base = (settings.static_base_url or "").rstrip('/')

    bubble_android = BubbleTemplates.app_download(
        image_url=f"{static_base}/images/app/android.jpg",
        title="Android 檢測 APP",
        app_name="Ultimate EMF Detector",
        description="可檢測機器發出的電磁場訊號，確認設備是否正常運作",
        button_label="前往 Google Play",
        store_url="https://play.google.com/store/apps/details?id=com.mreprogramming.ultimateemfdetector"
    )

    return {
        "type": "flex_message",
        "content": bubble_android,
        "alt_text": "Android 檢測 APP 下載"
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
        "theta": "explain_double_freq",
        "pulse_gen": "explain_pulse_gen",
        "客製頻率": "explain_pulse_gen",
        "composite_freq": "explain_composite_freq",
        "複合式": "explain_composite_freq",
        "複合式頻率": "explain_composite_freq",
        "0.5hz": "explain_composite_freq",
        "ten_freq": "explain_ten_freq",
        "十頻": "explain_ten_freq",
        "十頻儀": "explain_ten_freq",
        "整合十頻": "explain_ten_freq",
        "整合十頻機": "explain_ten_freq",
        "10頻": "explain_ten_freq",
        "pemf": "explain_ten_freq",
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