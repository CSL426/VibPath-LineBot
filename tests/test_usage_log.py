"""Each model call logs its token usage so prompt cache hits can be checked in production."""
import asyncio
import logging

from google.adk.events import Event
from google.genai import types

from vibpath_bot.services import ai_agent_service as service


async def _events(*events):
    for event in events:
        yield event


def test_model_usage_is_logged_with_cache_tokens(caplog):
    usage = types.GenerateContentResponseUsageMetadata(
        prompt_token_count=5274, cached_content_token_count=5185, candidates_token_count=56
    )
    event = Event(
        author="vibpath_agent",
        content=types.Content(role="model", parts=[types.Part(text="您好")]),
        usage_metadata=usage,
    )

    with caplog.at_level(logging.INFO):
        reply = asyncio.run(service.ai_agent_service._process_events(_events(event)))

    assert reply.endswith("您好")
    assert "Model usage: prompt=5274 cache_read=5185 cache_write=0 output=56" in caplog.text
