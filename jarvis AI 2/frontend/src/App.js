import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    // Establish WebSocket connection
    const newSocket = new WebSocket('ws://localhost:8000/ws');
    
    newSocket.onopen = () => {
      console.log('WebSocket Connected');
    };

    newSocket.onmessage = (event) => {
      setMessages(prevMessages => [
        ...prevMessages, 
        { text: event.data, sender: 'ai' }
      ]);
    };

    newSocket.onclose = () => {
      console.log('WebSocket Disconnected');
    };

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, []);

  const sendMessage = () => {
    if (socket && inputMessage) {
      socket.send(inputMessage);
      setMessages(prevMessages => [
        ...prevMessages, 
        { text: inputMessage, sender: 'user' }
      ]);
      setInputMessage('');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Assistant</h1>
        <div className="chat-container">
          {messages.map((message, index) => (
            <div 
              key={index} 
              className={`message ${message.sender}`}
            >
              {message.text}
            </div>
          ))}
        </div>
        <div className="input-container">
          <input 
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message..."
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </header>
    </div>
  );
}

export default App;
