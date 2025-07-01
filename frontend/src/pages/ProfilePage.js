// src/pages/ProfilePage.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ProfilePage = ({ userId }) => {
    const [user, setUser] = useState(null);
    const [posts, setPosts] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const userRes = await axios.get(`http://localhost:8000/users/${userId}`);
                const postsRes = await axios.get(`http://localhost:8000/posts/user/${userId}`);
                setUser(userRes.data);
                setPosts(postsRes.data);
            } catch (err) {
                console.error("Failed to fetch profile data", err);
            }
        };
        if (userId) fetchData();
    }, [userId]);

    if (!user) return <p>Loading...</p>;

    return (
        <div style={{ padding: "20px" }}>
            <h2>{user.username}'s Profile</h2>
            <p>Email: {user.email}</p>
            <p>Friends: {user.friends_count || 0}</p>

            <h3>Your Posts</h3>
            {posts.length === 0 ? (
                <p>No posts yet.</p>
            ) : (
                posts.map(post => (
                    <div key={post.id} style={{
                        border: "1px solid #ccc",
                        borderRadius: "8px",
                        padding: "10px",
                        marginBottom: "10px"
                    }}>
                        <p>{post.content}</p>
                        {post.image && <img src={post.image} alt="Post" style={{ width: "100%", maxHeight: "200px" }} />}
                        <small>{new Date(post.timestamp).toLocaleString()}</small>
                    </div>
                ))
            )}
        </div>
    );
};

export default ProfilePage;