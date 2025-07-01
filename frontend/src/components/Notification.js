// src/components/Notification.js
import React, { useEffect, useState } from 'react';

const Notification = ({ userId }) => {
    const [notifications, setNotifications] = useState([]);
    const ws = useRef(null);

    useEffect(() => {
        ws.current = new WebSocket(`ws://localhost:8000/ws/notifications/${userId}/`);

        ws.current.onmessage = (event) => {
            const notification = JSON.parse(event.data);
            setNotifications(prev => [notification, ...prev]);
        };

        return () => {
            if (ws.current) ws.current.close();
        };
    }, [userId]);

    return (
        <div style={{ maxHeight: "300px", overflowY: "auto", padding: "10px" }}>
            <h3>Notifications</h3>
            {notifications.length === 0 && <p>No notifications yet.</p>}
            {notifications.map((notif, index) => (
                <div key={index} style={{
                    border: "1px solid #eee",
                    padding: "10px",
                    marginBottom: "10px",
                    borderRadius: "4px",
                    backgroundColor: notif.read ? "#f9f9f9" : "#e6f7ff"
                }}>
                    <strong>{notif.type}</strong>
                    <p>{notif.message}</p>
                    <small>{new Date(notif.timestamp).toLocaleString()}</small>
                </div>
            ))}
        </div>
    );
};

export default Notification;