from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():

    # Get absolute path of project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    template_path = os.path.join(project_root, "templates")

    app = Flask(__name__, template_folder=template_path)

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "main.login"
    login_manager.login_message = "Please log in to access this page."

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app