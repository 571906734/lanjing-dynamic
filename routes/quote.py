import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from extensions import db, mail
from models import QuoteRequest
from flask_mail import Message

quote_bp = Blueprint('quote', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx', 'xls', 'xlsx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@quote_bp.route('/', methods=['GET', 'POST'])
def request_quote():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        company = request.form.get('company', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        country = request.form.get('country', '').strip()
        service_type = request.form.get('service_type', '').strip()
        vessel_type = request.form.get('vessel_type', '').strip()
        location = request.form.get('location', '').strip()
        requirements = request.form.get('requirements', '').strip()
        timeline = request.form.get('timeline', '').strip()
        budget = request.form.get('budget', '').strip()

        if not name or not company or not email or not service_type or not location or not requirements:
            flash('Please fill in all required fields.', 'danger')
            return render_template('quote.html')

        # Handle file upload
        file_path = None
        file = request.files.get('file')
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'quotes')
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)

        quote = QuoteRequest(
            name=name,
            company=company,
            email=email,
            phone=phone,
            country=country,
            service_type=service_type,
            vessel_type=vessel_type,
            location=location,
            requirements=requirements,
            file_path=file_path,
            timeline=timeline,
            budget=budget,
        )
        db.session.add(quote)
        db.session.commit()

        # Send confirmation email to customer
        try:
            msg = Message(
                subject=f'Quote Request Received - {company}',
                recipients=[email],
                body=f'''Dear {name},

Thank you for your quote request to LanJing Ship Service.

We have received your inquiry for: {service_type}
Location: {location}

Our team will review your requirements and respond within 24 hours.

If you have any urgent needs, please contact us directly:
Phone/WhatsApp: 008618956963823
Email: AhLanJing@outlook.com

Best regards,
LanJing Ship Service Team
'''
            )
            mail.send(msg)
        except Exception:
            pass  # Email failure shouldn't block form submission

        # Notify admin
        try:
            admin_msg = Message(
                subject=f'New Quote Request from {company}',
                recipients=[current_app.config['ADMIN_EMAIL']],
                body=f'''New quote request received:

Name: {name}
Company: {company}
Email: {email}
Phone: {phone}
Country: {country}
Service Type: {service_type}
Vessel Type: {vessel_type}
Location: {location}
Timeline: {timeline}
Budget: {budget}

Requirements:
{requirements}

View in admin: {url_for('admin.view_quotes', _external=True)}
'''
            )
            mail.send(admin_msg)
        except Exception:
            pass

        flash('Your quote request has been submitted successfully! We will respond within 24 hours.', 'success')
        return redirect(url_for('quote.request_quote'))

    return render_template('quote.html')
