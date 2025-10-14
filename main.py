import os
import sys

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

import aiohttp
from fastapi import Request, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from linebot.models import MessageEvent, PostbackEvent, FollowEvent
from linebot.exceptions import InvalidSignatureError
from linebot.aiohttp_async_http_client import AiohttpAsyncHttpClient
from linebot import AsyncLineBotApi, WebhookParser

# Import handlers and services
from vibpath_bot.utils.line_utils import set_line_bot_api
from vibpath_bot.handlers.webhook_handler import WebhookHandler
from vibpath_bot.api.user_preferences_api import router as user_preferences_router
from vibpath_bot.config.env_config import settings

# Initialize the FastAPI app for LINEBot
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize LINE Bot API
session = aiohttp.ClientSession()
async_http_client = AiohttpAsyncHttpClient(session)
line_bot_api = AsyncLineBotApi(settings.channel_access_token, async_http_client)
parser = WebhookParser(settings.channel_secret)

# Set LINE Bot API instance for utilities
set_line_bot_api(line_bot_api)

# Initialize webhook handler
webhook_handler = WebhookHandler(line_bot_api)

# Include API routers
app.include_router(user_preferences_router)


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
    """LINE webhook endpoint"""
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = await request.body()
    body = body.decode()

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Get request host for dynamic URL generation
    request_host = request.headers.get("host")

    for event in events:
        if isinstance(event, FollowEvent):
            # Handle follow event (user adds bot as friend)
            await webhook_handler.handle_follow_event(event)

        elif isinstance(event, MessageEvent) and event.message.type == "text":
            # Handle text message
            await webhook_handler.handle_text_message(event, request_host)

        elif isinstance(event, PostbackEvent):
            # Handle postback events from buttons
            await webhook_handler.handle_postback_event(event, request_host)

        elif isinstance(event, MessageEvent) and event.message.type == "image":
            # Handle image messages if needed
            continue
        else:
            # Skip other event types
            continue

    return "OK"


if __name__ == "__main__":
    import uvicorn

    print(f"Starting server on port {settings.port}")
    uvicorn.run(app, host="0.0.0.0", port=settings.port)
