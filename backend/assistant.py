import json
import os
import time
from openai import AzureOpenAI

from dotenv import load_dotenv
from openai.pagination import SyncCursorPage
from openai.types.beta.threads import Message

import booking.mock as booking

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview"
)

assistant_id = os.getenv("ASSISTANT_ID")

# Define new tools
new_tools = [
    {
        "type": "file_search", "file_search": {"ranking_options": {"ranker": "default_2024_08_21", "score_threshold": 0}}
    },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "booking-get_available_seats",
    #         "description": "Vyhladaj volne miesta na sedenie",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "floor_number": {
    #                     "type": "integer",
    #                     "description": "Cislo poschodia, napr. 2"
    #                 }
    #             },
    #             "required": ["floor_number"]
    #         },
    #         "strict": False
    #     }
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "booking-book_on_floor",
    #         "description": "Zarezervuj volne miesto na sedenie",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "floor_number": {
    #                     "type": "integer",
    #                     "description": "Cislo poschodia, napr. 2"
    #                 }
    #             },
    #             "required": ["floor_number"]
    #         },
    #         "strict": False
    #     }
    # }
]

# Update the assistant with new tools
assistant = client.beta.assistants.update(
    assistant_id=assistant_id,
    tools=new_tools
)

tools = {
    "booking-get_available_seats": booking.get_available_seats,
    "booking-book_on_floor": booking.book_on_floor
}

def file_name_to_md_link(file_name: str) -> str:
    # TODO: figure this out
    return f"[{file_name}](https://google.com/?q={file_name})"


def ask(question: str) -> str:
    filenames = []

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
            time.sleep(1)  # TODO: get rid of sleep and make this async
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
                        annotations = block.text.annotations
                        for annotation in annotations:
                            if annotation.type == "file_citation":
                                file_id = annotation.file_citation.file_id
                                file = client.files.retrieve(file_id)
                                filenames.append(file_name_to_md_link(file.filename))

                        # Just return the first text block value
                        text = block.text.value
                        return text + "\n\n" + "\n".join(filenames)

            # Ooops, it looks like an empty or non-textual response
            return "Error"

        elif run.status == 'requires_action':
            # the assistant requires calling some functions
            # and submit the tool outputs back to the run
            for tool in run.required_action.submit_tool_outputs.tool_calls:
                function_name = tool.function.name
                if function_name in tools:
                    function = tools[function_name]
                    args = json.loads(tool.function.arguments)

                    result = function(**args)
                    output = json.dumps(result, default=lambda x: x.__dict__)
                    print(output)

                    run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=[{
                            "tool_call_id": tool.id,
                            "output": output
                        }]
                    )
        else:
            # Error
            print(run.status)
            print(run.last_error)
            return "Error"
