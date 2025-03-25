from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.services.user_service import UserService


def admin_required(fn):
    """
    自定义装饰器，检查当前用户是否为管理员
    这里只是一个示例，实际项目中需要添加用户角色字段来实现
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        # 这里应该有一个实际的角色检查，现在只是示例
        # 例如：user = UserService.get_user_by_id(user_id)
        # if user.role != 'admin':
        return fn(*args, **kwargs)
    return wrapper


def owner_required(fn):
    """
    自定义装饰器，检查当前用户是否为资源所有者
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        
        # 假设路由参数中有user_id
        resource_user_id = kwargs.get('user_id')
        
        if resource_user_id is not None and int(current_user_id) != int(resource_user_id):
            return jsonify({"msg": "没有权限访问该资源"}), 403
            
        return fn(*args, **kwargs)
    return wrapper 