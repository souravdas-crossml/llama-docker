"""
This module provides a document loader class that loads documents from a directory, splits them into chunks of text, 
creates embeddings using a specified model, and stores the embeddings in a vector store.

Dependencies:
- langchain.embeddings: Provides the HuggingFaceEmbeddings class for creating embeddings.
- langchain.vectorstores: Provides the FAISS class for creating the vector store.
- langchain.text_splitter: Provides the CharacterTextSplitter class for splitting text into chunks.
- langchain.document_loaders: Provides the DirectoryLoader class for loading documents from a directory.
- typing.List: Used for type hinting the return value of the load_and_split_text function.

Usage:
1. Instantiate the document_loader class with the required parameters.
2. Call the create_vectorstore method to load and split the documents, create embeddings, and store them in a vector store.
"""

# Import Dependencies
from typing import List

from langchain.document_loaders import (
        DirectoryLoader, 
        CSVLoader, 
        PyPDFLoader,
        BSHTMLLoader,
        JSONLoader,
        TextLoader
    )
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS


class document_loader:
    """
    This class provides functionality to load documents, split them into chunks, 
    create embeddings, and store them in a vector store.
    """
    def __init__(self,
                 directory_path: str, 
                 load_type: str,
                 file_type: str,
                 model_name: str,
                 model_kwargs: dict,
                 vectorDB_directory: str,
                 chunk_size: int = None)-> None:
        """
        Initializes the document_loader object with the specified parameters.

        Args:
            directory_path (str): Path to the directory containing the documents.
            chunk_size (int): Size of the document chunks to be processed.
            load_type (str): Type of documents to be loaded (CSV, PDF, HTML, File Directory)).
            file_type (str): Type of file to be loaded for file directory.
            model_name (str): Name of the embedding model to be used.
            model_kwargs (dict): Keyword arguments for the embedding model.
            vectorDB_directory (str): Directory path for storing the vector store.
        """
        self._document_path = directory_path
        self._chunk_size = 1000 if chunk_size is None or chunk_size == 0 else chunk_size
        self._load_type = load_type
        self._file_type = file_type
        self.model_name = model_name
        self.model_kwargs = model_kwargs
        self.vectorDB_directory = vectorDB_directory
    
    @staticmethod
    def create_embedding(model_name, model_kwargs):
        """
        Creates embeddings using specified model and model_kwargs (parameters)

        Args:
            model_name (str): model used to create embeddings
            model_kwargs (dict): model parameters used

        Returns:
            _type_: embeddings created by the specified model (mathematical representation of text data)
        """
        _embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)
        return _embeddings
    
    def load_document(self)-> any:
        """
        Loads the documents from different sources like pdf, txt files, file directories, json, html, etc.

        Returns:
            any: object for loaded document.
        """
        try:
            if self._load_type == "csv":
                loader = CSVLoader(file_path=self._document_path)
                data = loader.load()
            if self._load_type == "file_directory":
                if self._file_type not in ["**/*.txt", "**/*.md"]:
                    raise ValueError("only **/*.txt and **/*.md file types are allowed.")
                loader = DirectoryLoader(self._document_path, glob=self.file_type)
                data = loader.load()
            if self._load_type == "pdf":
                loader = PyPDFLoader(self._document_path)
                data = loader.load()
            if self._load_type == "html":
                loader = BSHTMLLoader(self._document_path)
                data = loader.load()
            if self._load_type == "json":
                loader = JSONLoader(
                    file_path=self._document_path,
                    jq_schema='.',
                    text_content=False
                )
                data = loader.load()
            if self._load_type == "text":
                loader = TextLoader(self._document_path)
                data = loader.load()
            else:
                raise ValueError("Invalid load type. Only Load type allowed are json, pdf, file_directory, csv, and html.")
        except Exception as e:
            return str(e)
            
        return data
    def text_spliter(self, document: any) -> List[str]:
        """
        Splits the input document into chunks of text.

        Args:
            document (any): The input document to be split.

        Returns:
            List[str]: A list of strings representing the split text chunks.
        """
        splitter = CharacterTextSplitter(
            chunk_size=self._chunk_size,
            chunk_overlap=0
        )
        texts = splitter.split_documents(document)
        return texts

    
    def create_vectorstore(self, texts:List[str], embeddings:any)-> None:
        """
        Loads and splits the documents, creates embeddings, and stores them in a vector store.
        Vector store used in this instance is FAISS. The vector DB instance is created as 
        pkl file and is persisted.

        Args:
            texts (_type_): text that is to be embedded into the vector store
            embeddings (_type_): model embeddding
        """
        vector_store = FAISS.from_documents(
            documents=texts,
            embedding=embeddings
        )
        vector_store.save_local(self.vectorDB_directory)
    