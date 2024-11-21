import os
import openai
from pathlib import Path

from openai import OpenAI

# Set your OpenAI API key
api_key = os.environ.get('OPENAI_API_KEY')
# Define directories
base_dir = Path("./data")
alt_dir = base_dir / "alternatives"

# Create 'alternatives' subdirectory if it doesn't exist
alt_dir.mkdir(exist_ok=True)


# Function to generate alternative text using OpenAI
def generate_alternatives(content):
    prompt = (
        "Take the following Slovak text and rewrite it by replacing some words with synonyms "
        "or slightly changing the language while keeping the original meaning:\n\n"
        f"{content}\n\n"
        "Provide only the modified text."
    )
    client = OpenAI(
        api_key=api_key,  # This is the default and can be omitted
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
        {
            "role": "user",
            "content": prompt,
        },
    ],
    )
    return response.choices[0].message.content


def process_files():
    print("Iterate over files...")
    # Iterate over files in base directory
    for file in base_dir.iterdir():
        if file.is_file() and "alternative" not in file.name and "DS_Store" not in file.name:  # Process only files
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()

            alt_file_path = alt_dir / file.name
            if not os.path.isfile(alt_file_path):
                # Generate alternative text
                try:
                    alternative_text = generate_alternatives(content)
                except Exception as e:
                    print(f"Error processing file {file.name}: {e}")
                    continue

                # Save the alternative content into the 'alternatives' subdirectory

                with open(alt_file_path, 'w', encoding='utf-8') as f:
                    f.write(alternative_text)

    print(f"Alternative files saved in {alt_dir}")

process_files()