import asyncio
import os
import dotenv

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.kernel import Kernel

from plugins.hours_plugin import HoursPlugin
from plugins.menu_plugin import MenuPlugin

NAME = "Jeeves"
INSTRUCTIONS = "Using the tools available answer the users question."


async def invoke_agent(agent: ChatCompletionAgent, input: str, chat: ChatHistory):
    chat.add_user_message(input)

    print(f"# {AuthorRole.USER}: '{input}'")

    async for content in agent.invoke(chat):
        print(f"# {content.role} - {content.name or '*'}: '{content.content}'")
        chat.add_message(content)


async def main():
    kernel = Kernel(
        services=[
            AzureChatCompletion(
              service_id='agent',
              deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
              api_key=os.getenv("AZURE_OPENAI_API_KEY"),
              endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
          )
        ]
    )
    kernel.add_plugin(plugin=HoursPlugin(), plugin_name="hours")
    kernel.add_plugin(plugin=MenuPlugin(), plugin_name="menu")

    agent = ChatCompletionAgent(service_id="agent", kernel=kernel, name=NAME, instructions=INSTRUCTIONS)

    chat = ChatHistory()

    await invoke_agent(agent, "What time does your store open on Friday?", chat)
    await invoke_agent(agent, "What are the specials on the menu?", chat)


if __name__ == "__main__":
    dotenv.load_dotenv()
    asyncio.run(main())