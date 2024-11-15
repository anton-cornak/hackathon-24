import os

import logging

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_chroma import Chroma

from langchain_huggingface import HuggingFaceEmbeddings


class Preprocess:
    def __init__(
        self,
        data_path: str,
        db_path: str,
        embeddings_model: str,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):
        self.db_path = db_path
        self.embeddings_model = HuggingFaceEmbeddings(model_name=embeddings_model)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.loader = DirectoryLoader(data_path, glob="*.md")

        self.logger = logging.getLogger(__name__)
        self.documents: list[Document] = []
        self.chunks: list[Document] = []
        self.chroma: Chroma = None

    def _load_documents(self):
        try:
            self.logger.info("Loading documents...")

            self.documents = self.loader.load()
        except Exception as e:
            self.logger.error(f"Error loading documents: {e}")

    def _create_chunks(self):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            add_start_index=True,
        )

        self.chunks = text_splitter.split_documents(self.documents)

        print(f"Created {len(self.chunks)} chunks")

    def prepare_data(self) -> Chroma:
        if os.path.exists(self.db_path):
            self.chroma = Chroma(
                persist_directory=self.db_path,
                embedding_function=self.embeddings_model,
            )
        else:
            self._load_documents()
            self._create_chunks()
            self.chroma = Chroma.from_documents(
                self.chunks,
                self.embeddings_model,
                persist_directory=self.db_path,
            )

        return self.chroma
