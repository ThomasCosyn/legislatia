import chromadb

from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain_core.messages import HumanMessage
from services.embedding_function import OVHEmbeddingFunction
from services.llm import LLM
from services.prompts import RAG_PROMPT
from typing import Type


class QueryToolsInput(BaseModel):
    query: str = Field(description="The natural language query to be used to \
                       search the collection.")


class QueryRenaissanceProgram(BaseTool):
    name = "query_renaissance_program"
    description = "Interroge la collection Chroma DB contenant le programme \
        Renaissance. Renvoie une liste de textes sémantiquement pertinents."
    args_schema: Type[BaseModel] = QueryToolsInput

    def _run(self, query: str) -> list[str]:
        """ Use this Tool to query the Chroma DB
        """
        chroma_client = chromadb.PersistentClient()
        collection = chroma_client.get_collection("le-monde",
                                                  embedding_function=OVHEmbeddingFunction("https://multilingual-e5-base.endpoints.kepler.ai.cloud.ovh.net/api/text2vec"))  # noqa
        query_results = collection.query(query_texts=query,
                                         n_results=2)
        extracts = query_results['documents'][0]
        answer = LLM.invoke(
            [HumanMessage(content=RAG_PROMPT.format(question=query,
                                                    context="\n\n###\n".join(extracts)))]
                            )
        return answer

    async def _arun(self, query: str) -> list[str]:
        """ Use this Tool to query the Chroma DB
        """
        raise NotImplementedError("This tool is not async yet.")
