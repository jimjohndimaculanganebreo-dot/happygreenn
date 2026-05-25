import os
from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from .extensions import db
from .models.user import User

login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///happygreenn.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads", "covers")
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    from .routes.auth import auth_bp
    from .routes.public import public_bp
    from .routes.reader import reader_bp
    from .routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(reader_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        seed_admin()

    return app

def seed_admin():
    email = os.getenv("ADMIN_EMAIL", "author@happygreenn.com")
    password = os.getenv("ADMIN_PASSWORD", "admin123")

    if not User.query.filter_by(email=email).first():
        admin = User(
            username="happygreenn",
            email=email,
            password_hash=generate_password_hash(password),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()