// src/pages/FriendDetailPage.js
import React, { useEffect, useState } from 'react';
import api from '../utils/api';

function FriendDetailPage({ match }) {
  const [friend, setFriend] = useState(null);

  useEffect(() => {
    const fetchFriend = async () => {
      try {
        const response = await api.get(`/friends/${match.params.id}/`);
        setFriend(response.data);
      } catch (error) {
        console.error('Failed to fetch friend details:', error);
      }
    };
    fetchFriend();
  }, [match.params.id]);

  if (!friend) return <div>Loading...</div>;

  return (
    <div>
      <h1>{friend.name}'s Profile</h1>
      <p>Email: {friend.email}</p>
      {/* 更多好友信息 */}
    </div>
  );
}

export default FriendDetailPage;