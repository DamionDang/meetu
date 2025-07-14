// src/pages/ChatPage.js
import React, { useState } from 'react';
import ChatSidebar from '../components/chat/ChatSidebar';
import ChatWindow from '../components/chat/ChatWindow';

function ChatPage() {
  const [selectedFriend, setSelectedFriend] = useState(null);

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      <ChatSidebar onSelectFriend={setSelectedFriend} />
      {selectedFriend ? (
        <ChatWindow selectedFriend={selectedFriend} />
      ) : (
        <div style={{ flex: 1, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <p>请选择一个好友开始聊天</p>
        </div>
      )}
    </div>
  );
}

export default ChatPage;