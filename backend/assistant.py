import os
import time
from openai import AzureOpenAI

from dotenv import load_dotenv
from openai.pagination import SyncCursorPage
from openai.types.beta.threads import Message

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview"
)

# assistant = client.beta.assistants.create(
#   model="gpt-4o", # replace with model deployment name.
#   instructions="",
#   tools=[{"type":"function","function":{"name":"get_weather","description":"Determine weather in my location","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and state e.g. Seattle, WA"},"unit":{"type":"string","enum":["c","f"]}},"required":["location"]},"strict":False}}],
#   tool_resources={},
#   temperature=1,
#   top_p=1
# )
#
# print(f"Assistant created: {assistant}")

assistant_id = os.getenv("ASSISTANT_ID")

# Define new tools
new_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Determine weather in my location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state e.g. Seattle, WA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["c", "f"]
                    }
                },
                "required": ["location"]
            },
            "strict": False
        }
    }
]


def get_weather(location, unit='c'):
    """
    Determine weather in a specific location.

    Parameters:
    location (str): The city and state e.g. Seattle, WA
    unit (str): The unit of temperature, either 'c' for Celsius or 'f' for Fahrenheit. Default is 'c'.

    Returns:
    dict: A dictionary containing weather information for the specified location.
    """
    # Example implementation (replace with actual API call)
    weather_data = {
        "location": location,
        "temperature": 20,  # Example temperature
        "unit": unit,
        "description": "Partly cloudy"
    }
    return weather_data


# Update the assistant with new tools
# assistant = client.beta.assistants.update(
#     assistant_id=assistant_id,
#     tools=new_tools
# )


def ask(question: str) -> str:
    # Create a thread
    thread = client.beta.threads.create()

    # Add a user question to the thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=question
    )

    # Run the thread
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    while True:
        while run.status in ['queued', 'in_progress', 'cancelling']:
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        if run.status == 'completed':

            messages: SyncCursorPage[Message] = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            for page in messages:
                for block in page.content:
                    if block.type == "text":
                        # Just return the first text block value
                        return block.text.value
            break
        elif run.status == 'requires_action':
            # the assistant requires calling some functions
            # and submit the tool outputs back to the run
            for tool in run.required_action.submit_tool_outputs.tool_calls:
                # get data from the weather function
                if tool.function.name == "get_weather":
                    weather = get_weather("Kosice", "c")

                    run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=[{
                            "tool_call_id": tool.id,
                            "output": str(weather)
                        }]
                    )

        else:
            # Error
            print(run.status)
            print(run.last_error)
            break
