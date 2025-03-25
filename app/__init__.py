from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta

# 创建Flask应用实例
db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3307/test_database?charset=utf8mb4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # JWT配置
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

    # 初始化数据库和JWT
    db.init_app(app)
    jwt.init_app(app)

    # 注册蓝图
    from .controllers import user_controller, auth_controller
    app.register_blueprint(user_controller.bp)
    app.register_blueprint(auth_controller.bp)

    @app.cli.command('init-db')
    def init_db():
        with app.app_context():
            db.create_all()
        print('Database initialized successfully!')

    return app
