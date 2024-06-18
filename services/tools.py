import chromadb

from services.embedding_function import OVHEmbeddingFunction
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type


class QueryToolsInput(BaseModel):
    query: str = Field(description="The natural language query to be used to \
                       search the collection.")


class QueryRenaissanceProgram(BaseTool):
    name = "query_renaissance_program"
    description = "Query the Chroma DB collection containing the Renaissance \
        program. Returns a list of texts semantically relevant."
    args_schema: Type[BaseModel] = QueryToolsInput

    def _run(self, query: str) -> list[str]:
        """ Use this Tool to query the Chroma DB
        """
        chroma_client = chromadb.PersistentClient()
        collection = chroma_client.get_collection("le-monde",
                                                  embedding_function=OVHEmbeddingFunction("https://multilingual-e5-base.endpoints.kepler.ai.cloud.ovh.net/api/text2vec"))  # noqa
        results = collection.query(query_texts=query,
                                   n_results=2)
        return results['documents'][0]

    async def _arun(self, query: str) -> list[str]:
        """ Use this Tool to query the Chroma DB
        """
        raise NotImplementedError("This tool is not async yet.")
