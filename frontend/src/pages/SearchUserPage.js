// src/pages/SearchUserPage.js
import React, { useState } from 'react';
import axios from 'axios';

const SearchUserPage = ({ userId }) => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

    const handleSearch = async () => {
        if (!query.trim()) return;
        try {
            const res = await axios.get(`http://localhost:8000/users/search`, {
                params: { q: query }
            });
            setResults(res.data);
        } catch (err) {
            console.error("Search failed", err);
        }
    };

    const sendFriendRequest = async (targetId) => {
        try {
            await axios.post('http://localhost:8000/friends/request', {
                user_id: userId,
                target_id: targetId
            });
            alert("Friend request sent!");
        } catch (err) {
            alert("Failed to send friend request.");
        }
    };

    return (
        <div style={{ padding: "20px" }}>
            <h2>Search Users</h2>
            <input
                type="text"
                placeholder="Search by username or email"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
            />
            <button onClick={handleSearch}>Search</button>

            <ul style={{ marginTop: "20px" }}>
                {results.map(user => (
                    <li key={user.id} style={{
                        display: "flex",
                        justifyContent: "space-between",
                        borderBottom: "1px solid #ddd",
                        padding: "10px 0"
                    }}>
                        <span>{user.username} ({user.email})</span>
                        <button onClick={() => sendFriendRequest(user.id)}>Add Friend</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default SearchUserPage;