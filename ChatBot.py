# Copyright (c) Microsoft. All rights reserved.

import asyncio

from dotenv import load_dotenv

import streamlit as st
import numpy as np
import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai
import add_completion_service

load_dotenv()

system_message = """
You are a chat bot. you need to provide the information of the
capital of cities, countries. and a bit summury of that
"""

kernel = sk.Kernel()

# chat_service = sk_oai.AzureChatCompletion(
#     **azure_openai_settings_from_dot_env_as_dict(include_api_version=True)
# )
# kernel.add_chat_service("chat-gpt", chat_service)

kernel.add_completion_service()

prompt_config = sk.PromptTemplateConfig.from_completion_parameters(
    max_tokens=2000, temperature=0.7, top_p=0.8
)

prompt_template = sk.ChatPromptTemplate(
    "{{$user_input}}", kernel.prompt_template_engine, prompt_config
)

prompt_template.add_system_message(system_message)
prompt_template.add_user_message("Hi there, who are you?")
prompt_template.add_assistant_message(
    "I am Mosscap, a chat bot. I'm trying to figure out what people need."
)

function_config = sk.SemanticFunctionConfig(prompt_config, prompt_template)
chat_function = kernel.register_semantic_function("ChatBot", "Chat", function_config)



async def chat(user_input) -> str:
    context_vars = sk.ContextVariables()
    context_vars["user_input"] = user_input

    answer = kernel.run_stream_async(chat_function, input_vars=context_vars)
    full_message = ""
    async for message in answer:
        full_message += message

    return full_message


# async def main() -> None:
#     chatting = True
#     while chatting:
#         chatting = await chat()


# if __name__ == "__main__":
#     asyncio.run(main())


def main():
    st.title("Chat with chatbot ")

    # user_input = st.text_input("User:", "")
    user_input = st.chat_input("type here")
    # chat_history = []
    chat_history = ""
    # user=st.chat_message("user")
    if user_input:
        
            response = asyncio.run(chat(user_input))
            with st.chat_message("user"):
                st.write(user_input)
                # chat_history_user += f"\nUser: {user_input}"
            with st.chat_message("Assistant"):
                 st.write(response)
                # chat_history_mos+= f"\nMosscap: {response}\n"
            # st.text_area(":", chat_history, height=200)


if __name__ == "__main__":
    main()
