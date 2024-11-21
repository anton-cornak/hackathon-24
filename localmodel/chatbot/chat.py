from langchain.schema import Document
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer


class Chat:
    def __init__(
        self,
        qa_model: str,
    ):
        self.qa_model = AutoModelForQuestionAnswering.from_pretrained(qa_model)
        self.qa_tokenizer = AutoTokenizer.from_pretrained(qa_model)
        self.qa_pipeline = pipeline(
            "question-answering", model=self.qa_model, tokenizer=self.qa_tokenizer
        )

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