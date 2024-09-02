from Kridic import agent
import chainlit as cl
from langchain.schema.runnable.config import RunnableConfig
from langchain.schema.runnable import Runnable

@cl.on_chat_start
async def on_chat_start():
    files = None

    # Wait for the user to upload a file
    while files == None:
        files = await cl.AskFileMessage(
            content="Please upload a text file to begin!", accept=["image/jpeg", "image/png"]
        ).send()

    image_file = files[0]

    # Let the user know that the system is ready
    
    await cl.Message(
        content=f"`{image_file.name}` uploaded"
    ).send()

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
