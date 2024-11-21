from chatbot.chat import Chat
from embeddings.prepare_data import Preprocess
from embeddings.semantic_search import SemanticSearch
import openai
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

    openai.api_key = ""

    language = "Slovak"
    messages = [{"role": "system", "content": f"You are an assistant providing helpful answers in {language} language."}]
    

    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            print("Chatbot: Bye!")
            break
        else:
            results = semantic_search.search(user_input, top_k=3)
            contexts = [doc.page_content for doc, _ in results]
            context = " ".join(contexts)

            messages.append({"role": "system", "content": f"Relevant context: {context}"})
            messages.append({"role": "user", "content": user_input})

            try:
                response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=messages,
                    temperature=0.5,
                )

                qa_res = response.choices[0].message.content.strip()
                print(f"QA Bot: {qa_res}")
                messages.append({"role": "assistant", "content": qa_res})

            except openai.error.OpenAIError as e:
                print(f"Error in generating response: {e}")

            # print("***************")
            # print(messages)
            # print("***************")

if __name__ == "__main__":
    chat()