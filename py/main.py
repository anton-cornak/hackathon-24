import os
import logging
from pprint import pprint

from fastapi import FastAPI
import uvicorn
from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fastapi_app = FastAPI()
bot_token = os.environ.get("SLACK_BOT_TOKEN")
signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
app_token = os.environ.get("SLACK_APP_TOKEN")

# Slack app
slack_app = AsyncApp(token=bot_token, signing_secret=signing_secret)
slack_handler = AsyncSlackRequestHandler(slack_app)

@fastapi_app.post("/slack/events")
async def slack_events(request):
    logger.info("Received Slack event")
    return await slack_handler.handle(request)

@slack_app.message("hello")
async def handle_message(body, say):
    pprint(body)
    user_id = body['user']
    logger.info(f"Received 'hello' message from user {user_id}")
    await say(f"Hey there <@{user_id}>!")

@slack_app.event("message")
async def handle_message_events(body, logger):
    event = body.get("event", {})
    text = event.get("text", "")
    user = event.get("user", "")
    channel = event.get("channel", "")
    thread_ts = str(event.get("thread_ts", event.get("ts")))

    await slack_app.client.chat_postMessage(channel=channel, text=f"You said: {text}", thread_ts=thread_ts)

async def start_fastapi():
    logger.info("Starting FastAPI")
    config = uvicorn.Config(fastapi_app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def start_slack():
    logger.info("Starting Slack")
    handler = AsyncSocketModeHandler(slack_app, app_token)
    await handler.start_async()

async def main():
    await asyncio.gather(start_fastapi(), start_slack())

if __name__ == "__main__":
    logger.info("Starting main function")
    asyncio.run(main())