import getpass
import os


from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.nvidia import NVIDIAEmbedding
from llama_index.llms.nvidia import NVIDIA
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings

from llama_index.embeddings.nvidia import NVIDIAEmbedding

if not os.environ.get("NVIDIA_API_KEY", "").startswith("nvapi-"):
    nvidia_api_key = getpass.getpass("Enter your NVIDIA API key: ")
    assert nvidia_api_key.startswith("nvapi-"), f"{nvidia_api_key[:5]}... is not a valid key"
    os.environ["NVIDIA_API_KEY"] = nvidia_api_key
else:
    nvidia_api_key = os.environ["NVIDIA_API_KEY"]


#Configure the settings
Settings.text_splitter = SentenceSplitter(chunk_size=500)
Settings.llm= NVIDIA(model="meta/llama3-8b-instruct",nvidia_api_key=nvidia_api_key)
Settings.embed_model = NVIDIAEmbedding(model="embed-qa-4",nvidia_api_key=nvidia_api_key)

#Initialize the index and query engine
index= None
query_engine = None

