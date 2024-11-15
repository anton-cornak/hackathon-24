from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


class SemanticSearch:
    def __init__(self, embeddings_model: str, chroma: Chroma):
        self.embeddings_model = HuggingFaceEmbeddings(model_name=embeddings_model)
        self.chroma = chroma

    def search(self, query: str, top_k: int = 5) -> list[tuple[Document, float]]:
        results = self.chroma.similarity_search_with_score(query, k=top_k)

        return results
