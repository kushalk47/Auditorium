from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()  # Initialize SQLAlchemy instance

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)  # Register the app with SQLAlchemy

    with app.app_context():
        from models import User, Appointment, Admin, Session  # Ensure all models are imported
        db.create_all()  # This will create tables in TiDB if they don’t exist

    return app

app = create_app()

# Import routes after initializing app
import routes
