import os
import requests

from chromadb.api.types import Documents, EmbeddingFunction, Embeddings


class OVHEmbeddingFunction(EmbeddingFunction[Documents]):
    def __init__(self, api_url: str):
        """Initialize the embedding function."""
        self.api_url = api_url
        self.headers = {
            "Content-Type": "text/plain",
            "Authorization": (
                f"Bearer {os.getenv('OVH_AI_ENDPOINTS_ACCESS_TOKEN')}"
            ),
        }

    def __call__(self, input: Documents) -> Embeddings:
        """Embed the input documents."""
        response_data = []
        embeddings = []
        for doc in input:
            response = requests.post(self.api_url,
                                     data=doc,
                                     headers=self.headers)
            if response.status_code == 200:
                response_data.append(response.json())
                embeddings.append(response_data[-1])
            else:
                print(f"Error for document '{doc}': {response.status_code}")
                embeddings.append(None)  # Handle error case
        return embeddings
