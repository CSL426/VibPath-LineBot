"""Model selection and the output normalization applied to model text."""
import pytest
from google.adk.models.anthropic_llm import AnthropicLlm

from vibpath_bot.handlers.postback_handler import postback_handler
from vibpath_bot.services import ai_agent_service as service


def test_claude_model_uses_anthropic_client_with_workspace_header(monkeypatch):
    monkeypatch.setenv("AI_MODEL", "claude-haiku-5-5")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("ANTHROPIC_WORKSPACE_ID", "wrkspc_test")

    model, config = service._build_model()

    assert isinstance(model, AnthropicLlm)
    assert model.model == "claude-haiku-5-5"
    assert model.client.default_headers["anthropic-workspace-id"] == "wrkspc_test"
    assert model.client.max_retries == 1
    assert config.effort == "low"


def test_other_models_pass_through_to_gemini(monkeypatch):
    monkeypatch.setenv("AI_MODEL", "gemini-3.5-flash-lite")
    assert service._build_model() == ("gemini-3.5-flash-lite", None)


def test_default_is_haiku(monkeypatch):
    monkeypatch.delenv("AI_MODEL")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    model, _ = service._build_model()
    assert model.model == "claude-haiku-5-5"


def test_simplified_characters_become_traditional():
    assert service._to_traditional("这是关于磁场的问题") == "這是關於磁場的問題"


def test_mainland_terms_become_taiwan_terms():
    assert service._to_traditional("视频和软件的信息，默认质量") == "影片和軟體的資訊，預設品質"
    assert service._to_traditional("視頻的屏幕") == "影片的螢幕"


@pytest.mark.parametrize(
    "text, expected",
    [
        ("這個問題是安全問題，我直接用文字回答。\n\n產品符合規範。", "產品符合規範。"),
        ("這是安全相關問題，我直接用文字說明：產品符合規範。", "產品符合規範。"),
        ("有輻射嗎這類安全相關問題，我直接回答：產品符合規範。", "產品符合規範。"),
        ("依規定直接以文字回答，不呼叫工具。\n抱歉，無法治療。", "抱歉，無法治療。"),
    ],
)
def test_meta_opening_is_removed(text, expected):
    assert service._strip_meta_opening(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "產品符合規範。\n我們也提供文字回答以外的服務。",
        "十頻儀採用 Type-C 供電。",
        "請問您用的工具是哪一款？",
        "我直接用文字回答。",
    ],
    ids=["later-sentence", "plain", "customer-word", "only-sentence"],
)
def test_normal_replies_are_kept(text):
    expected = text
    assert service._strip_meta_opening(text) == expected


def test_valid_traditional_is_never_rewritten():
    # 整句轉換曾把這些改壞
    text = "台灣設計製造，每一台設備不會干擾，了解後查看訊息再使用 🎚️"
    assert service._to_traditional(text) == text


def test_traditional_product_text_is_left_unchanged():
    for key in postback_handler.list_available_explanations():
        text = postback_handler.get_explanation(key)
        assert service._to_traditional(text) == text, key
