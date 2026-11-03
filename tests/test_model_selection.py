"""Model selection and the output normalization applied to model text."""
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


def test_valid_traditional_is_never_rewritten():
    # 整句轉換曾把這些改壞
    text = "台灣設計製造，每一台機器不會干擾，了解後再使用 🎚️"
    assert service._to_traditional(text) == text


def test_traditional_product_text_is_left_unchanged():
    for key in postback_handler.list_available_explanations():
        text = postback_handler.get_explanation(key)
        assert service._to_traditional(text) == text, key
