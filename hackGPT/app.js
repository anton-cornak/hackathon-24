const { App } = require('@slack/bolt');

// Initializes your app with your bot token and signing secret
const app = new App({
    token: process.env.SLACK_BOT_TOKEN,
    signingSecret: process.env.SLACK_SIGNING_SECRET,
    socketMode: true, // add this
    appToken: process.env.SLACK_APP_TOKEN // add this
});

app.message('hello', async ({ message, say }) => {
    // say() sends a message to the channel where the event was triggered
    await say(`Hey there <@${message.user}>!`);
});

// When a user joins the team, send a message in a predefined channel asking them to introduce themselves
app.event('member_left_channel', async ({ event, client, logger }) => {
    try {
        // Call chat.postMessage with the built-in client
        const result = await client.chat.postMessage({
            channel: event.channel,
            text: `Good bye, <@${event.user.id}>!`
        });
        logger.info(result);
    }
    catch (error) {
        logger.error(error);
    }
});

app.event('member_joined_channel', async ({ event, client, logger }) => {
    try {
        // Call chat.postMessage with the built-in client
        const result = await client.chat.postMessage({
            channel: event.channel,
            text: `Hello, <@${event.user.id}>!`
        });
        logger.info(result);
    }
    catch (error) {
        logger.error(error);
    }
});
(async () => {
    // Start your app
    await app.start(process.env.PORT || 3000);

    console.log('⚡️ Bolt app is running!');
})();