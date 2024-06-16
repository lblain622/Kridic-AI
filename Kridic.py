from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings,ChatNVIDIA
import uuid
from langserve import RemoteRunnable
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import re
from pathlib import Path
from typing import Callable, Union

from fastapi import FastAPI, HTTPException
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from langserve import add_routes
from langserve.pydantic_v1 import BaseModel, Field
key = "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"

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


app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
)




chat_prompts = ChatPromptTemplate.from_messages( [
        ("system", "You are a helpful Menu Analyzer AI bot that categorizes menu items with tags of possible allergens and ingrediants. You also can answer questions about the given food items or about food in general,based upon what the human asks. Your name is Kridic."),
        ("human","{human_input}"),
        MessagesPlaceholder(variable_name="history"),
    ])

#embedder = NVIDIAEmbeddings(model="snowflake/arctic-embed-l")

chatter = ChatNVIDIA(model="meta/llama3-8b-instruct",
                     api_key=key,
                     base_url="https://integrate.api.nvidia.com/v1")

chain = chat_prompts |chatter | StrOutputParser()
#answer=chatter.invoke("What is your name")

#chat = RemoteRunnable("http://localhost:8000/")
#session_id = str(uuid.uuid4())

class InputChat(BaseModel):
    human_input: str = Field(
        ...,
        title="Human input",
        description="The human input to the chatbot.",
        extra={"widget": {"type": "chat", "input": "human_input"}},
    )

chain_with_history = RunnableWithMessageHistory(
    chain,
    create_session_factory("chat_histories"),
    input_messages_key="human_input",
    history_messages_key="history",
).with_types(input_type=InputChat)

add_routes(app, chain_with_history)
@app.post("/chat")
async def chat(input: InputChat):
    response = await chain_with_history.invoke(
        input.dict(), 
        config={'configurable': {'session_id': input.session_id}}
    )
    return response

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)

