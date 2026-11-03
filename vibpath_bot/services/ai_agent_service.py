"""
AI Agent Service
Manages Gemini AI agent initialization, session management, and query execution
"""
import os
import json
import re
from anthropic import AsyncAnthropic
from google.adk.agents import Agent
from google.adk.models.anthropic_llm import AnthropicGenerateContentConfig, AnthropicLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from opencc import OpenCC
from vibpath_bot.tools.ai_tools import show_company_introduction, show_product_catalog, show_service_menu, show_product_details, show_detection_apps, show_manual_download
from vibpath_bot.config.agent_prompts import get_agent_instruction
from vibpath_bot.config.env_config import settings
from vibpath_bot.utils.logger import ai_logger as logger
from vibpath_bot.utils.exceptions import AIAgentError, ToolExecutionError, SessionError

# Shared tool mapping — single source of truth for both execution paths
TOOL_MAP = {
    'show_company_introduction': show_company_introduction,
    'show_product_catalog': show_product_catalog,
    'show_service_menu': show_service_menu,
    'show_product_details': show_product_details,
    'show_detection_apps': show_detection_apps,
    'show_manual_download': show_manual_download,
}
TOOLS_WITH_HOST = {'show_company_introduction', 'show_product_catalog'}

# User-facing reply when the AI service is rate-limited or overloaded
BUSY_MESSAGE = "⚠️ AI 服務目前繁忙中，請稍後再試。"


_S2T = OpenCC("s2t")


def _to_traditional(text: str) -> str:
    """Fix the stray simplified characters models mix in despite the prompt.

    Only characters outside Big5 are converted: converting whole text also rewrites
    valid Traditional, e.g. 台→臺, 干擾→幹擾, 了解→瞭解.
    """
    def convert(char: str) -> str:
        try:
            char.encode("big5")
            return char
        except UnicodeEncodeError:
            return _S2T.convert(char)

    # 「于」本身在 Big5 內不會被轉，但「关于」只轉一半會變成「關于」
    return "".join(convert(char) for char in text).replace("關于", "關於")


def _build_model():
    """Return (model, generate_content_config) for AI_MODEL."""
    ai_model = os.getenv("AI_MODEL", "claude-haiku-5-5")
    if not ai_model.startswith("claude"):
        return ai_model, None

    workspace_id = os.getenv("ANTHROPIC_WORKSPACE_ID")
    client = AsyncAnthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        default_headers={"anthropic-workspace-id": workspace_id} if workspace_id else None,
        timeout=30.0,
        max_retries=1,
    )
    return (
        AnthropicLlm(model=ai_model, max_tokens=2048, client=client),
        AnthropicGenerateContentConfig(effort="low"),
    )


def _reply_with_tool_result(tool, args, tool_context, tool_response):
    """工具的卡片或固定文字就是給客人的回覆，不需要模型再摘要一次。"""
    tool_context.actions.skip_summarization = True
    return None


