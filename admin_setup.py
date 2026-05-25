#!/usr/bin/env python3
"""
Admin setup script for LanJing Ship Service.
Run this script to create or reset the admin user.
Usage: python admin_setup.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from models import User

app = create_app('development')

with app.app_context():
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@lanjingship.com')
    password = os.environ.get('ADMIN_PASSWORD', 'LanJing2026!')

    existing = User.query.filter_by(username=username).first()
    if existing:
        print(f'[INFO] Admin user "{username}" already exists. Resetting password...')
        existing.set_password(password)
        existing.email = email
        existing.is_admin = True
        db.session.commit()
        print(f'[OK] Admin password reset successfully.')
    else:
        admin = User(
            username=username,
            email=email,
            is_admin=True,
        )
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f'[OK] Admin user "{username}" created successfully.')

    print(f'    Username: {username}')
    print(f'    Email:    {email}')
    print(f'    Password: {password}')
    print(f'    Admin:    True')