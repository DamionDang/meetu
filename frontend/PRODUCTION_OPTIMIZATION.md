# Frontend Production Optimization Guide

## 1. 环境变量配置

创建 `.env.production` 文件：

```bash
# API配置
REACT_APP_API_BASE_URL=https://api.meetu.com
REACT_APP_WS_BASE_URL=wss://api.meetu.com

# CDN配置
REACT_APP_CDN_URL=https://cdn.meetu.com
REACT_APP_STATIC_URL=https://cdn.meetu.com/static

# 第三方服务
REACT_APP_GOOGLE_MAPS_KEY=your_google_maps_api_key
REACT_APP_SENTRY_DSN=your_sentry_dsn

# 性能监控
REACT_APP_ENABLE_ANALYTICS=true
REACT_APP_ANALYTICS_ID=your_analytics_id

# 功能开关
REACT_APP_ENABLE_PWA=true
REACT_APP_ENABLE_SERVICE_WORKER=true
```

## 2. Webpack 生产优化配置

在 `package.json` 中添加构建脚本：

```json
{
  "scripts": {
    "build:prod": "REACT_APP_ENV=production npm run build",
    "build:analyze": "npm run build && npx webpack-bundle-analyzer build/static/js/*.js",
    "build:gzip": "npm run build && gzip -9 build/static/**/*.{js,css}"
  }
}
```

## 3. CDN集成配置

### 3.1 修改 public/index.html 添加CDN预连接：

```html
<link rel="preconnect" href="https://cdn.meetu.com">
<link rel="dns-prefetch" href="https://api.meetu.com">
<link rel="preload" href="https://cdn.meetu.com/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
```

### 3.2 创建 CDN 工具类：

```javascript
// src/utils/cdn.js
const CDN_BASE_URL = process.env.REACT_APP_CDN_URL || '';

export const getCDNUrl = (path) => {
  if (!CDN_BASE_URL) return path;
  return `${CDN_BASE_URL}${path}`;
};

export const getOptimizedImageUrl = (url, options = {}) => {
  if (!url) return '';
  
  const { width, height, quality = 80, format = 'webp' } = options;
  const params = new URLSearchParams();
  
  if (width) params.append('w', width);
  if (height) params.append('h', height);
  params.append('q', quality);
  params.append('f', format);
  
  return `${getCDNUrl('/images/resize')}?url=${encodeURIComponent(url)}&${params.toString()}`;
};
```

## 4. Service Worker 配置

### 4.1 创建自定义 Service Worker：

```javascript
// public/sw.js
const CACHE_NAME = 'meetu-v1.0.0';
const STATIC_CACHE_URLS = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/manifest.json'
];

// 安装 Service Worker
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(STATIC_CACHE_URLS))
  );
});

// 网络优先策略，适用于API请求
self.addEventListener('fetch', (event) => {
  if (event.request.url.includes('/api/')) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          // 缓存成功的API响应
          if (response.status === 200) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME)
              .then((cache) => cache.put(event.request, responseClone));
          }
          return response;
        })
        .catch(() => {
          // 网络失败时从缓存返回
          return caches.match(event.request);
        })
    );
  } else {
    // 静态资源使用缓存优先策略
    event.respondWith(
      caches.match(event.request)
        .then((response) => response || fetch(event.request))
    );
  }
});
```

## 5. 性能监控配置

### 5.1 集成 Web Vitals：

```javascript
// src/utils/performance.js
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

const sendToAnalytics = (metric) => {
  // 发送性能数据到分析服务
  if (process.env.REACT_APP_ENABLE_ANALYTICS === 'true') {
    // gtag('event', metric.name, {
    //   event_category: 'Web Vitals',
    //   event_label: metric.id,
    //   value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
    //   non_interaction: true,
    // });
  }
};

export const initPerformanceMonitoring = () => {
  getCLS(sendToAnalytics);
  getFID(sendToAnalytics);
  getFCP(sendToAnalytics);
  getLCP(sendToAnalytics);
  getTTFB(sendToAnalytics);
};
```

## 6. 部署脚本

### 6.1 创建生产构建脚本：

```bash
#!/bin/bash
# deploy-frontend.sh

echo "开始前端生产部署..."

# 1. 安装依赖
npm ci --production=false

# 2. 运行测试
npm run test -- --coverage --watchAll=false

# 3. 构建生产版本
npm run build:prod

# 4. 压缩静态资源
find build/static -name "*.js" -exec gzip -9 -k {} \;
find build/static -name "*.css" -exec gzip -9 -k {} \;

# 5. 上传到CDN（示例：AWS S3）
if [ "$USE_S3_CDN" = "true" ]; then
    aws s3 sync build/ s3://$S3_BUCKET_NAME/ --delete --cache-control max-age=31536000
    aws cloudfront create-invalidation --distribution-id $CLOUDFRONT_DISTRIBUTION_ID --paths "/*"
fi

# 6. 部署到服务器
rsync -avz --delete build/ $DEPLOY_USER@$DEPLOY_HOST:$DEPLOY_PATH/

echo "前端部署完成！"
```

## 7. Nginx 配置优化

```nginx
server {
    listen 80;
    server_name meetu.com www.meetu.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name meetu.com www.meetu.com;
    
    # SSL 配置
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Strict-Transport-Security "max-age=63072000" always;
    
    # 根目录
    root /var/www/meetu/build;
    index index.html;
    
    # 静态资源缓存
    location /static/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        gzip_static on;
    }
    
    # 图片压缩
    location ~* \.(jpg|jpeg|png|gif|ico|svg)$ {
        expires 1M;
        add_header Cache-Control "public";
        gzip_static on;
    }
    
    # API 代理
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # WebSocket 代理
    location /ws/ {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # SPA 路由支持
    location / {
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "no-cache";
    }
    
    # Gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
}
```

## 8. Docker 生产配置

```dockerfile
# frontend/Dockerfile.prod
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --production=false

COPY . .
RUN npm run build:prod

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

这些配置将显著提升 MEETU 前端应用的性能和用户体验。