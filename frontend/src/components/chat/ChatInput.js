// src/components/chat/ChatInput.js
import React, { useState } from 'react';

function ChatInput({ onSendMessage }) {
  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim()) {
      onSendMessage(text);
      setText('');
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', padding: '10px' }}>
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="输入消息..."
        style={{ flex: 1, padding: '8px' }}
      />
      <button type="submit">发送</button>
    </form>
  );
}

export default ChatInput;