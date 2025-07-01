// src/pages/FriendDetailPage.js
import React from 'react';
import ChatWindow from '../components/ChatWindow';

const FriendDetailPage = ({ userId }) => {
    const friendId = parseInt(window.location.pathname.split('/').pop());

    return (
        <div style={{ padding: "20px" }}>
            <h2>Chat with Friend ID: {friendId}</h2>
            <ChatWindow userId={userId} friendId={friendId} />
        </div>
    );
};

export default FriendDetailPage;