import os
import logging
from pprint import pprint

from fastapi import FastAPI
import uvicorn
from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
import asyncio
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fastapi_app = FastAPI()
bot_token = os.environ.get("SLACK_BOT_TOKEN")
signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
app_token = os.environ.get("SLACK_APP_TOKEN")
api_token = os.environ.get("API_TOKEN")

# Slack app
slack_app = AsyncApp(token=bot_token, signing_secret=signing_secret)
slack_handler = AsyncSlackRequestHandler(slack_app)

@fastapi_app.post("/slack/events")
async def slack_events(request):
    logger.info("Received Slack event")
    return await slack_handler.handle(request)

@fastapi_app.get("/health")
async def health():
    return {"status": "ok"}

@slack_app.message("hello")
async def handle_message(body, say):
    pprint(body)
    user_id = body['user']
    logger.info(f"Received 'hello' message from user {user_id}")
    await say(f"Hey there <@{user_id}>!")

@slack_app.event("message")
async def handle_message_events(body, logger):
    pprint(body)
    event = body.get("event", {})
    text = event.get("text", "")
    user = event.get("user", "")
    channel = event.get("channel", "")
    thread_ts = str(event.get("thread_ts", event.get("ts")))
    status, resp = send_question(text, api_token)
    await slack_app.client.reactions_add(
        channel=channel,
        name="thumbsup",
        timestamp=thread_ts
    )
    # if status == 200:
    #     await slack_app.client.chat_postMessage(channel=channel, text=f"Response: {resp}", thread_ts=thread_ts)
    # else:
    #     await slack_app.client.chat_postMessage(channel=channel, text=f"Failed to get response from assistant. Response code: {status}", thread_ts=thread_ts)

async def start_fastapi():
    logger.info("Starting FastAPI")
    config = uvicorn.Config(fastapi_app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def start_slack():
    logger.info("Starting Slack")
    handler = AsyncSocketModeHandler(slack_app, app_token)
    await handler.start_async()

def send_question(question, api_key):
    url = "https://ca-hackathon-assistant.ashymeadow-57180c2e.swedencentral.azurecontainerapps.io/assistant"
    body = {
        "question": question
    }
    headers = {
        "X-API-KEY": api_key
    }
    response = requests.post(url, json=body, headers=headers)
    return response.status_code, response.json()

async def main():
    await asyncio.gather(start_fastapi(), start_slack())

if __name__ == "__main__":
    logger.info("Starting main function")
    asyncio.run(main())