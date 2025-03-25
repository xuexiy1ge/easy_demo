from app.models.user import User
from app import db

class UserService:
    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def create_user(data):
        user = User(username=data.get('username'), email=data.get('email'))
        if user.username and user.email and data.get('password'):
            user.set_password(data.get('password'))
            db.session.add(user)
            db.session.commit()
            return user
        return None

    @staticmethod
    def authenticate_user(username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def update_user(user_id, data):
        user = User.query.get(user_id)
        if user:
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            if data.get('password'):
                user.set_password(data.get('password'))
            db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        return user
