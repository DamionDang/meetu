# utils/exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class BusinessException(Exception):
    """业务异常基类"""
    def __init__(self, message, code=None, status_code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)

class AuthenticationException(BusinessException):
    """认证异常"""
    def __init__(self, message="认证失败"):
        super().__init__(message, code="AUTH_ERROR", status_code=status.HTTP_401_UNAUTHORIZED)

class PermissionException(BusinessException):
    """权限异常"""
    def __init__(self, message="权限不足"):
        super().__init__(message, code="PERMISSION_ERROR", status_code=status.HTTP_403_FORBIDDEN)

class ValidationException(BusinessException):
    """数据验证异常"""
    def __init__(self, message="数据验证失败"):
        super().__init__(message, code="VALIDATION_ERROR", status_code=status.HTTP_400_BAD_REQUEST)

class ResourceNotFoundException(BusinessException):
    """资源未找到异常"""
    def __init__(self, message="资源未找到"):
        super().__init__(message, code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)

def custom_exception_handler(exc, context):
    """统一异常处理器"""
    # 调用DRF的默认异常处理器
    response = exception_handler(exc, context)
    
    # 记录异常日志
    logger.error(f"Exception in {context['view'].__class__.__name__}: {str(exc)}", exc_info=True)
    
    if response is not None:
        # 自定义响应格式
        custom_response_data = {
            'success': False,
            'code': getattr(exc, 'code', 'ERROR'),
            'message': response.data.get('detail', str(exc)) if hasattr(response.data, 'get') else str(exc),
            'data': None,
            'timestamp': context['request'].META.get('HTTP_X_TIMESTAMP'),
        }
        response.data = custom_response_data
    else:
        # 处理自定义业务异常
        if isinstance(exc, BusinessException):
            custom_response_data = {
                'success': False,
                'code': exc.code,
                'message': exc.message,
                'data': None,
                'timestamp': context['request'].META.get('HTTP_X_TIMESTAMP'),
            }
            return Response(custom_response_data, status=exc.status_code)
        
        # 处理未预期的系统异常
        custom_response_data = {
            'success': False,
            'code': 'SYSTEM_ERROR',
            'message': '系统内部错误',
            'data': None,
            'timestamp': context['request'].META.get('HTTP_X_TIMESTAMP'),
        }
        return Response(custom_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response

class StandardResponse:
    """标准响应格式"""
    @staticmethod
    def success(data=None, message="操作成功", code="SUCCESS"):
        return Response({
            'success': True,
            'code': code,
            'message': message,
            'data': data,
        }, status=status.HTTP_200_OK)
    
    @staticmethod
    def error(message="操作失败", code="ERROR", status_code=status.HTTP_400_BAD_REQUEST):
        return Response({
            'success': False,
            'code': code,
            'message': message,
            'data': None,
        }, status=status_code)