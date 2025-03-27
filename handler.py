from flask import request, redirect, url_for, flash
from __init__ import db
from models import User, Appointment
from datetime import datetime

def book_appointment_handler():
    if request.method == "POST":
        try:
            name = request.form["name"]
            institute_name = request.form["institute_name"]
            event_details = request.form["event_details"]
            contact_number = request.form["contact_number"]
            expected_turnover = request.form["expected_turnover"]
            request_date = datetime.strptime(request.form["request_date"], "%Y-%m-%d")

            # Store the appointment in the database
            new_user = User(
                name=name,
                institute_name=institute_name,
                event_details=event_details,
                contact_number=contact_number,
                expected_turnover=expected_turnover,
                request_date=request_date
            )
            db.session.add(new_user)
            db.session.commit()

            # Also store in Appointment table
            new_appointment = Appointment(
                name=name,
                institute_name=institute_name,
                appointment_date=request_date
            )
            db.session.add(new_appointment)
            db.session.commit()

            flash("Appointment booked successfully!", "success")
            return redirect(url_for("book_appointment"))

        except Exception as e:
            flash(f"Error booking appointment: {e}", "danger")
            return redirect(url_for("book_appointment"))

