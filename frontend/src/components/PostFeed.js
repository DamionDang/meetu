// src/components/PostFeed.js
import React, { useState } from 'react';

const PostFeed = ({ posts, onLike, onComment }) => {
    const [comments, setComments] = useState({});

    const handleLike = (postId) => {
        onLike(postId);
    };

    const handleCommentChange = (postId, e) => {
        setComments({
            ...comments,
            [postId]: e.target.value,
        });
    };

    const handleCommentSubmit = (postId) => {
        onComment(postId, comments[postId]);
        setComments({
            ...comments,
            [postId]: "",
        });
    };

    return (
        <div className="post-feed">
            {posts.map((post) => (
                <div key={post.id} className="post-card">
                    <h4>{post.user.username}</h4>
                    <p>{post.content}</p>
                    {post.image_url && <img src={post.image_url} alt="post" style={{ width: "100%", maxHeight: "200px" }} />}
                    <div>
                        <button onClick={() => handleLike(post.id)}>👍 Like</button>
                        <span> {post.likes_count || 0} Likes</span>
                    </div>
                    <div className="comments-section">
                        <input
                            type="text"
                            placeholder="Add a comment..."
                            value={comments[post.id] || ""}
                            onChange={(e) => handleCommentChange(post.id, e)}
                        />
                        <button onClick={() => handleCommentSubmit(post.id)}>Send</button>
                        {post.comments.map((comment) => (
                            <div key={comment.id} className="comment">
                                <strong>{comment.user.username}: </strong>
                                <span>{comment.content}</span>
                            </div>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
};

export default PostFeed;