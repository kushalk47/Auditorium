# admin_handler.py
from flask import request, redirect, url_for, flash, session, render_template
from __init__ import db, app
from models import Admin, Session # Assuming 'Session' is your DB model for user sessions
from datetime import datetime
import uuid
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app=app, key_func=get_remote_address)

# --- Admin Login Handler ---
@app.route('/admin_login', methods=['GET', 'POST']) # Explicitly define methods
@limiter.limit("2 per minute")
def admin_login_handler():
    if request.method == "POST":
        try:
            # Extract form data
            name = request.form["name"]
            password = request.form["password"]

            # Find the admin in the database
            admin = Admin.query.filter_by(name=name).first()

            # Verify admin credentials
            if not admin or not admin.check_password(password):
                flash("Invalid username or password.", "danger")
                return redirect(url_for("admin_login_handler")) # Redirect to the login handler's own URL

            # Generate a unique session token
            session_token = str(uuid.uuid4())

            # Create a new session in the Session table
            # You might want to update an existing session if admin logs in again
            # For simplicity, creating a new one or handling expiry is common.
            # If you have an existing session record, you might want to invalidate it or update its token/timestamp.
            new_session = Session(
                admin_id=admin.id,
                session_token=session_token,
                created_at=datetime.utcnow()
            )
            db.session.add(new_session)
            db.session.commit()

            # Store admin details in Flask session
            session["admin_id"] = admin.id
            session["admin_name"] = admin.name
            session["session_token"] = session_token # Store the DB session token in Flask session

            # Flash success message
            flash("Login successful! Welcome to the admin dashboard.", "success")

            # Redirect to the dashboard route
            return redirect(url_for("dashboard"))

        except Exception as e:
            # Log the error for debugging, don't show raw error to user
            print(f"Error during admin login: {e}") 
            flash("An unexpected error occurred during login. Please try again.", "danger")
            return redirect(url_for("admin_login_handler"))

    # For GET requests, render the admin login page
    return render_template("admin_login.html")


# --- Admin Logout Handler ---
@app.route('/admin_logout')
def admin_logout():
    # Invalidate the session token in the database, if it exists
    if 'session_token' in session:
        db_session_token = session['session_token']
        # Find the session in the database and delete it
        user_session = Session.query.filter_by(session_token=db_session_token).first()
        if user_session:
            db.session.delete(user_session)
            db.session.commit()

    # Clear all items from the Flask session
    session.clear() # Clears all session data (admin_id, admin_name, session_token)

    flash('You have been logged out.', 'info')
    return redirect(url_for('admin_login_handler')) # Redirect to the admin login page