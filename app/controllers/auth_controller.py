from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    jwt_required, get_jwt_identity
)
from app.services.user_service import UserService

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # 检查用户名是否已存在
    existing_user = UserService.authenticate_user(data.get('username'), None)
    if existing_user:
        return jsonify({"msg": "用户名已存在"}), 400
        
    user = UserService.create_user(data)
    if user:
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email
        }), 201
    return jsonify({"msg": "注册失败，请提供有效信息"}), 400


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = UserService.authenticate_user(username, password)
    
    if not user:
        return jsonify({"msg": "用户名或密码错误"}), 401
        
    # 创建访问令牌和刷新令牌
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    })


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    user = UserService.get_user_by_id(current_user_id)
    
    if not user:
        return jsonify({"msg": "用户不存在"}), 404
        
    access_token = create_access_token(identity=current_user_id)
    
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    })


@bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = UserService.get_user_by_id(current_user_id)
    
    if not user:
        return jsonify({"msg": "用户不存在"}), 404
        
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    }) 