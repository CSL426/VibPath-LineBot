import os
import sys
import asyncio
from io import BytesIO

import aiohttp
from fastapi import Request, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from zoneinfo import ZoneInfo

from linebot.models import MessageEvent, PostbackEvent, TextSendMessage
from linebot.exceptions import InvalidSignatureError
from linebot.aiohttp_async_http_client import AiohttpAsyncHttpClient
from linebot import AsyncLineBotApi, WebhookParser
# No tools needed for now - just using agent for general conversation
from multi_tool_agent.utils.line_utils import set_line_bot_api, before_reply_display_loading_animation
from vibpath_bot.handlers.message_handler import MessageHandler
from vibpath_bot.handlers.postback_handler import postback_handler
from vibpath_bot.config.agent_prompts import get_agent_instruction
from google.adk.agents import Agent

# Import necessary session components
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.genai import types

# Google AI API configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or ""

# LINE Bot configuration
channel_secret = os.getenv("ChannelSecret", None)
channel_access_token = os.getenv("ChannelAccessToken", None)

# Validate environment variables
if channel_secret is None:
    print("Specify ChannelSecret as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify ChannelAccessToken as environment variable.")
    sys.exit(1)
if not GOOGLE_API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY via env var or code.")

# Initialize the FastAPI app for LINEBot
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

session = aiohttp.ClientSession()
async_http_client = AiohttpAsyncHttpClient(session)
line_bot_api = AsyncLineBotApi(channel_access_token, async_http_client)
parser = WebhookParser(channel_secret)

# Set LINE Bot API instance for utilities
set_line_bot_api(line_bot_api)

# Initialize message handler for Flex Messages
message_handler = MessageHandler()

# Initialize ADK client
root_agent = Agent(
    name="vibpath_agent",
    model="gemini-2.0-flash",
    description="VibPath智能客服",
    instruction=get_agent_instruction("vibpath_customer_service"),
    tools=[],
)
print(f"Agent '{root_agent.name}' created.")

# --- Session Management ---
# Key Concept: SessionService stores conversation history & state.
# InMemorySessionService is simple, non-persistent storage for this tutorial.
session_service = InMemorySessionService()

# Define constants for identifying the interaction context
APP_NAME = "linebot_adk_app"
# Instead of fixed user_id and session_id, we'll now manage them dynamically

# Dictionary to track active sessions
active_sessions = {}

# Create a function to get or create a session for a user


async def get_or_create_session(user_id):  # Make function async
    if user_id not in active_sessions:
        # Create a new session for this user
        session_id = f"session_{user_id}"
        # Add await for the async session creation
        await session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )
        active_sessions[user_id] = session_id
        print(
            f"New session created: App='{APP_NAME}', User='{user_id}', Session='{session_id}'"
        )
    else:
        # Use existing session
        session_id = active_sessions[user_id]
        print(
            f"Using existing session: App='{APP_NAME}', User='{user_id}', Session='{session_id}'"
        )

    return session_id


# Key Concept: Runner orchestrates the agent execution loop.
runner = Runner(
    agent=root_agent,  # The agent we want to run
    app_name=APP_NAME,  # Associates runs with our app
    session_service=session_service,  # Uses our session manager
)
print(f"Runner created for agent '{runner.agent.name}'.")


