# delete_all_data.py
from __init__ import create_app, db
from models import User, Appointment, Admin, Session

app = create_app()

def wipe_all_data():
    with app.app_context():
        try:
            # Double confirmation
            confirm = input("THIS WILL DELETE ALL DATA IN ALL TABLES. TYPE 'ERASE ALL' TO CONFIRM: ")
            if confirm.strip().lower() != 'erase all':
                print("Operation cancelled.")
                return

            # Delete order matters due to foreign keys
            Session.query.delete()
            Appointment.query.delete()
            User.query.delete()
            Admin.query.delete()  # Deletes ALL admins including root
            
            db.session.commit()
            print("Successfully deleted ALL data from all tables!")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error: {str(e)}")
            print("No changes were committed.")

if __name__ == "__main__":
    wipe_all_data()