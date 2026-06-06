from app import db
from app.models.user import User


class UserService:
    @staticmethod
    def get_by_id(user_id):
        return db.session.get(User, user_id)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create_user(username, password, name, email, role="student", phone=None):
        user = User(
            username=username,
            name=name,
            email=email,
            role=role,
            phone=phone,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def authenticate(username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_students():
        return User.query.filter_by(role="student").all()

    @staticmethod
    def get_mentors():
        return User.query.filter_by(role="mentor").all()
