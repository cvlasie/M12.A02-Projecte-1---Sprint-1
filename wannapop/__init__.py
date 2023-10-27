from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db_manager = SQLAlchemy()

def create_app():
    # Construct the core app object
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    # Secret key
    app.config["SECRET_KEY"]

    # paràmetre que farà servir SQLAlchemy per a connectar-se
    app.config["SQLALCHEMY_DATABASE_URI"]
    # mostre als logs les ordres SQL que s'executen
    app.config["SQLALCHEMY_ECHO"]

    # Inicialitza els plugins
    db_manager.init_app(app)

    with app.app_context():
        from . import routes_main

        # Registra els blueprints
        app.register_blueprint(routes_main.main_bp)

    app.logger.info("Aplicació iniciada")

    return app