class AIAgentService:
    """Service for managing AI agent and sessions"""

    def __init__(self):
        """Initialize AI agent service"""
        # Initialize ADK client with AI tools
        ai_model, generate_content_config = _build_model()
        self.root_agent = Agent(
            name="vibpath_agent",
            model=ai_model,
            description="VibPath智能客服",
            instruction=get_agent_instruction("vibpath_customer_service"),
            tools=[show_company_introduction, show_product_catalog, show_service_menu, show_product_details, show_detection_apps, show_manual_download],
            after_tool_callback=_reply_with_tool_result,
            generate_content_config=generate_content_config,
        )
        logger.info(f"Agent '{self.root_agent.name}' created successfully")

        # Session Management
        self.session_service = InMemorySessionService()
        self.app_name = "linebot_adk_app"
        self.active_sessions = {}

        # Initialize runner
        self.runner = Runner(
            agent=self.root_agent,
            app_name=self.app_name,
            session_service=self.session_service,
        )
        logger.info(f"Runner created for agent '{self.runner.agent.name}'")

    async def get_or_create_session(self, user_id: str) -> str:
        """
        Get or create a session for a user

        Args:
            user_id: LINE user ID

        Returns:
            str: Session ID

        Raises:
            SessionError: If session creation fails
        """
        try:
            if user_id not in self.active_sessions:
                # Create a new session for this user
                session_id = f"session_{user_id}"
                await self.session_service.create_session(
                    app_name=self.app_name, user_id=user_id, session_id=session_id
                )
                self.active_sessions[user_id] = session_id
                logger.info(f"New session created for user '{user_id}': {session_id}")
            else:
                # Use existing session
                session_id = self.active_sessions[user_id]
                logger.debug(f"Using existing session for user '{user_id}': {session_id}")

            return session_id
        except Exception as e:
            logger.error(f"Failed to create session for user '{user_id}': {str(e)}", exc_info=True)
            raise SessionError(f"Session creation failed", detail=str(e))

    def _execute_tool(self, tool_call, request_host: str = None):
        """
        Execute a tool based on tool_call information

        Args:
            tool_call: Tool call object from agent event
            request_host: Request host for dynamic URL generation

        Returns:
            Tool execution result (dict or None)
        """
        tool_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
        return self._invoke_tool(tool_name, args, request_host)

    def _clean_markdown(self, text: str) -> str:
        """
        Remove markdown formatting from text for LINE display

        Args:
            text: Text with potential markdown formatting

        Returns:
            str: Clean text without markdown
        """
        # Remove bold **text** or __text__
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'__(.+?)__', r'\1', text)
        # Remove italic *text* or _text_
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'_(.+?)_', r'\1', text)
        # Remove markdown links [text](url) -> text (url)
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'\1 \2', text)
        # Remove bullet points
        text = re.sub(r'^\s*[\*\-]\s+', '• ', text, flags=re.MULTILINE)
        return text

    async def _process_events(self, events, request_host: str = None):
        """
        Process agent events and handle tool calls or final responses

        Args:
            events: Async iterator of agent events
            request_host: Request host for dynamic URL generation

        Returns:
            Final response (string or dict)
        """
        final_response = "抱歉，我暫時無法處理您的請求，請稍後再試或使用快速回覆按鈕。"
        tool_result = None

        # 拿到工具結果也要把事件讀完：提早離開的話工具回應不會寫進 session，
        # 模型會以為上一題還沒答完，之後每句話都重複呼叫同一個工具
        async for event in events:
            if event.error_code:
                logger.error(f"Model returned an error: {event.error_code} {event.error_message}")

            # Check for tool calls in multiple locations
            # Method 1: Check event.tool_calls
            if hasattr(event, 'tool_calls') and event.tool_calls:
                for tool_call in event.tool_calls:
                    try:
                        tool_result = tool_result or self._execute_tool(tool_call, request_host)
                    except ToolExecutionError as e:
                        logger.error(f"Tool execution error: {e.message}")
                    except Exception as e:
                        logger.error(f"Unexpected tool execution error: {str(e)}", exc_info=True)

            # Method 2: Check event.content.parts for function_call
            if hasattr(event, 'content') and event.content and hasattr(event.content, 'parts') and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        try:
                            tool_result = tool_result or self._execute_tool_from_function_call(part.function_call, request_host)
                        except ToolExecutionError as e:
                            logger.error(f"Tool execution error: {e.message}")
                        except Exception as e:
                            logger.error(f"Unexpected tool execution error: {str(e)}", exc_info=True)

            # Check for final response
            if event.is_final_response():
                if tool_result:
                    break
                if event.content and event.content.parts:
                    # Get only text parts
                    text_parts = [p.text for p in event.content.parts if hasattr(p, 'text') and p.text]
                    if text_parts:
                        raw_text = text_parts[0]
                        clean_text = _to_traditional(self._clean_markdown(raw_text))
                        final_response = "AI客服阿弦:\n" + clean_text
                elif event.actions and event.actions.escalate:
                    final_response = f"Agent escalated: {event.error_message or 'No specific message.'}"
                break

        return tool_result or final_response

    def _execute_tool_from_function_call(self, function_call, request_host: str = None):
        """Execute a tool from a function_call object in content parts."""
        tool_name = function_call.name
        args = dict(function_call.args) if function_call.args else {}
        return self._invoke_tool(tool_name, args, request_host)

    def _invoke_tool(self, tool_name: str, args: dict, request_host: str = None):
        """Shared tool invocation logic."""
        if tool_name in TOOLS_WITH_HOST:
            args['request_host'] = request_host

        if tool_name in TOOL_MAP:
            logger.info(f"Executing tool: {tool_name}")
            try:
                result = TOOL_MAP[tool_name](**args)
                return result
            except Exception as e:
                logger.error(f"Tool '{tool_name}' execution failed: {str(e)}", exc_info=True)
                raise ToolExecutionError(f"Failed to execute tool '{tool_name}'", detail=str(e))

        logger.warning(f"Unknown tool requested: {tool_name}")
        return None

    async def _run_and_process(self, user_id: str, session_id: str,
                               content, request_host: str = None):
        """Run agent and process events (single execution path)."""
        events = self.runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        )
        return await self._process_events(events, request_host)

    async def call_agent(self, query: str, user_id: str, request_host: str = None):
        """
        Send a query to the agent and get the final response

        Args:
            query: User's message text
            user_id: LINE user ID
            request_host: Request host for dynamic URL generation

        Returns:
            Agent response (string or dict)

        Raises:
            AIAgentError: If agent execution fails
        """
        logger.info(f"User query from '{user_id}': {query[:50]}...")

        try:
            # Get or create a session for this user
            session_id = await self.get_or_create_session(user_id)

            # Prepare the user's message in ADK format
            content = types.Content(role="user", parts=[types.Part(text=query)])

            final_response = await self._run_and_process(
                user_id, session_id, content, request_host
            )

        except ValueError as e:
            logger.warning(f"ValueError during agent execution: {str(e)}")

            if "Session not found" in str(e):
                logger.info(f"Recreating lost session for user '{user_id}'")
                self.active_sessions.pop(user_id, None)
                session_id = await self.get_or_create_session(user_id)
                try:
                    final_response = await self._run_and_process(
                        user_id, session_id, content, request_host
                    )
                except Exception as e2:
                    logger.error(f"Retry failed: {str(e2)}", exc_info=True)
                    raise AIAgentError("Agent execution failed after retry", detail=str(e2))
            else:
                logger.error(f"Agent execution error: {str(e)}", exc_info=True)
                raise AIAgentError("Agent execution failed", detail=str(e))
        except Exception as e:
            error_str = str(e).lower()
            is_rate_limit = "429" in error_str or "rate limit" in error_str or "quota" in error_str or "resource exhausted" in error_str
            is_overloaded = "503" in error_str or "unavailable" in error_str or "high demand" in error_str
            is_key_error = "api key" in error_str and ("invalid" in error_str or "expired" in error_str)

            if is_rate_limit or is_overloaded or is_key_error:
                if is_rate_limit:
                    reason = "rate limit (429)"
                elif is_overloaded:
                    reason = "model overloaded (503)"
                else:
                    reason = "API key invalid/expired"
                current_key = os.getenv("GOOGLE_API_KEY")
                untried_keys = [k for k in settings.get_fallback_keys() if k != current_key]
                if untried_keys:
                    last_error = None
                    for i, fallback_key in enumerate(untried_keys, start=1):
                        logger.warning(
                            f"{reason}, switching to fallback key {i}/{len(untried_keys)} for user '{user_id}'"
                        )
                        os.environ["GOOGLE_API_KEY"] = fallback_key
                        try:
                            final_response = await self._run_and_process(
                                user_id, session_id, content, request_host
                            )
                            break
                        except Exception as e2:
                            logger.warning(f"Fallback key {i}/{len(untried_keys)} also failed: {str(e2)}")
                            last_error = e2
                    else:
                        logger.error(f"All API keys exhausted for user '{user_id}': {str(last_error)}", exc_info=True)
                        if is_overloaded:
                            return BUSY_MESSAGE
                        raise AIAgentError("Agent execution failed with all API keys", detail=str(last_error))
                else:
                    logger.warning(f"{reason} and no fallback available for user '{user_id}': {str(e)}")
                    return BUSY_MESSAGE
            else:
                logger.error(f"Unexpected error during agent execution: {str(e)}", exc_info=True)
                raise AIAgentError("Unexpected agent error", detail=str(e))

        logger.info(f"Agent response for '{user_id}': {str(final_response)[:50]}...")
        return final_response


# Create global service instance
ai_agent_service = AIAgentService()
