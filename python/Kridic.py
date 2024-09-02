
from langchain_nvidia_ai_endpoints import ChatNVIDIA, NVIDIAEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import re
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from pathlib import Path
from typing import Callable, Union
from tools import *
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
import dotenv
from tools import *
import faiss

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

dotenv.load_dotenv()
key=os.getenv("NVIDIA_KEY")

from tempfile import TemporaryDirectory

from langchain_community.agent_toolkits import FileManagementToolkit




chat_prompts = ChatPromptTemplate.from_messages( [
        ("system", "You are a helpful Menu Analyzer AI bot that categorizes menu items with tags of possible allergens and ingrediants. You also can answer questions about the given food items or about food in general,based upon what the human asks. Your name is Kridic."),
        ("human","{human_input}"),

        MessagesPlaceholder(variable_name="history"),
    ])


chatter = ChatNVIDIA(model="meta/llama3-8b-instruct",
                     api_key=key,
                     base_url="https://integrate.api.nvidia.com/v1")

embedder = NVIDIAEmbeddings(model="snowflake/arctic-embed-l")
working_directory = TemporaryDirectory()

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


dest_embed_dir = Path("embeddings")
splitter = RecursiveCharacterTextSplitter()
def read_embedding(path: str):
    menu_info = extract_menu_info(path)
    texts = splitter.split_text(menu_info)
    documents = [Document(page_content=text, metadata={"source": path, "text": text}) for text in texts]
    
    if os.path.exists(dest_embed_dir):
        vecStore = FAISS.load_local(folder_path=dest_embed_dir, embeddings=embedder)
        vecStore.add_documents(documents)
        vecStore.save_local(folder_path=dest_embed_dir)
    else:
        vecStore = FAISS.from_documents(documents, embeddings=embedder)
        vecStore.save_local(folder_path=dest_embed_dir)

# Initialize Chat Prompt Template
chat_prompts = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful Menu Analyzer AI bot that categorizes menu items with tags of possible allergens and ingredients. You also can answer questions about the given food items or about food in general, based upon what the human asks. Your name is Kridic."),
    ("human", "{human_input}"),
    MessagesPlaceholder(variable_name="history"),
])

# Initialize chat model and memory
chatter = ChatNVIDIA(model="meta/llama3-8b-instruct", api_key=key, base_url="https://integrate.api.nvidia.com/v1")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Load embeddings
vectorStore = FAISS.load_local(folder_path=dest_embed_dir, embeddings=embedder,allow_dangerous_deserialization=True)

# Initialize the conversational retrieval agent
agent = ConversationalRetrievalChain.from_llm(
    llm=chatter,
    memory=memory,
    prompt=chat_prompts,
    output_parser=StrOutputParser(),
    retriever=vectorStore.as_retriever(),
)

