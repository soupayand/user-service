from flask import Flask
from .database.connection import db
from flask_migrate import Migrate
from .api.user import user_bp
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()
    
    app = Flask(__name__)
    database_uri = os.getenv("DATABASE_URI")
    if database_uri is None:
        raise ConnectionError("Database connection uri not present in env file")
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    migrate = Migrate(app, db)

    app.register_blueprint(user_bp)
    
    # No need to call db.create_all() when using Flask-Migrate
    with app.app_context():
        db.create_all()
    
    return app
