import uuid
from langserve import RemoteRunnable

# Create an instance of RemoteRunnable pointing to your running server
chat = RemoteRunnable("http://localhost:8000/cha")

# Generate a unique session_id for this chat session
session_id = str(uuid.uuid4())

# Prepare the input data for the chat
input_data = {
    "human_input": "What is your favorite animal?"
}

# Prepare the configuration with session_id
config = {
    "configurable": {
        "session_id": session_id
    }
}

# Invoke the chat server with the input data and configuration
response = chat.invoke(input_data, config=config)

# Print the response from the chat server
print(response)
