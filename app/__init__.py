from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.routes import main, owners, vets
    app.register_blueprint(main.bp)
    app.register_blueprint(owners.bp)
    app.register_blueprint(vets.bp)

    with app.app_context():
        db.create_all()

    return app
