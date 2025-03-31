# routes.py
from flask import render_template, request, flash, redirect, url_for, session
from __init__ import db, app
from handler import book_appointment_handler
from admin_handler import admin_login_handler
from models import Appointment,Session
from sqlalchemy import text
from datetime import datetime


@app.route('/')
def home():
    booked_appointments = Appointment.query.order_by(Appointment.appointment_date.asc()).all()
    current_date = datetime.combine(datetime.today(), datetime.min.time())
    return render_template('home.html', booked_appointments=booked_appointments, current_date = current_date)

@app.route('/book-appointment', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        return book_appointment_handler()
    return render_template('book_appointment.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    # If admin is already logged in, redirect to dashboard
    if "admin_id" in session:
        return redirect(url_for("dashboard"))
    return admin_login_handler()

@app.route('/dashboard')
def dashboard():
    # Check if admin is logged in
    if "admin_id" not in session:
        flash("Please log in to access the admin dashboard.", "danger")
        return redirect(url_for("admin_login"))
    
    # Fetch appointments for the dashboard
    appointments = Appointment.query.all()
    current_date = datetime.combine(datetime.today(), datetime.min.time())
    return render_template('dashboard.html', appointments=appointments,current_date=current_date)

@app.route('/approve-appointment/<int:appointment_id>', methods=['POST'])
def approve_appointment(appointment_id):
    # Check if admin is logged in
    if "admin_id" not in session:
        flash("Please log in to approve appointments.", "danger")
        return redirect(url_for("admin_login"))

    # Find the appointment
    appointment = Appointment.query.get_or_404(appointment_id)

    # Update the status to "approved"
    appointment.status = "approved"
    db.session.commit()

    flash(f"Appointment {appointment_id} has been approved.", "success")
    return redirect(url_for("dashboard"))

@app.route('/view-appointments')
def view_appointments():
    appointments = Appointment.query.all()
    if not appointments:
        return "No appointments found."

    result = [
        f"ID: {appointment.id}, Name: {appointment.name}, Institute: {appointment.institute_name}, "
        f"Status: {appointment.status}, Date: {appointment.appointment_date}"
        for appointment in appointments
    ]
    
    return "\n".join(result)

@app.route('/test-connection')
def test_connection():
    if 'admin_id' not in session:
        return "Unauthorized access"

    try:
        # Wrap the raw SQL with text()
        result = db.session.execute(text("SELECT VERSION()"))
        version = result.fetchone()[0]
        return f"Connected to TiDB successfully! Server version: {version}"
    except Exception as e:
        return f"Failed to connect to TiDB: {str(e)}"

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
def admin():
    # Check if admin is logged in
    if "admin_id" not in session:
        flash("Please log in to access the admin page.", "danger")
        return redirect(url_for("admin_login"))
    return render_template('admin.html')