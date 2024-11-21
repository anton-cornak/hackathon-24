from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document

PROMPT_TEMPLATE = """
Answer the following question:

{question}

only using the following context:

{context}
"""


def llama_answer_question(
    question: str, semantic_search_res: list[tuple[Document, float]]
) -> str:
    context = "\n\n----\n\n".join([doc.page_content for doc, _ in semantic_search_res])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(question=question, context=context)

    model = OllamaLLM(model="llama3.1")
    response = model.invoke(prompt)

    return response