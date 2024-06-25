import os

from langchain_mistralai import ChatMistralAI


LLM = ChatMistralAI(
        model="mistral-large-latest",
        api_key=os.getenv("MISTRAL_API_KEY"),
        max_retries=6
    )
'''
# model = ChatMistralAI(
#     model="Mixtral-8x22B-Instruct-v0.1",
#     api_key=os.getenv("OVH_AI_ENDPOINTS_ACCESS_TOKEN"),
#     endpoint="https://mixtral-8x22b-instruct-v01.endpoints.kepler.ai.cloud.ovh.net/api/openai_compat/v1",  # noqa
#     max_tokens=1000
# )
# model = AzureChatOpenAI(
#     azure_endpoint="https://neo-conversation-sweden-azopenai-dev.openai.azure.com/",
#     api_key=os.getenv("AZURE_OPENAI_KEY"),
#     azure_deployment="gpt-4o",
#     api_version="2024-05-01-preview"
# )
'''