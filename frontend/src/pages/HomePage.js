// src/pages/HomePage.js
import React, { useEffect, useState } from 'react';
import MapComponent from '../components/MapComponent';
import PostFeed from '../components/PostFeed';
import Notification from '../components/Notification';
import GeolocationButton from '../components/GeolocationButton';
import FriendRequestList from '../components/FriendRequestList';
import FriendsList from '../components/FriendsList';
import CreatePostForm from '../components/CreatePostForm';
import { api } from '../utils/api';

const HomePage = ({ userId }) => {
    const [userLocation, setUserLocation] = useState(null);
    const [nearbyUsers, setNearbyUsers] = useState([]);
    const [posts, setPosts] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const usersRes = await api.get(`/nearby-users/${userId}`);
                const postsRes = await api.get(`/posts/nearby`, {
                    params: { user_id: userId }
                });

                setNearbyUsers(usersRes.data);
                setPosts(postsRes.data);
            } catch (err) {
                console.error("Failed to fetch data", err);
            }
        };
        if (userId) fetchData();
    }, [userId]);

    const handleLocationUpdate = (location) => {
        setUserLocation(location);
    };

    const handleLike = async (postId) => {
        await api.post(`/posts/${postId}/like`, { user_id: userId });
    };

    const handleComment = async (postId, content) => {
        await api.post(`/posts/${postId}/comment`, {
            user_id: userId,
            content
        });
    };

    const handlePostCreated = (newPost) => {
        setPosts([newPost, ...posts]);
    };

    return (
        <div style={{ display: "flex", height: "100vh" }}>
            <div style={{ flex: 3 }}>
                <MapComponent
                    userLocation={userLocation}
                    nearbyUsers={nearbyUsers}
                    posts={posts}
                />
                <GeolocationButton
                    userId={userId}
                    onLocationUpdate={handleLocationUpdate}
                />
                <CreatePostForm userId={userId} onPostCreated={handlePostCreated} />
            </div>
            <div style={{ flex: 1, borderLeft: "1px solid #ccc", padding: "10px" }}>
                <FriendRequestList userId={userId} />
                <FriendsList userId={userId} />
                <Notification userId={userId} />
                <PostFeed
                    posts={posts}
                    onLike={handleLike}
                    onComment={handleComment}
                />
            </div>
        </div>
    );
};

export default HomePage;