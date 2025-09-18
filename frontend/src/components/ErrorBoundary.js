// src/components/ErrorBoundary.js
import React from 'react';
import './ErrorBoundary.css';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    // 更新状态，以便下次渲染时显示降级UI
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // 记录错误信息
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    
    this.setState({
      error: error,
      errorInfo: errorInfo
    });

    // 这里可以将错误发送到错误监控服务
    // logErrorToService(error, errorInfo);
  }

  handleReload = () => {
    // 重新加载页面
    window.location.reload();
  };

  handleGoHome = () => {
    // 返回首页
    window.location.href = '/';
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <div className="error-container">
            <div className="error-icon">⚠️</div>
            <h2>哎呀！出错了</h2>
            <p>很抱歉，页面遇到了一个错误。请尝试刷新页面或返回首页。</p>
            
            <div className="error-actions">
              <button onClick={this.handleReload} className="btn-primary">
                刷新页面
              </button>
              <button onClick={this.handleGoHome} className="btn-secondary">
                返回首页
              </button>
            </div>
            
            {process.env.NODE_ENV === 'development' && (
              <details className="error-details">
                <summary>技术详情（仅开发环境显示）</summary>
                <pre className="error-stack">
                  {this.state.error && this.state.error.toString()}
                  <br />
                  {this.state.errorInfo.componentStack}
                </pre>
              </details>
            )}
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;