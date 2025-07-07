from abc import ABC, abstractmethod
import hashlib
import json
import numpy as np
import pandas as pd
import redis
from redis.commands.search.field import (
    TextField,
    VectorField,
)
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from models.document import Document

VECTOR_DIMENSION = 1536


class VectorDbCache(ABC):
    """
    Abstract base class for a vector database cache.

    This class defines the interface for caching and retrieving documents based on vector similarity.

    Methods
    -------
    find_similar(vector: list[float], k=10) -> list[Document]
        Asynchronously finds and returns up to `k` documents most similar to the given vector.

    write(documents: list[Document])
        Asynchronously writes a list of documents to the cache.
    """
    @abstractmethod
    async def find_similar(self, vector: list[float], k=10) -> list[Document]:
        pass

    @abstractmethod
    async def write(self, documents: list[Document]):
        pass


SHA256 = hashlib.sha256()


class RedisVectorCache(VectorDbCache):
    _pool = None

    def __init__(self, host, port) -> None:
        """
        Initializes a RedisVectorCache instance with a connection to a Redis server.

        If a connection pool does not already exist, it creates one using the provided host and port.
        Subsequent instances will reuse the same connection pool.

        Args:
            host (str): The hostname or IP address of the Redis server.
            port (int): The port number on which the Redis server is listening.
        """
        if RedisVectorCache._pool is None:
            RedisVectorCache._pool = redis.ConnectionPool(host=host, port=port)

        self.client = redis.Redis(
            connection_pool=RedisVectorCache._pool, decode_responses=True
        )

    async def find_similar(self, vector: list[float], k=10) -> list[Document]:
        """
        Asynchronously finds and returns the top-k most similar documents to a given vector.

        Args:
            vector (list[float]): The query vector to compare against stored document vectors.
            k (int, optional): The number of most similar documents to retrieve. Defaults to 10.

        Returns:
            list[Document]: A list of Document objects representing the most similar documents,
                            each with associated URL, text, vector, and similarity score.

        Note:
            - The similarity score is computed as 1 minus the vector score returned by the search.
            - Utilizes a Redis search index ("idx:chunks_vss") with KNN vector search.
        """
        chunks = (
            self.client.ft("idx:chunks_vss")
            .search(
                Query(f"(*)=>[KNN {k} @vector $query_vector AS vector_score]")
                .sort_by("vector_score")
                .return_fields("vector_score", "text", "url", "vector")
                .dialect(2),
                {"query_vector": np.array(vector, dtype=np.float32).tobytes()},
            )
            .docs  # type: ignore
        )
        documents = map(
            lambda doc: Document(
                url=doc.url,
                text=doc.text,
                vector=json.loads(doc.vector),
                similarity=1 - float(doc.vector_score),
            ),
            chunks,
        )

        return list(documents)

    async def get_insertables(self, documents: list[Document]) -> list[Document]:
        """
        Filters and returns documents that are not already present in the cache or are not sufficiently similar to existing documents.

        Args:
            documents (list[Document]): A list of Document objects to be checked for insertion.

        Returns:
            list[Document]: A list of Document objects that are considered insertable (i.e., not found in the cache or not similar enough to existing documents).

        Notes:
            - A document is considered similar if the similarity score with an existing document is greater than or equal to 0.97.
            - The method uses the `find_similar` coroutine to check for similar documents based on the document's vector.
        """
        insertables = []
        for document in documents:
            results = await self.find_similar(document.vector, k=1)
            if not results:
                insertables.append(document)
            elif results[0].similarity < 0.97:
                insertables.append(document)
        return insertables

    async def write(self, documents: list[Document]):
        """
            Writes documents to the cache after filtering out similar or existing documents.
        
            Args:
                documents (list[Document]): A list of Document objects to be written to the cache.
        
            Notes:
                - Uses get_insertables to filter out documents that are already in the cache or too similar.
                - Generates a unique chunk_id using SHA256 hash of the document text.
                - Sets each document's similarity to -1 before storing.
                - Stores documents in Redis with an expiration of 1 hour (3600 seconds).
            """
        documents = await self.get_insertables(documents)
        pipeline = self.client.pipeline()
        for document in documents:
            SHA256.update(document.text.encode("utf-8"))
            chunk_id = SHA256.hexdigest()
            redis_key = f"chunks:{chunk_id}"
            document.similarity = -1
            pipeline.json().set(redis_key, "$", document.model_dump())
            pipeline.expire(redis_key, 3600)

        pipeline.execute()

    def init_test(self):
        """
        Initializes the test environment by loading mock data from a pickle file, processing the data,
        and storing it in Redis using a pipeline.

        The method performs the following steps:
        1. Loads a DataFrame from a pickle file located at "mocks/database_pickle".
        2. Converts the 'vector' column in the DataFrame to a list format.
        3. Converts the DataFrame into a list of dictionaries (records).
        4. For each record, computes a SHA256 hash of the 'text' field to use as a unique identifier.
        5. Stores each record in Redis as a JSON object using the computed hash as part of the key.
        6. Executes the Redis pipeline to batch the operations.

        Assumes that `self.client` is a Redis client instance and `SHA256` is a hashlib.sha256 object.
        """
        df = pd.read_pickle("mocks/database_pickle")
        df["vector"] = df["vector"].apply(lambda x: x.tolist()[0])
        chunks = df.to_dict("records")

        pipeline = self.client.pipeline()
        for chunk in chunks:
            SHA256.update(chunk["text"].encode("utf-8"))
            chunk_id = SHA256.hexdigest()
            redis_key = f"chunks:{chunk_id}"
            pipeline.json().set(redis_key, "$", chunk)
        pipeline.execute()

    def init_index(self, vector_dimension):
        """
        The `init_index` function creates a search index for text, URL, and vector fields with specified
        dimensions and settings.
        
        :param vector_dimension: The `vector_dimension` parameter in the `init_index` method represents the
        dimensionality of the vector field that will be created in the index. This parameter specifies the
        number of components or features in the vector field. It is used to define the size of the vector
        space in which the vectors will be
        """
        schema = (
            TextField("$.text", no_stem=True, as_name="text"),
            TextField("$.url", no_stem=True, as_name="url"),
            VectorField(
                "$.vector",
                "FLAT",
                {
                    "TYPE": "FLOAT32",
                    "DIM": vector_dimension,
                    "DISTANCE_METRIC": "COSINE",
                },
                as_name="vector",
            ),
        )
        definition = IndexDefinition(prefix=["chunks:"], index_type=IndexType.JSON)
        self.client.ft("idx:chunks_vss").create_index(
            fields=schema, definition=definition
        )
