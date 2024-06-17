import React, { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { Button } from 'react-bootstrap';
import './App.css'; // Assuming this file exists for styling
import { RemoteRunnable } from "@langchain/core/runnables/remote";
import ErrorBoundary from './component/ErrorBoundary';

function App() {
  const [file, setFile] = useState(null);
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState('');

  // Instantiate RemoteRunnable for chat
  const chat = new RemoteRunnable("http://localhost:8000/chat");

  useEffect(() => {
    // Generate a unique session ID when the component mounts
    setSessionId(uuidv4());
  }, []);

  // Function to handle file selection
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  // Function to handle file upload
  const handleUpload = async (event) => {
    event.preventDefault();
    if (!file) {
      alert('Please select a file to upload.');
      return;
    }

    const url = `http://localhost:8000/upload-menu/${sessionId}`;
    const formData = new FormData();
    formData.append('file', file);
    formData.append('session_id', sessionId);

    const config = {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    };

    try {
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
        headers: config.headers,
      });

      const data = await response.json();
      console.log(data);
      setMessages((prevMessages) => [...prevMessages, { type: 'bot', text: data }]);
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file. Please try again.');
    }
  };

  // Function to handle chat message submission
  const handleChat = async (event) => {
    event.preventDefault();
    const message = event.target.message.value.trim();
    if (!message) {
      alert('Please enter a message.');
      return;
    }

    try {
      const response = await chat.invoke({ human_input: message, session_id: sessionId });
      console.log(response);
      setMessages((prevMessages) => [...prevMessages, { type: 'user', text: message }, { type: 'bot', text: response }]);
    } catch (error) {
      console.error('Error sending chat message:', error);
      alert('Error sending chat message. Please try again.');
    }

    event.target.reset();
  };

  return (
    <ErrorBoundary>
      <div className="App">
        <h1>Menu Analyzer Chatbot</h1>
        <form onSubmit={handleChat}>
          <input type="text" name="message" />
          <Button variant="primary" type="submit">Send</Button>
        </form>

        {/* File Upload Form */}
        <form onSubmit={handleUpload}>
          <input type="file" onChange={handleFileChange} />
          <Button variant="secondary" type="submit">Upload</Button>
        </form>

        {/* Display messages */}
        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.type}`}>
              {msg.text}
            </div>
          ))}
        </div>
      </div>
    </ErrorBoundary>
  );
}

export default App;
