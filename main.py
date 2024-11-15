import logging

from chatbot.chat import Chat
from chatbot.llama import llama_answer_question
from embeddings.prepare_data import Preprocess
from embeddings.semantic_search import SemanticSearch

logging.basicConfig(level=logging.ERROR)


def chat():

    embeddings_model = "paraphrase-multilingual-MiniLM-L12-v2"

    preprocess = Preprocess(
        data_path="data",
        db_path="chroma",
        embeddings_model=embeddings_model,
    )

    preprocess.prepare_data()

    semantic_search = SemanticSearch(
        embeddings_model=embeddings_model,
        chroma=preprocess.chroma,
    )

    chatbot = Chat(
        qa_model="distilbert-base-uncased-distilled-squad",
        # text_gen_model="facebook/bart-large",
    )

    print("Hello, I'm you annotation helper. What can I do for you?")

    while True:
        user_input = input("You: ")
        if user_input == "bye":
            print("Goodbye!")
            break
        else:
            results = semantic_search.search(user_input, top_k=3)
            qa_res = chatbot.qa_answer_question(user_input, results)
            # text_gen_res = chatbot.text_gen_question(user_input, results)
            print(f"QA Bot: {qa_res}")
            # print(f"Text Gen Bot: {text_gen_res}")
            llama_res = llama_answer_question(user_input, results)
            print(f"Llama: {llama_res}")


if __name__ == "__main__":
    chat()
