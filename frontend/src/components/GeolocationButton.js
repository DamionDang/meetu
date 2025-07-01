// src/components/GeolocationButton.js
import React, { useState } from 'react';
import axios from 'axios';

const GeolocationButton = ({ userId, onLocationUpdate }) => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const getLocation = () => {
        setLoading(true);
        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const { latitude, longitude } = position.coords;
                try {
                    await axios.post("http://localhost:8000/location", null, {
                        params: { user_id: userId, latitude, longitude }
                    });
                    onLocationUpdate({ lat: latitude, lng: longitude });
                } catch (err) {
                    setError("Failed to update location.");
                } finally {
                    setLoading(false);
                }
            },
            (err) => {
                setError("Location access denied.");
                setLoading(false);
            }
        );
    };

    return (
        <div className="geolocation-button">
            <button onClick={getLocation} disabled={loading}>
                {loading ? "Updating..." : "Update My Location"}
            </button>
            {error && <p style={{ color: "red" }}>{error}</p>}
        </div>
    );
};

export default GeolocationButton;