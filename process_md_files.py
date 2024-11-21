import logging
import os
from datetime import datetime

import openai

from private_config import API_KEY

logging.basicConfig(level=logging.INFO)

# Set your OpenAI API key
openai.api_key = API_KEY


def process_md_files(folder_path):
    """
    Opens all `.md` files in the specified folder, rephrases their content using GPT,
    appends the rephrased content to the end of each file, and saves the changes.

    Args:
        folder_path (str): Path to the folder containing `.md` files.
    """
    start_time = datetime.now()
    logging.info(f"Processing started at: {start_time}")
    # Get a list of all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file has a `.md` extension
        if filename.endswith(".md"):
            file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}_alternative.md")


            # Open and read the file's content
            with open(file_path, "r", encoding="utf-8") as file:
                original_content = file.read()

            # Rephrase the content using GPT
            logging.info(f"Processing file: {filename}")
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",  # Specify the GPT model (e.g., "gpt-4" for more advanced capabilities)
                    messages=[
                        {"role": "system", "content": "You are an assistant that rephrases text using synonyms. Text must be in Slovak language"},
                        {"role": "user", "content": f"Rephrase the following text:\n{original_content}"}
                    ],
                    temperature=0.7,  # Adjust the creativity of the output
                )
                # Extract the rephrased content from the response
                paraphrased_content = response['choices'][0]['message']['content']
            except openai.error.OpenAIError as e:
                # Handle API errors gracefully and continue with other files
                logging.error(f"Error processing file {filename}: {e}")
                continue

            # Append the rephrased content to the end of the file
            with open(new_file_path, "a", encoding="utf-8") as file:
                file.write("\n\n---\n\n")  # Separator between original and rephrased content
                file.write(paraphrased_content)

            logging.info(f"File {filename} successfully updated.")
    end_time = datetime.now()
    logging.info(f"Processing finished at: {end_time}")
    logging.info(f"Processing completed in: {end_time - start_time}")


if __name__ == '__main__':
    process_md_files("./data")
