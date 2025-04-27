import os
from autogen_ext.models.openai import OpenAIChatCompletionClient, AzureOpenAIChatCompletionClient
from dotenv import load_dotenv
from typing import Union # Import Union for type hinting

load_dotenv() # Load environment variables from .env file

# API_HOST = os.getenv("API_HOST", "azure")

def ConfigLlm(API_HOST:str = "azure") -> Union[OpenAIChatCompletionClient, AzureOpenAIChatCompletionClient]:
    """Initializes and returns an LLM client based on the global API_HOST environment variable.

    Supports 'github', 'azure', and 'openai' hosts. Reads credentials from environment variables.

    Returns:
        An initialized LLM client (OpenAIChatCompletionClient or AzureOpenAIChatCompletionClient).

    Raises:
        KeyError: If required environment variables are missing.
        ValueError: If API_HOST is not one of the supported values.
    """
    client = None # Initialize client to None
    if API_HOST == "github":
        client = OpenAIChatCompletionClient(
            model=os.getenv("GITHUB_MODEL", "gpt-4o"),
            api_key=os.environ["GITHUB_TOKEN"],
            base_url="https://models.inference.ai.azure.com"
        )
    elif API_HOST == "azure":
        client = AzureOpenAIChatCompletionClient(
            azure_deployment=os.getenv("CHATBOT_UI_AZURE_DEPLOYMENT_NAME"),
            model=os.getenv("CHATBOT_UI_AZURE_DEPLOYMENT_NAME"), # Often the same as deployment name
            api_version=os.getenv("CHATBOT_UI_AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("CHATBOT_UI_AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("CHATBOT_UI_AZURE_OPENAI_KEY")
        )
    elif API_HOST == "openai":
        client = OpenAIChatCompletionClient(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            api_key=os.environ["OPENAI_API_KEY"],
            base_url="https://api.openai.com/v1"
        )
    else:
        raise ValueError(f"Unsupported API_HOST: {API_HOST}. Must be 'github', 'azure', or 'openai'.")

    if client is None:
        raise ValueError(f"Client could not be initialized for API_HOST: {API_HOST}")

    return client