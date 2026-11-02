"""
Pin the exact JSON each message builder sends to LINE.

The golden file was captured from the pre-v3 SDK, so a diff here means customers
would see something different. Regenerate only for an intended content change:
UPDATE_GOLDEN=1 pytest tests/test_message_payloads.py
"""
import json
import os
from pathlib import Path

import pytest

from vibpath_bot.handlers.ai_toggle_handler import ai_toggle_handler
from vibpath_bot.handlers.message_handler import MessageHandler
from vibpath_bot.handlers.postback_handler import postback_handler
from vibpath_bot.handlers.quick_reply import QuickReplyTemplates
from vibpath_bot.services.user_preference_service import user_preference_service
from vibpath_bot.tools import ai_tools

GOLDEN = Path(__file__).parent / "golden" / "line_messages.json"
HOST = "bot.example.test"


def to_payload(message):
    if isinstance(message, (list, tuple)):
        return [to_payload(m) for m in message]
    if isinstance(message, dict):
        return message
    if hasattr(message, "as_json_dict"):
        return message.as_json_dict()
    return message.to_dict()


def build_cases(monkeypatch):
    # AI 開關的訊息內容只看狀態，不需要真的碰資料庫
    monkeypatch.setattr(user_preference_service, "toggle_ai_reply", lambda user_id: user_id == "on")
    monkeypatch.setattr(user_preference_service, "set_ai_reply_status", lambda user_id, enabled: None)
    monkeypatch.setattr(user_preference_service, "is_ai_reply_enabled", lambda user_id: user_id == "on")

    handler = MessageHandler()
    cases = {
        "welcome": handler.create_welcome_message(),
        "service_menu": handler.create_service_menu(),
        "error_flex": handler.create_error_message("測試錯誤"),
        "error_text": handler.create_error_message("測試錯誤", use_flex=False),
        "help": handler.create_help_message(),
        "frequency_carousel": handler.create_frequency_services_carousel(HOST),
        "company_intro": handler.create_company_introduction(HOST),
        "manual_card": handler.create_manual_download_card(HOST),
        "toggle_on": ai_toggle_handler.handle_toggle("on"),
        "toggle_off": ai_toggle_handler.handle_toggle("off"),
        "set_on": ai_toggle_handler.handle_set("x", True),
        "status_on": ai_toggle_handler.get_status("on"),
        "status_off": ai_toggle_handler.get_status("off"),
        "tool_company": ai_tools.show_company_introduction(HOST),
        "tool_catalog": ai_tools.show_product_catalog(HOST),
        "tool_menu": ai_tools.show_service_menu(HOST),
        "tool_manual": ai_tools.show_manual_download(),
        "tool_apps": ai_tools.show_detection_apps(),
        "tool_product": ai_tools.show_product_details("十頻"),
        "qr_basic": handler.create_quick_reply_basic(),
        "qr_products": handler.create_quick_reply_products(),
        "qr_weather_cities": QuickReplyTemplates.weather_cities(),
        "qr_main_menu": QuickReplyTemplates.main_menu(),
        "qr_yes_no": QuickReplyTemplates.yes_no_confirmation(),
        "qr_weather_actions": QuickReplyTemplates.weather_actions("台北"),
        "qr_location": QuickReplyTemplates.location_sharing(),
        "qr_error_recovery": QuickReplyTemplates.error_recovery(),
        "qr_feedback": QuickReplyTemplates.feedback_options(),
        "qr_custom_uri": QuickReplyTemplates.custom_quick_reply(
            [{"label": "網站", "action": "uri", "value": "https://example.test"}]
        ),
    }
    postbacks = postback_handler.list_available_explanations() + [
        "toggle_ai_reply", "check_ai_status", "show_product_details", "show_basic_menu",
        "show_frequency_products", "show_company_intro", "show_manual_download",
        "show_service_menu", "unknown_postback",
    ]
    for data in postbacks:
        cases[f"postback_{data}"] = postback_handler.handle_postback(data, "on", HOST)
    cases["postback_no_quick_reply"] = postback_handler.handle_postback(
        "explain_40hz", "on", HOST, with_quick_reply=False
    )
    return {name: to_payload(message) for name, message in cases.items()}


def test_payloads_match_golden(monkeypatch):
    actual = build_cases(monkeypatch)
    if os.environ.get("UPDATE_GOLDEN"):
        GOLDEN.parent.mkdir(exist_ok=True)
        GOLDEN.write_text(json.dumps(actual, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
        pytest.skip("golden updated")

    expected = json.loads(GOLDEN.read_text(encoding="utf-8"))
    assert sorted(actual) == sorted(expected)
    mismatched = [name for name in expected if actual[name] != expected[name]]
    assert not mismatched, f"payload changed: {mismatched}"
