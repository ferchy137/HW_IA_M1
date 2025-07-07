from abc import ABC, abstractmethod
import json
import aiohttp

import openai


class Embeddings(ABC):
    """Abstraction of embeddings client."""

    """
        Asynchronously generate embeddings for a list of text chunks.
    
        This abstract method must be implemented by subclasses to provide a concrete
        embedding generation strategy for a given text input.
    
        Args:
            chunks (list[str]): A list of text strings to be converted into embedding vectors.
    
        Returns:
            list[list[float]]: A list of embedding vectors corresponding to the input text chunks.
        """
    @abstractmethod
    async def run(self, chunks: list[str]) -> list[list[float]]:
        pass


class RemoteEmbeddings(Embeddings):
    """
    RemoteEmbeddings is a subclass of Embeddings that provides an asynchronous interface to a remote embeddings service.

    Attributes:
        vector_dimension (int): The dimensionality of the embedding vectors returned by the service.

    Methods:
        async run(chunks: list[str]) -> list[list[float]]:
            Sends a list of text chunks to a remote embeddings service via HTTP POST request and returns their embeddings.
            Args:
                chunks (list[str]): A list of text strings to be encoded.
            Returns:
                list[list[float]]: A list of embedding vectors corresponding to the input text chunks.
            Raises:
                Returns a list containing an empty list if the request fails or the response status is not 200.
    """
    """Instanciates a client that implements _embeddings service."""

    vector_dimension = 384

    async def run(self, chunks: list[str]) -> list[list[float]]:
        url = f"http://embeddings/encode"
        headers = {"Content-Type": "application/json"}
        payload = json.dumps({"text": chunks})
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, headers=headers) as response:
                if response.status == 200:
                    r = await response.json()
                    return r["embedding"]
        return [[]]


class OpenAIEmbeddings(Embeddings):
    """
    OpenAIEmbeddings is a wrapper class for generating vector embeddings using OpenAI's embedding models.

    Attributes:
        vector_dimension (int): The dimensionality of the embedding vectors produced by the model.

    Methods:
        run(chunks: list[str], model: str = "text-embedding-ada-002") -> list[list[float]]:
            Asynchronously generates embeddings for a list of text chunks using the specified OpenAI embedding model.

            Args:
                chunks (list[str]): A list of text strings to be embedded.
                model (str, optional): The OpenAI embedding model to use. Defaults to "text-embedding-ada-002".

            Returns:
                list[list[float]]: A list of embedding vectors, one for each input chunk.
    """
    """OpenAI embeddings client wrapper"""

    vector_dimension = 1536

    async def run(
        self, chunks: list[str], model="text-embedding-ada-002"
    ) -> list[list[float]]:
        response = await openai.Embedding.acreate(input=chunks, model=model)
        vectors = map(lambda x: x["embedding"], response["data"])  # type: ignore
        return list(vectors)
