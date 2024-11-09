import asyncio
import os
import dotenv

from typing import Dict, Optional
from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent
from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior,
)
from semantic_kernel.agents.strategies.termination.termination_strategy import (
    TerminationStrategy,
)
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import (
    AzureChatCompletion,
)
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.kernel import Kernel

from plugins.legal_plugin import LegalPlugin


class ApprovalTerminationStrategy(TerminationStrategy):
    """A strategy for determining when an agent should terminate."""

    async def should_agent_terminate(self, agent, history):
        """Check if the agent should terminate."""
        return "approved" in history[-1].content.lower()


REVIEWER_NAME = "ArtDirector"
REVIEWER_INSTRUCTIONS = """
You are an art director who has opinions about copywriting born of a love for David Ogilvy.
The goal is to determine if the given copy is acceptable to print.
You must make sure the copy is legally sound before approving.
If it is not legal be very clear on why it is not, and how to fix it.
If so, state that it is approved.
If not, provide insight on how to refine suggested copy without example.
"""

COPYWRITER_NAME = "CopyWriter"
COPYWRITER_INSTRUCTIONS = """
You are a copywriter with ten years of experience and are known for brevity and a dry humor.
The goal is to refine and decide on the single best copy as an expert in the field.
Only provide a single proposal per response.
You're laser focused on the goal at hand.
Don't waste time with chit chat.
Consider suggestions when refining an idea.
"""


def _create_chat_completion_agent(
    service_id: str, name: str, instructions: str, plugins: Dict[str, object]
) -> ChatCompletionAgent:
    kernel = Kernel()
    kernel.add_service(
        AzureChatCompletion(
            service_id=service_id,
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        )
    )
    execution_settings = kernel.get_prompt_execution_settings_from_service_id(service_id=service_id)
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    [
        kernel.add_plugin(plugin=plugin, plugin_name=plugin_name)
        for plugin_name, plugin in plugins.items()
    ]
    return ChatCompletionAgent(
        service_id=service_id,
        kernel=kernel,
        name=name,
        instructions=instructions,
        execution_settings=execution_settings,
    )


async def main():
    agent_reviewer = _create_chat_completion_agent(
        "artdirector", REVIEWER_NAME, REVIEWER_INSTRUCTIONS, {"legal": LegalPlugin()}
    )

    agent_writer = _create_chat_completion_agent(
        "copywriter", COPYWRITER_NAME, COPYWRITER_INSTRUCTIONS, {}
    )

    chat = AgentGroupChat(
        agents=[agent_writer, agent_reviewer],
        termination_strategy=ApprovalTerminationStrategy(
            agents=[agent_reviewer], maximum_iterations=10
        ),
    )

    user_input: Optional[str] = None
    while True:
        user_input = input("You: ")
        if user_input:
            break

    await chat.add_chat_message(ChatMessageContent(role=AuthorRole.USER, content=user_input))

    async for content in chat.invoke():
        print(f"{content.name or '*'}: '{content.content}'")


if __name__ == "__main__":
    dotenv.load_dotenv()
    asyncio.run(main())
