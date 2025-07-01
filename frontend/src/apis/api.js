// src/utils/api.js
import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://localhost:8000',
});

// 请求拦截器 - 添加 token
apiClient.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, error => {
    return Promise.reject(error);
});

// 响应拦截器 - 处理 401 错误等
apiClient.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;

        // 如果是 401 且不是刷新请求，则尝试刷新 token
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                const refreshToken = localStorage.getItem('refresh_token');
                const res = await axios.post('/auth/refresh-token', { refresh_token: refreshToken });
                const { token } = res.data;
                localStorage.setItem('token', token);
                apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
                return apiClient(originalRequest);
            } catch (err) {
                // 刷新失败，跳转到登录页
                window.location.href = '/login';
            }
        }

        return Promise.reject(error);
    }
);

export default apiClient;