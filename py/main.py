import os
from fastapi import FastAPI
import uvicorn
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
import asyncio

fastapi_app = FastAPI()
bot_token = os.environ.get("SLACK_BOT_TOKEN")
signing_secret = os.environ.get("SLACK_BOT_TOKEN")

# Slack app
slack_app = AsyncApp(token=bot_token, signing_secret=signing_secret)
slack_handler = AsyncSlackRequestHandler(slack_app)


@fastapi_app.post("/slack/events")
async def slack_events(request):
    return await slack_handler.handle(request)


@slack_app.message("hello")
async def handle_message(body, say):
    await say(f"Hey there <@{body['user']}>!")


async def start_fastapi():
    config = uvicorn.Config(fastapi_app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


async def start_slack():
    # Add your Slack app initialization logic if needed
    print("Slack app is ready to process events")


async def main():
    await asyncio.gather(start_fastapi(), start_slack())


if __name__ == "__main__":
    asyncio.run(main())
