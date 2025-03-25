from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('user', __name__, url_prefix='/api/users')


@bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    users = UserService.get_all_users()
    return jsonify([{'id': u.id, 'username': u.username, 'email': u.email} for u in users])


@bp.route('/', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    user = UserService.create_user(data)
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 201


@bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    # 验证是否为当前用户或管理员
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"msg": "没有权限修改其他用户信息"}), 403
        
    data = request.get_json()
    user = UserService.update_user(user_id, data)
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})


@bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    # 验证是否为当前用户或管理员
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"msg": "没有权限删除其他用户"}), 403
        
    UserService.delete_user(user_id)
    return jsonify({'message': 'User deleted successfully'})
