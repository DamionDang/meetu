// src/components/chat/ChatWindow.js
import React, { useEffect, useRef, useState } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import socket from '../../utils/socket';

function ChatWindow({ selectedFriend }) {
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef();

  useEffect(() => {
    socket.on('receive_message', (data) => {
      if ((data.sender === selectedFriend.id || data.receiver === selectedFriend.id)) {
        setMessages(prev => [...prev, data]);
      }
    });

    return () => {
      socket.off('receive_message');
    };
  }, [selectedFriend]);
  const sendMessage = (text) => {
    const message = {
      sender: parseInt(localStorage.getItem('userId')),
      receiver: selectedFriend.id,
      text,
    };
    socket.emit('send_message', message);
    setMessages(prev => [...prev, message]);
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
      <div style={{ flex: 1, overflowY: 'auto', padding: '10px' }}>
        {messages.map((msg, i) => (
          <ChatMessage
            key={i}
            message={msg}
            isSender={msg.sender === parseInt(localStorage.getItem('userId'))}
          />
        ))}
        <div ref={messagesEndRef} />
      </div>
      <ChatInput onSendMessage={sendMessage} />
    </div>
  );
}

export default ChatWindow;