from app import app, db
from models import User  # Change 'User' to your actual table name

with app.app_context():  # Ensure Flask app context is active
    try:
        users = User.query.all()
        if users:
            for user in users:
                print(user)
        else:
            print("Database initialized but no records found.")
    except Exception as e:
        print(f"Error accessing database: {e}")
