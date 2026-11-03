"""
Conversation context through the real ADK runner, with only the LLM faked.

Regression: returning as soon as a tool ran left the function call unanswered in the
session, so the model repeated the same tool for every later message.
"""
import asyncio

import pytest
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.genai import types

from vibpath_bot.handlers.message_handler import MessageHandler
from vibpath_bot.services import decision_service as decision_module
from vibpath_bot.services.ai_agent_service import ai_agent_service


class FakeLlm(BaseLlm):
    """Replies with the next scripted part and records every request it saw."""

    script: list = []
    requests: list = []

    async def generate_content_async(self, llm_request, stream=False):
        self.requests.append(llm_request)
        yield LlmResponse(content=types.Content(role="model", parts=[self.script.pop(0)]))


def run(query, user_id):
    return asyncio.run(ai_agent_service.call_agent(query, user_id, "bot.example.test"))


@pytest.fixture()
def fake_llm(monkeypatch):
    llm = FakeLlm(
        model="fake",
        script=[
            types.Part(function_call=types.FunctionCall(name="show_product_catalog", args={})),
            types.Part(text="您剛剛問了產品"),
        ],
        requests=[],
    )
    monkeypatch.setattr(ai_agent_service.root_agent, "model", llm)
    return llm


def parts_in(request):
    return [part for content in request.contents for part in content.parts]


def test_tool_reply_is_returned_without_a_second_llm_call(fake_llm):
    reply = run("你們有哪些產品", "ctx_tool_only")
    assert reply["type"] == "flex_message"
    assert len(fake_llm.requests) == 1


def test_next_message_sees_the_tool_result_and_does_not_repeat(fake_llm):
    assert run("你們有哪些產品", "ctx_followup")["type"] == "flex_message"
    assert "您剛剛問了產品" in run("我剛剛問了什麼？", "ctx_followup")

    history = parts_in(fake_llm.requests[-1])
    assert any(p.function_response and p.function_response.name == "show_product_catalog" for p in history)
    assert any(p.text == "我剛剛問了什麼？" for p in history)


@pytest.mark.parametrize(
    "text, decision, expected",
    [
        ("講人話", ("ai_off", 0.90), "general"),
        ("閉嘴", ("ai_off", 0.95), "general"),
        ("幫我把AI回覆關掉", ("ai_off", 0.90), "ai_off"),
        ("停止回復", ("ai_off", 0.90), "ai_off"),
        ("請開啟自動回覆", ("ai_on", 0.90), "ai_on"),
        ("關掉機器人", ("ai_off", 0.90), "ai_off"),
        ("把AI關掉", ("ai_off", 0.50), "general"),
        ("有哪些產品", ("frequency", 0.90), "frequency"),
    ],
)
def test_toggle_intents_need_the_message_to_mention_it(monkeypatch, text, decision, expected):
    async def fake_classify(message):
        return decision

    monkeypatch.setattr(decision_module.decision_service, "classify_intent", fake_classify)
    assert asyncio.run(MessageHandler().classify_message_type(text)) == expected
