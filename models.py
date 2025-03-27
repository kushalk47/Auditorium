from __init__ import db  # Import db from __init__.py instead of creating a new one
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Users Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    institute_name = db.Column(db.String(200), nullable=False)
    event_details = db.Column(db.Text, nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    expected_turnover = db.Column(db.Integer, nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)

# Appointment Table
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    institute_name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default="Pending")
    appointment_date = db.Column(db.DateTime, nullable=False)

# Admin Table (with password hashing)
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Sessions Table (Only for Admin)
class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    session_token = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    admin = db.relationship('Admin', backref=db.backref('sessions', lazy=True))