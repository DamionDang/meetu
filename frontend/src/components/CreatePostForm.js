// src/components/CreatePostForm.js
import React, { useState } from 'react';
import axios from 'axios';

const CreatePostForm = ({ userId, onPostCreated }) => {
    const [content, setContent] = useState('');
    const [image, setImage] = useState(null);
    const [latitude, setLatitude] = useState('');
    const [longitude, setLongitude] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const getLocation = () => {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                setLatitude(position.coords.latitude);
                setLongitude(position.coords.longitude);
            },
            (err) => {
                setError("Failed to get location");
            }
        );
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!content.trim()) return;

        setLoading(true);
        try {
            const formData = new FormData();
            formData.append("content", content);
            formData.append("user_id", userId);
            formData.append("latitude", latitude);
            formData.append("longitude", longitude);
            if (image) formData.append("image", image);

            const res = await axios.post("http://localhost:8000/posts", formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            });

            onPostCreated(res.data);
            setContent('');
            setImage(null);
            setLatitude('');
            setLongitude('');
        } catch (err) {
            setError("Failed to create post.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="create-post-form">
            <h3>Create a New Post</h3>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <form onSubmit={handleSubmit}>
                <textarea
                    placeholder="What's on your mind?"
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    required
                />
                <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => setImage(e.target.files[0])}
                />
                <div>
                    <label>Latitude:</label>
                    <input
                        type="number"
                        step="any"
                        value={latitude}
                        onChange={(e) => setLatitude(e.target.value)}
                    />
                    <label>Longitude:</label>
                    <input
                        type="number"
                        step="any"
                        value={longitude}
                        onChange={(e) => setLongitude(e.target.value)}
                    />
                    <button type="button" onClick={getLocation}>Use Current Location</button>
                </div>
                <button type="submit" disabled={loading}>
                    {loading ? "Posting..." : "Post"}
                </button>
            </form>
        </div>
    );
};

export default CreatePostForm;