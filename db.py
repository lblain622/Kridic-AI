from pymongo import MongoClient

key="mongodb+srv://lucilleablain:vgT5rP8lpxknWGf2@main.3bttjdq.mongodb.net/?retryWrites=true&w=majority&appName=Main"

client = MongoClient(key, appname="Main")
DB_NAME="kridic_agent"
COLLECTION_NAME="KNOWLEDGE_BASE"
VECTORY_SEARCH ="vector_index"
collection=client[DB_NAME][COLLECTION_NAME]

try:
    client.server_info()
    print("Connected to the database")
except:
    print("Failed to connect to the database")

