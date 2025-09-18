// src/components/chat/ChatWindow.js
import React, { useEffect, useRef, useState, useCallback, useMemo } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import LoadingSpinner from '../LoadingSpinner';
import socket from '../../utils/socket';

function ChatWindow({ selectedFriend }) {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(1);
  const messagesEndRef = useRef();
  const messagesContainerRef = useRef();
  const currentUserId = useMemo(() => parseInt(localStorage.getItem('userId')), []);

  // 使用useCallback优化事件处理函数
  const handleReceiveMessage = useCallback((data) => {
    if ((data.sender === selectedFriend.id || data.receiver === selectedFriend.id)) {
      setMessages(prev => {
        // 防止重复消息
        const isDuplicate = prev.some(msg => 
          msg.id === data.id || 
          (msg.text === data.text && msg.sender === data.sender && Math.abs(new Date(msg.timestamp) - new Date(data.timestamp)) < 1000)
        );
        
        if (isDuplicate) return prev;
        return [...prev, data];
      });
    }
  }, [selectedFriend.id]);

  // 优化消息发送函数
  const sendMessage = useCallback((text) => {
    if (!text.trim()) return;
    
    const message = {
      id: Date.now() + Math.random(), // 临时ID
      sender: currentUserId,
      receiver: selectedFriend.id,
      text: text.trim(),
      timestamp: new Date().toISOString(),
      status: 'sending' // 发送状态
    };
    
    // 立即添加到本地消息列表（乐观更新）
    setMessages(prev => [...prev, message]);
    
    // 发送到服务器
    socket.emit('send_message', message);
  }, [currentUserId, selectedFriend.id]);

  // 加载历史消息
  const loadMoreMessages = useCallback(async () => {
    if (loading || !hasMore) return;
    
    setLoading(true);
    try {
      // 这里应该调用API获取历史消息
      // const response = await api.get(`/chat/history/${selectedFriend.id}?page=${page}`);
      // const newMessages = response.data.messages;
      // setMessages(prev => [...newMessages, ...prev]);
      // setHasMore(response.data.has_more);
      // setPage(prev => prev + 1);
    } catch (error) {
      console.error('加载消息失败:', error);
    } finally {
      setLoading(false);
    }
  }, [loading, hasMore, page, selectedFriend.id]);

  // 监听WebSocket消息
  useEffect(() => {
    socket.on('receive_message', handleReceiveMessage);
    return () => {
      socket.off('receive_message', handleReceiveMessage);
    };
  }, [handleReceiveMessage]);

  // 自动滚动到底部
  useEffect(() => {
    const scrollToBottom = () => {
      messagesEndRef.current?.scrollIntoView({ 
        behavior: 'smooth',
        block: 'nearest'
      });
    };
    
    // 使用requestAnimationFrame确保DOM更新后再滚动
    requestAnimationFrame(scrollToBottom);
  }, [messages]);

  // 监听滚动事件，实现上拉加载更多
  useEffect(() => {
    const container = messagesContainerRef.current;
    if (!container) return;

    const handleScroll = () => {
      if (container.scrollTop === 0 && hasMore && !loading) {
        loadMoreMessages();
      }
    };

    container.addEventListener('scroll', handleScroll);
    return () => container.removeEventListener('scroll', handleScroll);
  }, [hasMore, loading, loadMoreMessages]);

  // 消息渲染优化 - 使用React.memo包装的组件
  const renderMessages = useMemo(() => {
    return messages.map((msg, index) => {
      const isLastMessage = index === messages.length - 1;
      const showTimestamp = index === 0 || 
        (new Date(msg.timestamp) - new Date(messages[index - 1].timestamp)) > 300000; // 5分钟
      
      return (
        <ChatMessage
          key={msg.id || `${msg.sender}-${msg.timestamp}-${index}`}
          message={msg}
          isSender={msg.sender === currentUserId}
          showTimestamp={showTimestamp}
          isLastMessage={isLastMessage}
        />
      );
    });
  }, [messages, currentUserId]);

  return (
    <div style={{ 
      flex: 1, 
      display: 'flex', 
      flexDirection: 'column',
      height: '100%',
      overflow: 'hidden'
    }}>
      {/* 消息列表容器 */}
      <div 
        ref={messagesContainerRef}
        style={{ 
          flex: 1, 
          overflowY: 'auto', 
          padding: '10px',
          scrollBehavior: 'smooth'
        }}
      >
        {/* 加载更多指示器 */}
        {loading && (
          <div style={{ textAlign: 'center', padding: '10px' }}>
            <LoadingSpinner size="small" message="加载消息中..." />
          </div>
        )}
        
        {/* 消息列表 */}
        {renderMessages}
        
        {/* 消息列表底部锚点 */}
        <div ref={messagesEndRef} />
      </div>
      
      {/* 输入区域 */}
      <ChatInput onSendMessage={sendMessage} disabled={loading} />
    </div>
  );
}

// 使用React.memo优化组件重渲染
export default React.memo(ChatWindow);