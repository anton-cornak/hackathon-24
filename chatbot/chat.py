from langchain.schema import Document
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer


class Chat:
    def __init__(
        self,
        qa_model: str,
        # text_gen_model: str,
    ):
        self.qa_model = AutoModelForQuestionAnswering.from_pretrained(qa_model)
        self.qa_tokenizer = AutoTokenizer.from_pretrained(qa_model)
        self.qa_pipeline = pipeline(
            "question-answering", model=self.qa_model, tokenizer=self.qa_tokenizer
        )

        # self.text_gen_tokenizer = AutoTokenizer.from_pretrained(text_gen_model)
        # self.text_gen_pipline = pipeline(
        #     "text-generation", model=text_gen_model, tokenizer=self.qa_tokenizer
        # )

    def qa_answer_question(
        self,
        question: str,
        semantic_search_res: list[tuple[Document, float]],
    ):
        context: str = ""

        for doc, _ in semantic_search_res:
            context += doc.page_content + " "

        qa_result = self.qa_pipeline(question=question, context=context)

        return qa_result["answer"]

    # def text_gen_question(
    #     self,
    #     question: str,
    #     semantic_search_res: list[tuple[Document, float]],
    # ):

    #     context: str = semantic_search_res[0][0].page_content

    #     prompt = f"Question: {question} Context: {context} Answer the question in one or two concise sentences:"

    #     text_gen_result = self.text_gen_pipline(prompt, max_length=300, truncation=True)

    #     return text_gen_result
