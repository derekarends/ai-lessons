import asyncio
import os
import dotenv

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior,
)
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.kernel import Kernel

from plugins.hours_plugin import HoursPlugin
from plugins.menu_plugin import MenuPlugin

NAME = "Jeeves"
INSTRUCTIONS = "Use the plugins available to answer the users question."


async def invoke_agent(agent: ChatCompletionAgent, input: str, chat: ChatHistory):
    chat.add_user_message(input)

    async for content in agent.invoke(chat):
        print(f"{content.name or '*'}: '{content.content}'")
        chat.add_message(content)


async def main():
    kernel = Kernel()
    kernel.add_service(
        AzureChatCompletion(
            service_id="agent",
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        )
    )

    execution_settings = kernel.get_prompt_execution_settings_from_service_id(service_id="agent")
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    kernel.add_plugin(plugin=HoursPlugin(), plugin_name="hours")
    kernel.add_plugin(plugin=MenuPlugin(), plugin_name="menu")

    agent = ChatCompletionAgent(
        service_id="agent",
        kernel=kernel,
        name=NAME,
        instructions=INSTRUCTIONS,
        execution_settings=execution_settings,
    )

    chat = ChatHistory()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        await invoke_agent(agent, user_input, chat)


if __name__ == "__main__":
    dotenv.load_dotenv()
    asyncio.run(main())
