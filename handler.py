from flask import request, redirect, url_for, flash, send_file
from __init__ import db
from models import User, Appointment
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import io

def book_appointment_handler():
    if request.method == "POST":
        try:
            # Extract form data
            name = request.form["name"]
            institute_name = request.form["institute_name"]
            event_details = request.form["event_details"]
            contact_number = request.form["contact_number"]
            expected_turnover = request.form["expected_turnover"]
            request_date = datetime.strptime(request.form["request_date"], "%Y-%m-%d")
            
            existing_appointment = Appointment.query.filter(
                Appointment.appointment_date == request_date,
                Appointment.status == "approved"
            ).first()

            if existing_appointment:
                flash(f"The date {request_date.strftime('%Y-%m-%d')} is already booked and approved. Please choose another date.", "danger")
                return redirect(url_for("book_appointment"))

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

            # Generate the PDF
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter

            # Header: BGS and SJB Group of Institutions (with color)
            p.setFont("Helvetica-Bold", 16)
            p.setFillColor(HexColor("#007bff"))  # Blue color to match your app's theme
            p.drawCentredString(width / 2, height - 50, "BGS and SJB Group of Institutions")

            # Draw a line below the header
            p.setFillColor(HexColor("#000000"))  # Reset to black for other elements
            p.line(50, height - 70, width - 50, height - 70)

            # Appointment Details (with increased font size and border)
            p.setFont("Helvetica", 14)  # Increased font size for body
            text = p.beginText(50, height - 100)
            text.setLeading(22)  # Adjust line spacing for larger font
            text.textLine("Appointment Confirmation")
            text.textLine("")
            text.textLine(f"Confirmation ID: {new_appointment.id}")  # Add Confirmation ID
            text.textLine(f"Name: {name}")
            text.textLine(f"Institute Name: {institute_name}")
            text.textLine(f"Event Details: {event_details}")
            text.textLine(f"Contact Number: {contact_number}")
            text.textLine(f"Expected Turnover: {expected_turnover}")
            text.textLine(f"Request Date: {request_date.strftime('%Y-%m-%d')}")
            p.drawText(text)

            # Add a border around the appointment details
            text_height = 8 * 26  # 8 lines (including empty line) * line spacing
            border_bottom_y = height - 100 - text_height  # Bottom y-coordinate of the border
            p.rect(40, border_bottom_y, width - 80, text_height + 20, stroke=1, fill=0)

            # Signature Section: Positioned just below the border
            signature_y = border_bottom_y - 30  # 30 points below the border
            p.setFont("Helvetica-Bold", 12)
            p.drawString(50, signature_y, "Signatures of Respective Heads")

            # Head of Department
            p.setFont("Helvetica", 10)
            p.drawString(50, signature_y - 20, "Head of Department:")
            p.line(150, signature_y - 20, 300, signature_y - 20)  # Line for signature

            # Principal
            p.drawString(50, signature_y - 50, "Principal:")
            p.line(150, signature_y - 50, 300, signature_y - 50)  # Line for signature

            # Footer: Powered by CSE(DS) SJBIT
            p.setFont("Helvetica-Oblique", 10)
            p.drawCentredString(width / 2, 30, "Powered by  SJBIT  CSE(DS) K47")

            # Finalize the PDF
            p.showPage()
            p.save()

            # Reset buffer position to the beginning
            buffer.seek(0)

            # Flash success message
            flash("Appointment booked successfully! Your confirmation PDF is being downloaded.", "success")

            # Send the PDF as a downloadable file
            return send_file(
                buffer,
                as_attachment=True,
                download_name="appointment_confirmation.pdf",
                mimetype="application/pdf"
            )

        except Exception as e:
            flash(f"Error booking appointment: {e}", "danger")
            return redirect(url_for("book_appointment"))