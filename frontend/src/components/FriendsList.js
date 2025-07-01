// src/components/FriendsList.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const FriendsList = ({ userId }) => {
    const [friends, setFriends] = useState([]);

    useEffect(() => {
        const fetchFriends = async () => {
            try {
                const res = await axios.get(`http://localhost:8000/friends/${userId}`);
                setFriends(res.data);
            } catch (err) {
                console.error("Failed to fetch friends list");
            }
        };
        if (userId) fetchFriends();
    }, [userId]);

    return (
        <div className="friends-list">
            <h3>Friends</h3>
            {friends.length === 0 ? (
                <p>No friends yet.</p>
            ) : (
                friends.map(friend => (
                    <div key={friend.id} className="friend-item">
                        <span>{friend.username}</span>
                    </div>
                ))
            )}
        </div>
    );
};

export default FriendsList;