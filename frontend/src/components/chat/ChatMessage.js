// src/components/chat/ChatMessage.js
import React from 'react';

function ChatMessage({ message, isSender }) {
  return (
    <div style={{
      textAlign: isSender ? 'right' : 'left',
      margin: '5px 0'
    }}>
      <span style={{
        display: 'inline-block',
        padding: '8px 12px',
        backgroundColor: isSender ? '#DCF8C6' : '#ECECEC',
        borderRadius: '10px',
        maxWidth: '70%'
      }}>
        {message.text}
      </span>
    </div>
  );
}

export default ChatMessage;