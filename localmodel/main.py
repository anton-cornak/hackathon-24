from chatbot.chat import Chat
# from chatbot.llama import llama_answer_question
from embeddings.prepare_data import Preprocess
from embeddings.semantic_search import SemanticSearch

def chat():
    print("Initializing...")
    
    data_path = "../data"
    db_path = "data.db"
    embeddings_model = "paraphrase-multilingual-MiniLM-L12-v2"

    preprocess = Preprocess(
        data_path,
        db_path,
        embeddings_model,
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

    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            print("Chatbot: Bye!")
            break
        else:
            results = semantic_search.search(user_input, top_k=3)
            qa_res = chatbot.qa_answer_question(user_input, results)
            print(f"QA Bot: {qa_res}")
            # llama_res = llama_answer_question(user_input, results)
            # print(f"Llama: {llama_res}")

if __name__ == "__main__":
    chat()
