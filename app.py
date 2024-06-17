from Kridic import agent
import chainlit as cl
from langchain.schema.runnable.config import RunnableConfig
from langchain.schema.runnable import Runnable

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("runnable", agent)

@cl.on_message
async def on_message(message:cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable
    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"human_input": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()  
