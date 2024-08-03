from typing import List, Union
import os
import discord


from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_upstage import ChatUpstage


API_KEY = os.getenv("UPSTAGE_API_KEY")
SYSTEM_PROMPT = """
Conversation follow the format '@username: message'. You should return name formed in @username.
"""


def _get_solar_response(
    input_text: str,
    chat_history: List[Union[HumanMessage, AIMessage]],
) -> str:
    llm = ChatUpstage(api_key=API_KEY)
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history"),
            ("human", input_text),
        ]
    )
    chain = qa_prompt | llm | StrOutputParser()
    answer_text = chain.invoke(
        {
            "question": input_text,
            "chat_history": chat_history,
        },
    )
    return answer_text


class Solar(discord.ui.View):
    def __init__(self):
        pass

    def description(self):
        return "Solar"

    async def execute(self, interaction: discord.Interaction, input_text: str):
        await interaction.response.defer(thinking=True)
        _conversations = [_message async for _message in interaction.channel.history()]
        _refined_conversations = [
            HumanMessage(f"@{_conversation.author}:{_conversation.content}")
            if _conversation.application_id is None
            else AIMessage(f"@{_conversation.author}:{_conversation.content}")
            async for _conversation in _conversations
        ]
        _message = _get_solar_response(
            input_text=input_text, chat_history=_refined_conversations
        )
        await interaction.followup.send(_message)
