import semantic_kernel as sk
from dotenv import dotenv_values
from semantic_kernel.connectors.ai.open_ai import (
    OpenAITextCompletion,
    AzureTextCompletion,
    OpenAIChatCompletion,
    AzureChatCompletion,
)
from semantic_kernel.kernel import Kernel
import os


def add_completion_service(self):
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env.example")
    config = dotenv_values(dotenv_path)
    

    # config = dotenv_values(".env.example")
    llm_service = config.get("GLOBAL__LLM_SERVICE", None)
    deployment_name = config.get("OPENAI_DEPLOYMENT_NAME", None)
    base_url = config.get("Base_url", None)
    api_version = config.get("API_version", None)   
    api_key = config.get("OPENAI_API_KEY", None)   

    # Configure AI service used by the kernel. Load settings from the .env file.
    # if llm_service == "AzureOpenAI":
    deployment_type = config.get("AZURE_OPEN_AI__DEPLOYMENT_TYPE", None)
    # print(llm_service,deployment_name,base_url,api_version)

    if deployment_type == "chat-completion":
        self.add_chat_service(
            "azure_gpt35_chat_completion",
            AzureChatCompletion(
        deployment_name=deployment_name,
        base_url=base_url,
        api_version=api_version,
        api_key=api_key,),
        )
    
    else:
        self.add_text_completion_service(
            "text_completion",
            AzureTextCompletion(
                config.get("AZURE_OPEN_AI__TEXT_COMPLETION_DEPLOYMENT_NAME", None),
                config.get("AZURE_OPEN_AI__ENDPOINT", None),
                config.get("AZURE_OPEN_AI__API_KEY", None),
            ),
        )    

Kernel.add_completion_service = add_completion_service

