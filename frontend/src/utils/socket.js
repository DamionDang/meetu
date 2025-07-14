// src/utils/socket.js
import { io } from 'socket.io-client';

const socket = io('http://localhost:8000', {
  reconnection: true,
  reconnectionAttempts: Infinity,
  randomizationFactor: 0.5,
});

export default socket;