# remove_data.py
from __init__ import create_app, db
from models import User, Appointment, Admin, Session
from datetime import datetime, timedelta

app = create_app()

def delete_old_data():
    with app.app_context():
        try:
            # Safety confirmation
            confirm = input("WARNING: This will permanently delete data. Continue? (y/n): ").lower()
            if confirm != 'y':
                print("Operation cancelled.")
                return

            # Delete appointments older than 30 days with approved status
            appointment_cutoff = datetime.now() - timedelta(days=30)
            old_appointments = Appointment.query.filter(
                Appointment.status == 'approved',
                Appointment.appointment_date < appointment_cutoff
            ).all()
            
            for appt in old_appointments:
                db.session.delete(appt)
            print(f"Deleted {len(old_appointments)} old appointments")

            # Delete users older than 1 year
            user_cutoff = datetime.now() - timedelta(days=365)
            old_users = User.query.filter(User.request_date < user_cutoff).all()
            
            for user in old_users:
                db.session.delete(user)
            print(f"Deleted {len(old_users)} old users")

            # Delete non-root admins (keep 'admin' account)
            admins_to_delete = Admin.query.filter(Admin.name != 'admin').all()
            
            for admin in admins_to_delete:
                db.session.delete(admin)
            print(f"Deleted {len(admins_to_delete)} non-root admins")

            # Optional: Delete sessions older than 30 days
            session_cutoff = datetime.now() - timedelta(days=30)
            old_sessions = Session.query.filter(Session.created_at < session_cutoff).all()
            
            for session in old_sessions:
                db.session.delete(session)
            print(f"Deleted {len(old_sessions)} old sessions")

            db.session.commit()
            print("Cleanup completed successfully!")

        except Exception as e:
            db.session.rollback()
            print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    delete_old_data()