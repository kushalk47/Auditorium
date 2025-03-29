# admin_handler.py
from flask import request, redirect, url_for, flash, session,render_template
from __init__ import db
from models import Admin, Session
from datetime import datetime
import uuid

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
                return redirect(url_for("admin_login"))

            # Generate a unique session token
            session_token = str(uuid.uuid4())

            # Create a new session in the Session table
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
            session["session_token"] = session_token

            # Flash success message
            flash("Login successful! Welcome to the admin dashboard.", "success")

            # Redirect to the new dashboard route
            return redirect(url_for("dashboard"))

        except Exception as e:
            flash(f"Error during login: {str(e)}", "danger")
            return redirect(url_for("admin_login"))

    # For GET requests, render the admin login page
    return render_template("admin_login.html")