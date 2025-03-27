from flask import render_template, request, flash, redirect, url_for
from __init__ import db ,app
from handler import book_appointment_handler 
from models import Appointment
from sqlalchemy import text

@app.route('/')
def home():
    booked_appointments = Appointment.query.order_by(Appointment.appointment_date.asc()).all()
    return render_template('home.html', booked_appointments=booked_appointments)
    

@app.route('/book-appointment', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        return book_appointment_handler()
    return render_template('book_appointment.html')

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
    return render_template('admin.html')
