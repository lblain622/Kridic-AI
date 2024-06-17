
from langchain_nvidia_ai_endpoints import ChatNVIDIA

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import re
from pathlib import Path
from typing import Callable, Union

from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from tools import *


key = "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"
from tempfile import TemporaryDirectory

from langchain_community.agent_toolkits import FileManagementToolkit

def _is_valid_identifier(value: str) -> bool:
    """Check if the session ID is in a valid format."""
    # Use a regular expression to match the allowed characters
    valid_characters = re.compile(r"^[a-zA-Z0-9-_]+$")
    return bool(valid_characters.match(value))

def create_session_factory(
    base_dir: Union[str, Path],
) -> Callable[[str], BaseChatMessageHistory]:
    """Create a session ID factory that creates session IDs from a base dir.

    Args:
        base_dir: Base directory to use for storing the chat histories.

    Returns:
        A session ID factory that creates session IDs from a base path.
    """
    base_dir_ = Path(base_dir) if isinstance(base_dir, str) else base_dir
    if not base_dir_.exists():
        base_dir_.mkdir(parents=True)

    def get_chat_history(session_id: str) -> FileChatMessageHistory:
        """Get a chat history from a session ID."""
        if not _is_valid_identifier(session_id):
            raise HTTPException(
                status_code=400,
                detail=f"Session ID `{session_id}` is not in a valid format. "
                "Session ID must only contain alphanumeric characters, "
                "hyphens, and underscores.",
            )
        file_path = base_dir_ / f"{session_id}.json"
        return FileChatMessageHistory(str(file_path))

    return get_chat_history



chat_prompts = ChatPromptTemplate.from_messages( [
        ("system", "You are a helpful Menu Analyzer AI bot that categorizes menu items with tags of possible allergens and ingrediants. You also can answer questions about the given food items or about food in general,based upon what the human asks. Your name is Kridic."),
        ("human","{human_input}"),

        MessagesPlaceholder(variable_name="history"),
    ])


chatter = ChatNVIDIA(model="meta/llama3-8b-instruct",
                     api_key=key,
                     base_url="https://integrate.api.nvidia.com/v1")

#embedder = NVIDIAEmbeddings(model="snowflake/arctic-embed-l")
working_directory = TemporaryDirectory()
tools = FileManagementToolkit(
    root_dir=str(working_directory.name),
    selected_tools=["read_file", "list_directory"],
).get_tools()


tools.append(extract_menu_info)

#chatter.bind_tools([extract_menu_info])


chain = chat_prompts |chatter | StrOutputParser()
chain_with_history = RunnableWithMessageHistory(
    chain,
    create_session_factory("chat_histories"),
    input_messages_key="human_input",
    history_messages_key="history",

)

agent = initialize_agent(tools=tools,llm=chain)




