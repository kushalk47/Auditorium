from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import logging

db = SQLAlchemy()  # Initialize SQLAlchemy instance

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)  # Register the app with SQLAlchemy

    with app.app_context():
        
        try:
            from models import User, Appointment, Admin, Session  # Ensure all models are imported
            db.create_all()  # This will create tables in TiDB if they don’t exist
            print("Database tables checked/created successfully.")

        except Exception as e:
            logging.error(f"Error initializing the database: {e}")


    return app

app = create_app()

# Import routes after initializing app
import routes
