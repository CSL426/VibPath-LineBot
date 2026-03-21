"""
Webhook Event Handler
Handles LINE webhook events (message, postback, follow)
"""
from linebot.models import MessageEvent, PostbackEvent, FollowEvent, TextSendMessage, FlexSendMessage
from linebot import AsyncLineBotApi
from vibpath_bot.utils.line_utils import before_reply_display_loading_animation
from vibpath_bot.handlers.message_handler import MessageHandler
from vibpath_bot.handlers.postback_handler import postback_handler
from vibpath_bot.handlers.ai_toggle_handler import ai_toggle_handler
from vibpath_bot.config.admin_config import admin_config
from vibpath_bot.services.user_preference_service import user_preference_service
from vibpath_bot.services.ai_agent_service import ai_agent_service
from vibpath_bot.utils.logger import webhook_logger as logger
from vibpath_bot.utils.exceptions import AIAgentError


class WebhookHandler:
    """Handler for LINE webhook events"""

    def __init__(self, line_bot_api: AsyncLineBotApi):
        """
        Initialize webhook handler

        Args:
            line_bot_api: LINE Bot API instance
        """
        self.line_bot_api = line_bot_api
        self.message_handler = MessageHandler()

    async def handle_follow_event(self, event: FollowEvent):
        """
        Handle follow event (user adds bot as friend)

        Args:
            event: LINE FollowEvent
        """
        user_id = event.source.user_id
        logger.info(f"New user followed: {user_id}")

        # Send welcome message
        welcome_messages = self.message_handler.create_welcome_message()
        await self.line_bot_api.reply_message(event.reply_token, welcome_messages)

    async def handle_text_message(self, event: MessageEvent, request_host: str = None):
        """
        Handle text message event

        Args:
            event: LINE MessageEvent
            request_host: Request host for dynamic URL generation
        """
        msg = event.message.text
        user_id = event.source.user_id
        logger.info(f"Received message from {user_id}: {msg[:50]}...")

        # Check if user is admin
        is_admin = admin_config.is_admin(user_id)

        # Handle admin commands (pause/resume)
        if is_admin:
            admin_reply = await self._handle_admin_commands(event, msg)
            if admin_reply:
                return  # Admin command was handled

        # Check if bot is paused (applies to everyone)
        if admin_config.check_pause_status():
            # Don't reply anything during pause
            return

        # Check if user wants to toggle AI reply
        if msg.strip().lower() in ['ai開關', 'ai設定']:
            reply_msg = ai_toggle_handler.handle_toggle(user_id)
            await self.line_bot_api.reply_message(event.reply_token, reply_msg)
            return

        # Check if user wants to check AI status
        if msg.strip().lower() in ['ai狀態', 'ai status']:
            reply_msg = ai_toggle_handler.get_status(user_id)
            await self.line_bot_api.reply_message(event.reply_token, reply_msg)
            return

        # Detect message type for appropriate handling
        message_type = self.message_handler.detect_message_type(msg)

        # Check if AI reply is enabled for this user
        is_ai_enabled = user_preference_service.is_ai_reply_enabled(user_id)
        logger.debug(f"AI reply status for {user_id}: {'Enabled' if is_ai_enabled else 'Disabled'}")

        # Show loading animation while processing (only if AI enabled)
        if is_ai_enabled:
            try:
                await before_reply_display_loading_animation(user_id, loading_seconds=60)
            except Exception as e:
                logger.warning(f"Failed to display loading animation: {e}")

        # Try AI agent first with tools (only if AI enabled)
        if is_ai_enabled:
            try:
                agent_response = await ai_agent_service.call_agent(msg, user_id, request_host)

                # Check if agent returned a structured response
                if isinstance(agent_response, dict):
                    if agent_response.get("type") == "flex_message":
                        reply_msg = FlexSendMessage(
                            alt_text=agent_response.get("alt_text", "VibPath 服務"),
                            contents=agent_response["content"]
                        )
                        await self.line_bot_api.reply_message(event.reply_token, reply_msg)
                        return
                    elif agent_response.get("type") == "text_with_quick_reply":
                        reply_msg = TextSendMessage(
                            text=agent_response["content"],
                            quick_reply=self.message_handler.create_quick_reply_basic()
                        )
                        await self.line_bot_api.reply_message(event.reply_token, reply_msg)
                        return

                # If agent returned regular text, use it
                if isinstance(agent_response, str) and agent_response.strip():
                    reply_msg = TextSendMessage(
                        text=agent_response,
                        quick_reply=self.message_handler.create_quick_reply_basic()
                    )
                    await self.line_bot_api.reply_message(event.reply_token, reply_msg)
                    return

            except AIAgentError as e:
                logger.error(f"AI Agent failed: {e.message}", exc_info=True)
                # Fall through to keyword detection
            except Exception as e:
                logger.error(f"Unexpected error in AI agent: {str(e)}", exc_info=True)
                # Fall through to keyword detection

        # Fallback to keyword detection (only for specific keywords)
        # When AI is disabled, only respond to specific menu keywords
        logger.debug(f"Checking keyword detection for: {msg}")
        reply_msg = None

        if message_type == "menu":
            reply_msg = self.message_handler.create_service_menu()
            # Add quick reply to flex message
            reply_msg.quick_reply = self.message_handler.create_quick_reply_basic()
        elif message_type == "help":
            reply_msg = self.message_handler.create_help_message()
        elif message_type == "frequency":
            reply_msg = self.message_handler.create_frequency_services_carousel(request_host)
            # Add quick reply to flex message
            reply_msg.quick_reply = self.message_handler.create_quick_reply_products()
        elif message_type == "business":
            reply_msg = self.message_handler.create_company_introduction(request_host)
            # Add quick reply to flex message
            reply_msg.quick_reply = self.message_handler.create_quick_reply_basic()
        elif message_type == "manual":
            reply_msg = self.message_handler.create_manual_download_card(request_host)
            # Add quick reply to flex message
            reply_msg.quick_reply = self.message_handler.create_quick_reply_basic()
        elif not is_ai_enabled:
            # AI is disabled and no keyword match - don't reply
            logger.info(f"AI disabled and no keyword match for '{msg}' - not replying")
            return
        else:
            # AI is enabled but no keyword match - show error
            reply_msg = TextSendMessage(
                text="抱歉，我暫時無法處理您的請求，請稍後再試或使用快速回覆按鈕。",
                quick_reply=self.message_handler.create_quick_reply_basic()
            )

        if reply_msg:
            await self.line_bot_api.reply_message(event.reply_token, reply_msg)

    async def handle_postback_event(self, event: PostbackEvent, request_host: str = None):
        """
        Handle postback event from buttons

        Args:
            event: LINE PostbackEvent
            request_host: Request host for dynamic URL generation
        """
        user_id = event.source.user_id
        postback_data = event.postback.data
        logger.info(f"Received postback from {user_id}: {postback_data}")

        # Process postback with handler
        reply_msg = postback_handler.handle_postback(postback_data, user_id, request_host)
        await self.line_bot_api.reply_message(event.reply_token, reply_msg)

    async def _handle_admin_commands(self, event: MessageEvent, msg: str) -> bool:
        """
        Handle admin commands (pause/resume/status/help)

        Args:
            event: LINE MessageEvent
            msg: Message text

        Returns:
            bool: True if command was handled, False otherwise
        """
        # Check for pause command
        pause_duration = admin_config.parse_pause_command(msg)
        if pause_duration is not None:
            admin_config.pause_bot(pause_duration, event.source.user_id)
            pause_info = admin_config.get_pause_info()
            reply_text = f"✅ Bot 已暫停\n⏰ 暫停時間: {pause_duration} 分鐘\n📅 恢復時間: {pause_info['pause_until']}"
            await self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_text)
            )
            return True

        # Check for resume command
        if admin_config.parse_resume_command(msg):
            admin_config.resume_bot(event.source.user_id)
            reply_text = "✅ Bot 已恢復運作"
            await self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_text)
            )
            return True

        # Check for status command
        if msg.strip().lower() in ['狀態', 'status']:
            pause_info = admin_config.get_pause_info()
            if pause_info['paused']:
                reply_text = f"⏸️ Bot 目前暫停中\n⏰ 剩餘時間: {pause_info['remaining_minutes']} 分鐘\n📅 恢復時間: {pause_info['pause_until']}"
            else:
                reply_text = "✅ Bot 目前正常運作"
            await self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_text)
            )
            return True

        # Check for help command
        if admin_config.parse_help_command(msg):
            reply_text = admin_config.get_admin_help_message()
            await self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_text)
            )
            return True

        return False