@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run"""
    return {"status": "healthy", "service": "linebot-adk"}


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "LINE Bot ADK is running", "status": "active"}


@app.post("/callback")
async def generic_callback(request: Request):
    """Generic callback endpoint for other web services"""
    try:
        # Get request body
        body = await request.body()
        headers = dict(request.headers)

        # Log the callback for debugging
        print(f"Received callback from: {headers.get('user-agent', 'Unknown')}")
        print(f"Callback body: {body.decode('utf-8', errors='ignore')}")

        # TODO: Add your callback processing logic here
        # You can handle different services based on headers or body content

        return {"status": "success", "message": "Callback received"}

    except Exception as e:
        print(f"Error processing callback: {str(e)}")
        return {"status": "error", "message": "Failed to process callback"}


@app.get("/callback")
async def callback_info():
    """Info about callback endpoint"""
    return {
        "message": "Generic callback endpoint",
        "usage": "POST to this endpoint for web service callbacks",
        "url": "/callback"
    }


@app.post("/webhook")
async def handle_callback(request: Request):
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = await request.body()
    body = body.decode()

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if isinstance(event, MessageEvent) and event.message.type == "text":
            # Process text message
            msg = event.message.text
            user_id = event.source.user_id
            print(f"Received message: {msg} from user: {user_id}")

            # Detect message type for appropriate handling
            message_type = message_handler.detect_message_type(msg)

            # Get request host for dynamic URL generation
            request_host = request.headers.get("host")

            # Handle special commands without calling agent
            if message_type == "menu":
                reply_msg = message_handler.create_service_menu()
                await line_bot_api.reply_message(event.reply_token, reply_msg)
                continue
            elif message_type == "help":
                reply_msg = message_handler.create_help_message()
                await line_bot_api.reply_message(event.reply_token, reply_msg)
                continue
            elif message_type == "frequency":
                reply_msg = message_handler.create_frequency_services_carousel(request_host)
                await line_bot_api.reply_message(event.reply_token, reply_msg)
                continue
            elif message_type == "business":
                reply_msg = message_handler.create_company_introduction(request_host)
                await line_bot_api.reply_message(event.reply_token, reply_msg)
                continue

            # Show loading animation while processing
            try:
                await before_reply_display_loading_animation(user_id, loading_seconds=60)
            except Exception as e:
                print(f"載入動畫顯示失敗: {e}")

            # Use the agent for general conversation
            response = await call_agent_async(msg, user_id)
            reply_msg = TextSendMessage(
                text=response,
                quick_reply=message_handler.create_quick_reply_services()
            )

            await line_bot_api.reply_message(event.reply_token, reply_msg)

        elif isinstance(event, PostbackEvent):
            # Handle postback events from buttons
            user_id = event.source.user_id
            postback_data = event.postback.data
            print(f"Received postback: {postback_data} from user: {user_id}")

            # Process postback with handler
            reply_msg = postback_handler.handle_postback(postback_data, user_id)
            await line_bot_api.reply_message(event.reply_token, reply_msg)

        elif isinstance(event, MessageEvent) and event.message.type == "image":
            # Handle image messages if needed
            continue
        else:
            # Skip other event types
            continue

    return "OK"


async def call_agent_async(query: str, user_id: str) -> str:
    """Sends a query to the agent and prints the final response."""
    print(f"\n>>> User Query: {query}")

    # Get or create a session for this user
    session_id = await get_or_create_session(user_id)  # Add await

    # Prepare the user's message in ADK format
    content = types.Content(role="user", parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response."  # Default

    try:
        # Key Concept: run_async executes the agent logic and yields Events.
        # We iterate through events to find the final answer.
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            # You can uncomment the line below to see *all* events during execution
            # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

            # Key Concept: is_final_response() marks the concluding message for the turn.
            if event.is_final_response():
                if event.content and event.content.parts:
                    # Assuming text response in the first part
                    final_response_text = event.content.parts[0].text
                elif (
                    event.actions and event.actions.escalate
                ):  # Handle potential errors/escalations
                    final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
                # Add more checks here if needed (e.g., specific error codes)
                break  # Stop processing events once the final response is found
    except ValueError as e:
        # Handle errors, especially session not found
        print(f"Error processing request: {str(e)}")
        # Recreate session if it was lost
        if "Session not found" in str(e):
            active_sessions.pop(user_id, None)  # Remove the invalid session
            session_id = await get_or_create_session(
                user_id
            )  # Create a new one # Add await
            # Try again with the new session
            try:
                async for event in runner.run_async(
                    user_id=user_id, session_id=session_id, new_message=content
                ):
                    # Same event handling code as above
                    if event.is_final_response():
                        if event.content and event.content.parts:
                            final_response_text = event.content.parts[0].text
                        elif event.actions and event.actions.escalate:
                            final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
                        break
            except Exception as e2:
                final_response_text = f"Sorry, I encountered an error: {str(e2)}"
        else:
            final_response_text = f"Sorry, I encountered an error: {str(e)}"

    print(f"<<< Agent Response: {final_response_text}")
    return final_response_text


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8080))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
