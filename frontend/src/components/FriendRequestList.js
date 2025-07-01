// src/components/FriendRequestList.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const FriendRequestList = ({ userId }) => {
    const [requests, setRequests] = useState([]);

    useEffect(() => {
        const fetchRequests = async () => {
            const res = await axios.get(`http://localhost:8000/friend-requests/${userId}`);
            setRequests(res.data);
        };
        if (userId) fetchRequests();
    }, [userId]);

    const acceptRequest = async (requestId) => {
        await axios.post(`http://localhost:8000/friend-requests/${requestId}/accept`);
        setRequests(requests.filter(req => req.id !== requestId));
    };

    return (
        <div className="friend-request-list">
            <h3>Pending Requests</h3>
            {requests.length === 0 ? (
                <p>No pending requests.</p>
            ) : (
                requests.map(req => (
                    <div key={req.id} className="request-item">
                        <span>{req.from_user.username}</span>
                        <button onClick={() => acceptRequest(req.id)}>Accept</button>
                    </div>
                ))
            )}
        </div>
    );
};

export default FriendRequestList;