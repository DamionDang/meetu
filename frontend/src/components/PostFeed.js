// src/components/PostFeed.js
import React, { useEffect, useState } from 'react';
import api from '../utils/api';

function PostFeed() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const fetchPosts = async () => {
      const res = await api.get('/posts/');
      setPosts(res.data);
    };
    fetchPosts();
  }, []);

  return (
    <div>
      {posts.map(post => (
        <div key={post.id}>
          <h4>{post.author.name}</h4>
          <p>{post.content}</p>
        </div>
      ))}
    </div>
  );
}

export default PostFeed;