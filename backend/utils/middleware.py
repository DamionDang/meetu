# utils/middleware.py
import logging
import time
import json
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    """请求日志中间件"""
    
    def process_request(self, request):
        request.start_time = time.time()
        
        # 记录请求信息
        log_data = {
            'method': request.method,
            'path': request.path,
            'user': str(request.user) if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous',
            'ip': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        }
        
        logger.info(f"Request started: {json.dumps(log_data)}")
        return None
    
    def process_response(self, request, response):
        # 计算请求处理时间
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            log_data = {
                'method': request.method,
                'path': request.path,
                'status_code': response.status_code,
                'duration': f"{duration:.3f}s",
                'user': str(request.user) if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous',
                'ip': self.get_client_ip(request),
            }
            
            # 根据响应状态选择日志级别
            if response.status_code >= 400:
                logger.warning(f"Request completed with error: {json.dumps(log_data)}")
            else:
                logger.info(f"Request completed: {json.dumps(log_data)}")
        
        return response
    
    def process_exception(self, request, exception):
        # 记录异常信息
        log_data = {
            'method': request.method,
            'path': request.path,
            'exception': str(exception),
            'user': str(request.user) if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous',
            'ip': self.get_client_ip(request),
        }
        
        logger.error(f"Request exception: {json.dumps(log_data)}", exc_info=True)
        return None
    
    def get_client_ip(self, request):
        """获取客户端IP地址"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SecurityLoggingMiddleware(MiddlewareMixin):
    """安全日志中间件"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.security_logger = logging.getLogger('django.security')
        super().__init__(get_response)
    
    def process_request(self, request):
        # 检测可疑请求
        self.check_suspicious_requests(request)
        return None
    
    def check_suspicious_requests(self, request):
        """检查可疑请求"""
        # 检查常见攻击模式
        suspicious_patterns = [
            'script', 'javascript:', 'vbscript:', 'onload', 'onerror',
            '../', '..\\', '/etc/passwd', 'cmd.exe', 'powershell'
        ]
        
        query_string = request.META.get('QUERY_STRING', '').lower()
        request_body = ''
        
        if request.method == 'POST' and request.content_type == 'application/json':
            try:
                request_body = request.body.decode('utf-8').lower()
            except:
                pass
        
        for pattern in suspicious_patterns:
            if pattern in query_string or pattern in request_body:
                self.security_logger.warning(
                    f"Suspicious request detected: {request.method} {request.path} "
                    f"from {self.get_client_ip(request)} - Pattern: {pattern}"
                )
                break
    
    def get_client_ip(self, request):
        """获取客户端IP地址"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip