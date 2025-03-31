# add_admin.py
from __init__ import create_app, db
from models import Admin

app = create_app()

with app.app_context():
    # Create a new admin
    admin = Admin(name="kushal")
    admin.set_password("minimal1234") # Set password
    db.session.add(admin)
    db.session.commit()
    print("Admin added successfully!")