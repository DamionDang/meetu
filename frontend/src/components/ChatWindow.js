// src/components/ChatWindow.js
import React, { useEffect, useRef, useState } from 'react';

const ChatWindow = ({ userId, friendId }) => {
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const ws = useRef(null);

    useEffect(() => {
        // 初始化 WebSocket 连接
        ws.current = new WebSocket(`ws://localhost:8000/ws/chat/${userId}/${friendId}/`);

        // 接收消息
        ws.current.onmessage = (event) => {
            const message = JSON.parse(event.data);
            setMessages((prev) => [...prev, message]);
        };

        // 错误处理
        ws.current.onerror = (error) => {
            console.error("WebSocket Error", error);
        };

        // 清理连接
        return () => {
            if (ws.current) {
                ws.current.close();
            }
        };
    }, [userId, friendId]);

    const sendMessage = () => {
        if (!inputValue.trim() || !ws.current || ws.current.readyState !== WebSocket.OPEN) return;

        const message = {
            sender: userId,
            receiver: friendId,
            content: inputValue,
            timestamp: new Date().toISOString()
        };

        ws.current.send(JSON.stringify(message));
        setMessages((prev) => [...prev, message]);
        setInputValue('');
    };

    return (
        <div style={{
            width: "100%",
            height: "400px",
            border: "1px solid #ccc",
            borderRadius: "8px",
            display: "flex",
            flexDirection: "column",
            overflow: "hidden"
        }}>
            <div style={{ flex: 1, padding: "10px", overflowY: "auto" }}>
                {messages.map((msg, index) => (
                    <div key={index} style={{
                        textAlign: msg.sender === parseInt(userId) ? "right" : "left",
                        margin: "5px 0"
                    }}>
                        <span style={{
                            display: "inline-block",
                            padding: "8px 12px",
                            backgroundColor: msg.sender === parseInt(userId) ? "#007bff" : "#eee",
                            color: msg.sender === parseInt(userId) ? "white" : "black",
                            borderRadius: "8px"
                        }}>
                            {msg.content}
                        </span>
                    </div>
                ))}
            </div>

            <div style={{
                display: "flex",
                borderTop: "1px solid #ccc",
                padding: "8px"
            }}>
                <input
                    type="text"
                    placeholder="Type a message..."
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    style={{ flex: 1, padding: "8px", borderRadius: "4px", border: "1px solid #ccc" }}
                />
                <button onClick={sendMessage} style={{ marginLeft: "8px" }}>Send</button>
            </div>
        </div>
    );
};

export default ChatWindow;