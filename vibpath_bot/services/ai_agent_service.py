"""
AI Agent Service
Manages Gemini AI agent initialization, session management, and query execution
"""
import os
import json
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from vibpath_bot.tools.ai_tools import show_company_introduction, show_product_catalog, show_service_menu, show_product_details, show_detection_apps, show_manual_download
from vibpath_bot.config.agent_prompts import get_agent_instruction
from vibpath_bot.utils.logger import ai_logger as logger
from vibpath_bot.utils.exceptions import AIAgentError, ToolExecutionError, SessionError


class AIAgentService:
    """Service for managing AI agent and sessions"""

    def __init__(self):
        """Initialize AI agent service"""
        # Initialize ADK client with AI tools
        ai_model = os.getenv("GOOGLE_AI_MODEL", "gemini-3.0-flash")
        self.root_agent = Agent(
            name="vibpath_agent",
            model=ai_model,
            description="VibPath智能客服",
            instruction=get_agent_instruction("vibpath_customer_service"),
            tools=[show_company_introduction, show_product_catalog, show_service_menu, show_product_details, show_detection_apps, show_manual_download],
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

        # Parse tool arguments
        args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}

        # Add request_host if the tool accepts it
        if tool_name in ['show_company_introduction', 'show_product_catalog']:
            args['request_host'] = request_host

        # Tool mapping
        tool_map = {
            'show_company_introduction': show_company_introduction,
            'show_product_catalog': show_product_catalog,
            'show_service_menu': show_service_menu,
            'show_product_details': show_product_details
        }

        if tool_name in tool_map:
            logger.info(f"Executing tool: {tool_name}")
            try:
                result = tool_map[tool_name](**args)
                logger.debug(f"Tool '{tool_name}' executed successfully")
                return result
            except Exception as e:
                logger.error(f"Tool '{tool_name}' execution failed: {str(e)}", exc_info=True)
                raise ToolExecutionError(f"Failed to execute tool '{tool_name}'", detail=str(e))

        logger.warning(f"Unknown tool requested: {tool_name}")
        return None

    async def _process_events(self, events, request_host: str = None):
        """
        Process agent events and handle tool calls or final responses

        Args:
            events: Async iterator of agent events
            request_host: Request host for dynamic URL generation

        Returns:
            Final response (string or dict)
        """
        final_response = "Agent did not produce a final response."

        async for event in events:
            # Check for tool calls
            if hasattr(event, 'tool_calls') and event.tool_calls:
                for tool_call in event.tool_calls:
                    try:
                        tool_result = self._execute_tool(tool_call, request_host)
                        if tool_result:
                            logger.info("Tool executed successfully, returning structured response")
                            return tool_result
                    except ToolExecutionError as e:
                        logger.error(f"Tool execution error: {e.message}")
                    except Exception as e:
                        logger.error(f"Unexpected tool execution error: {str(e)}", exc_info=True)

            # Check for final response
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response = "AI客服阿弦:\n" + event.content.parts[0].text
                elif event.actions and event.actions.escalate:
                    final_response = f"Agent escalated: {event.error_message or 'No specific message.'}"
                break

        return final_response

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

            # Execute the agent logic and process events
            events = self.runner.run_async(
                user_id=user_id, session_id=session_id, new_message=content
            )
            final_response = await self._process_events(events, request_host)

        except ValueError as e:
            # Handle errors, especially session not found
            logger.warning(f"ValueError during agent execution: {str(e)}")

            # Recreate session if it was lost
            if "Session not found" in str(e):
                logger.info(f"Recreating lost session for user '{user_id}'")
                self.active_sessions.pop(user_id, None)
                session_id = await self.get_or_create_session(user_id)

                # Retry with the new session
                try:
                    events = self.runner.run_async(
                        user_id=user_id, session_id=session_id, new_message=content
                    )
                    final_response = await self._process_events(events, request_host)
                except Exception as e2:
                    logger.error(f"Retry failed: {str(e2)}", exc_info=True)
                    raise AIAgentError("Agent execution failed after retry", detail=str(e2))
            else:
                logger.error(f"Agent execution error: {str(e)}", exc_info=True)
                raise AIAgentError("Agent execution failed", detail=str(e))
        except Exception as e:
            error_str = str(e).lower()
            # Check for rate limit (429) errors
            if "429" in error_str or "rate limit" in error_str or "quota" in error_str or "resource exhausted" in error_str:
                logger.warning(f"Rate limit (429) error for user '{user_id}': {str(e)}")
                return "⚠️ AI 服務目前繁忙中（429 錯誤），請稍後再試或聯絡技術人員。"
            logger.error(f"Unexpected error during agent execution: {str(e)}", exc_info=True)
            raise AIAgentError("Unexpected agent error", detail=str(e))

        logger.info(f"Agent response for '{user_id}': {str(final_response)[:50]}...")
        return final_response


# Create global service instance
ai_agent_service = AIAgentService()
