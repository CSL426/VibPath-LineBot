"""
End-to-end webhook tests: signed LINE payload in, real HTTP request to a stub LINE API out.
Exercises the SDK's serialization and response parsing, which payload tests can't reach.
"""
import base64
import hashlib
import hmac
import json
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest
from fastapi.testclient import TestClient
from linebot.v3.messaging import Configuration

import main
from vibpath_bot.config.env_config import settings
from vibpath_bot.services.ai_agent_service import ai_agent_service
from vibpath_bot.services.user_preference_service import user_preference_service
from vibpath_bot.tools import ai_tools

USER_ID = "U" + "0" * 32


@pytest.fixture()
def line_api():
    """Stub LINE API. Answers the way LINE does, including 202 for the loading animation."""
    calls = []

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            calls.append((self.path, self.headers.get("Authorization"), json.loads(self.rfile.read(length))))
            is_loading = self.path == "/v2/bot/chat/loading/start"
            # v3 SDK 會驗證回應，sentMessages 至少要一筆，空陣列會丟例外
            body = b"{}" if is_loading else b'{"sentMessages": [{"id": "1", "quoteToken": "q"}]}'
            self.send_response(202 if is_loading else 200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    server.calls = calls
    server.url = f"http://127.0.0.1:{server.server_port}"
    yield server
    server.shutdown()


@pytest.fixture()
def client(line_api, monkeypatch):
    monkeypatch.setattr(user_preference_service, "is_ai_reply_enabled", lambda user_id: True)
    monkeypatch.setattr(
        main,
        "Configuration",
        lambda access_token: Configuration(host=line_api.url, access_token=access_token),
    )
    with TestClient(main.app) as test_client:
        yield test_client


def post_events(client, events, secret=None):
    body = json.dumps({"destination": "Uxxx", "events": events})
    digest = hmac.new((secret or settings.channel_secret).encode(), body.encode(), hashlib.sha256).digest()
    return client.post(
        "/webhook",
        content=body,
        headers={"X-Line-Signature": base64.b64encode(digest).decode(), "Content-Type": "application/json"},
    )


def base_event(event_type, **extra):
    return {
        "type": event_type,
        "mode": "active",
        "timestamp": 1700000000000,
        "webhookEventId": "01H00000000000000000000000",
        "deliveryContext": {"isRedelivery": False},
        "source": {"type": "user", "userId": USER_ID},
        "replyToken": "reply-token",
        **extra,
    }


def text_event(text):
    return base_event(
        "message",
        message={"id": "1", "type": "text", "text": text, "quoteToken": "q"},
    )


def replies(line_api):
    return [body for path, _, body in line_api.calls if path == "/v2/bot/message/reply"]


def assert_contains(actual, expected):
    """Every expected field survives. The SDK may add defaults, e.g. image `animated: false`."""
    if isinstance(expected, dict):
        for key, value in expected.items():
            assert_contains(actual[key], value)
    elif isinstance(expected, list):
        assert len(actual) == len(expected)
        for actual_item, expected_item in zip(actual, expected):
            assert_contains(actual_item, expected_item)
    else:
        assert actual == expected


def test_bad_signature_is_rejected(client):
    assert post_events(client, [text_event("選單")], secret="wrong").status_code == 400


def test_keyword_replies_with_flex_and_quick_reply(client, line_api):
    assert post_events(client, [text_event("選單")]).status_code == 200
    path, auth, body = line_api.calls[0]
    assert path == "/v2/bot/message/reply"
    assert auth == f"Bearer {settings.channel_access_token}"
    assert body["replyToken"] == "reply-token"
    message = body["messages"][0]
    assert message["type"] == "flex"
    assert message["altText"] == "VibPath 服務選單"
    assert message["contents"]["type"] == "bubble"
    assert message["quickReply"]["items"][0]["action"]["type"] == "postback"


def test_postback_replies(client, line_api):
    event = base_event("postback", postback={"data": "show_company_intro"})
    assert post_events(client, [event]).status_code == 200
    message = replies(line_api)[0]["messages"][0]
    assert message["altText"] == "VibPath 公司介紹"
    assert message["contents"]["hero"]["url"].endswith("/images/business/HomePage.png")


def test_follow_sends_both_welcome_messages(client, line_api):
    event = base_event("follow", follow={"isUnblocked": False})
    assert post_events(client, [event]).status_code == 200
    assert [m["type"] for m in replies(line_api)[0]["messages"]] == ["text", "flex"]


def test_ai_text_reply_shows_loading_without_error_log(client, line_api, monkeypatch, caplog):
    async def fake_agent(msg, user_id, request_host):
        return "AI客服阿弦:\n您好"

    monkeypatch.setattr(ai_agent_service, "call_agent", fake_agent)
    with caplog.at_level(logging.INFO):
        assert post_events(client, [text_event("你好")]).status_code == 200

    # LINE 回 202 才是成功，舊版只認 200，每次都記一筆假的 ERROR
    loading = [body for path, _, body in line_api.calls if path == "/v2/bot/chat/loading/start"]
    assert loading == [{"chatId": USER_ID, "loadingSeconds": 60}]
    assert line_api.calls[0][0] == "/v2/bot/chat/loading/start"
    assert not [r for r in caplog.records if r.levelno >= logging.ERROR]

    message = replies(line_api)[0]["messages"][0]
    assert message["text"] == "AI客服阿弦:\n您好"
    assert message["quickReply"]["items"]


@pytest.mark.parametrize(
    "tool_result",
    [
        ai_tools.show_product_catalog("bot.example.test"),
        ai_tools.show_detection_apps(),
        ai_tools.show_manual_download(),
    ],
    ids=["catalog", "apps", "manual"],
)
def test_ai_tool_flex_reply_keeps_content(client, line_api, monkeypatch, tool_result):
    async def fake_agent(msg, user_id, request_host):
        return tool_result

    monkeypatch.setattr(ai_agent_service, "call_agent", fake_agent)
    assert post_events(client, [text_event("給我看")]).status_code == 200
    message = replies(line_api)[0]["messages"][0]
    assert message["type"] == "flex"
    assert message["altText"] == tool_result["alt_text"]
    assert_contains(message["contents"], tool_result["content"])


def test_other_events_are_ignored(client, line_api):
    events = [
        base_event("unfollow"),
        base_event(
            "message",
            message={"id": "2", "type": "image", "quoteToken": "q", "contentProvider": {"type": "line"}},
        ),
        base_event("somethingLineAddsLater", somethingNew={"x": 1}),
    ]
    assert post_events(client, events).status_code == 200
    assert line_api.calls == []
