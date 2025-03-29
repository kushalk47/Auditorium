# add_admin.py
from __init__ import create_app, db
from models import Admin

app = create_app()

with app.app_context():
    # Create a new admin
    admin = Admin(name="sjbit")
    admin.set_password("forty#SJBIT") # Set password
    db.session.add(admin)
    db.session.commit()
    print("Admin added successfully!")