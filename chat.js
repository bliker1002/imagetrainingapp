import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [modelName, setModelName] = useState('');
  const [userId, setUserId] = useState('');

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');
    setUserId(id);
    setModelName(`Model for ${id}`);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newMessage = { text: input, sender: 'user' };
    setMessages([...messages, newMessage]);
    setInput('');

    try {
      const response = await axios.post('/api/generate', {
        user_id: userId,
        prompt: input,
      });

      setMessages(msgs => [...msgs, { image: response.data.image_url, sender: 'bot' }]);
    } catch (error) {
      console.error('Error generating image:', error);
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="mb-4">{modelName}</h2>
      <div className="chat-messages p-3 bg-dark" style={{height: '400px', overflowY: 'auto'}}>
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender} mb-2`}>
            {msg.text ? 
              <p className="p-2 rounded bg-secondary text-white">{msg.text}</p> : 
              <img src={msg.image} alt="Generated" className="img-fluid rounded" />
            }
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="mt-3">
        <div className="input-group">
          <input
            type="text"
            className="form-control"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Describe the image you want..."
          />
          <button type="submit" className="btn btn-primary">Send</button>
        </div>
      </form>
    </div>
  );
}