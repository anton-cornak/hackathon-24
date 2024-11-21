import os
from pprint import pprint

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")

@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)
    pprint(body)
    event = body.get("event", {})
    text = event.get("text", "")
    user = event.get("user", "")
    channel = event.get("channel", "")
    thread_ts = str(event.get("thread_ts", event.get("ts")))

    app.client.chat_postMessage(channel=channel, text=f"You said: {text}", thread_ts=thread_ts)

@app.command("/hi")
def handle_hello_command(ack, respond, command):
    # Acknowledge the command request
    ack()
    # Respond to the command
    respond(f"Hello, <@{command['user_id']}>!")
# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()