from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings


class ChromaDB:
    def __init__(
        self,
        chroma_path: str,
        embeddings: HuggingFaceEmbeddings,
        chunks: list[Document] = None,
        from_documents: bool = False,
    ) -> None:
        """
        Initialize the ChromaDB object.

        Args:
            chroma_path (str): The directory where the ChromaDB is stored.
            embeddings (HuggingFaceEmbeddings): The Hugging Face embeddings model.
            chunks (list[Document]): A list of Document objects.
            from_documents (bool): Whether to create the ChromaDB from documents or embeddings.
        """
        self.chroma_path: str = chroma_path
        self.chunks: list[Document] = chunks
        self.embeddings: HuggingFaceEmbeddings = embeddings
        self.from_documents: bool = from_documents
        self.chroma: Chroma

    def _init_from_documents(self) -> None:
        """
        Initialize a new Chroma object.
        """
        self.chroma = Chroma.from_documents(
            self.chunks,
            self.embeddings,
            persist_directory=self.chroma_path,
        )

    def _init_from_embeddings(self) -> None:
        """
        Initialize a new Chroma object from previously created embeddings.
        """
        self.chroma = Chroma(
            persist_directory=self.chroma_path,
            embedding_function=self.embeddings,
        )

    def create_chroma_db(self) -> Chroma:
        """
        Create a ChromaDB object.
        """

        if self.from_documents:
            self._init_from_documents()
        else:
            self._init_from_embeddings()

        return self.chroma