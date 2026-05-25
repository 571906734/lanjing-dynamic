import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_mail import Message
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, mail
from models import User

auth_bp = Blueprint('auth', __name__)


def send_verification_email(user):
    """Send verification email. Returns True if sent, False if mail not configured."""
    if not current_app.config.get('MAIL_PASSWORD'):
        return False
    token = user.generate_verification_token()
    db.session.commit()
    verify_url = url_for('auth.verify_email', token=token, _external=True)
    msg = Message(
        subject='Verify your email - LanJing Ship Service',
        recipients=[user.email],
        body=f'''Welcome to LanJing Ship Service!

Please verify your email address by clicking the link below:
{verify_url}

If you did not create this account, please ignore this email.

Best regards,
LanJing Ship Service Team''')
    mail.send(msg)
    return True


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()
        remember = request.form.get('remember') == 'on'

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            if not user.is_verified and current_app.config.get('MAIL_PASSWORD'):
                flash('Please verify your email before logging in. Check your inbox.', 'warning')
                return render_template('auth/login.html')
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('auth/register.html')

        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'danger')
            return render_template('auth/register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('auth/register.html')

        user = User(username=username, email=email)
        user.set_password(password)

        # Auto-verify if mail not configured
        if not current_app.config.get('MAIL_PASSWORD'):
            user.is_verified = True

        db.session.add(user)
        db.session.commit()

        if user.is_verified:
            flash('Registration successful! Please log in.', 'success')
        else:
            if send_verification_email(user):
                flash('Registration successful! Please check your email to verify your account.', 'success')
            else:
                user.is_verified = True
                db.session.commit()
                flash('Registration successful! Please log in.', 'success')

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/verify/<token>')
def verify_email(token):
    if current_user.is_authenticated and current_user.is_verified:
        flash('Your email is already verified.', 'info')
        return redirect(url_for('main.index'))

    user = User.query.filter_by(verification_token=token).first()
    if not user:
        flash('Invalid or expired verification link.', 'danger')
        return redirect(url_for('auth.login'))

    if user.token_expired():
        flash('Verification link has expired. Please request a new one.', 'danger')
        return redirect(url_for('auth.login'))

    user.is_verified = True
    user.verified_at = datetime.utcnow()
    user.verification_token = None
    db.session.commit()

    flash('Email verified successfully! You can now log in.', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
