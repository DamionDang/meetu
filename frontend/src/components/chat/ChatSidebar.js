// src/components/chat/ChatSidebar.js
import React, { useEffect, useState } from 'react';
import api from '../../utils/api';

function ChatSidebar({ onSelectFriend }) {
  const [friends, setFriends] = useState([]);

  useEffect(() => {
    const fetchFriends = async () => {
      const res = await api.get('/friends/');
      setFriends(res.data);
    };
    fetchFriends();
  }, []);

  return (
    <div style={{ width: '250px', borderRight: '1px solid #ccc', padding: '10px' }}>
      <h3>好友列表</h3>
      <ul style={{ listStyle: 'none', paddingLeft: 0 }}>
        {friends.map(friend => (
          <li key={friend.id}>
            <button onClick={() => onSelectFriend(friend)} style={{ width: '100%', padding: '8px', margin: '5px 0' }}>
              {friend.name} {friend.is_online ? '(在线)' : ''}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ChatSidebar;