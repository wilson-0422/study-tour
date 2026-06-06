from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "请先登录后再访问此页面"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.routes import routes_bp
    from app.routes.registrations import registrations_bp
    from app.routes.insurances import insurances_bp
    from app.routes.accommodations import accommodations_bp
    from app.routes.achievements import achievements_bp
    from app.routes.mentors import mentors_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(routes_bp)
    app.register_blueprint(registrations_bp)
    app.register_blueprint(insurances_bp)
    app.register_blueprint(accommodations_bp)
    app.register_blueprint(achievements_bp)
    app.register_blueprint(mentors_bp)

    with app.app_context():
        db.create_all()

    return app
