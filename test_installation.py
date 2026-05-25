#!/usr/bin/env python3
"""
Test script to verify LanJing Flask dynamic website installation.
Run this after creating the project to check if everything is set up correctly.
"""

import os
import sys
import sqlite3

def check_project_structure():
    """Verify all required files and directories exist."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    required_files = [
        'app.py',
        'config.py',
        'models.py',
        'extensions.py',
        'admin_setup.py',
        'requirements.txt',
        '.env.example',
        'README.md',
        'routes/__init__.py',
        'routes/main.py',
        'routes/services.py',
        'routes/cases.py',
        'routes/quote.py',
        'routes/news.py',
        'routes/auth.py',
        'routes/admin.py',
        'templates/base.html',
        'templates/index.html',
        'static/css/style.css',
        'static/js/main.js',
        'static/css/admin.css',
        'static/js/admin.js',
        'translations/en/LC_MESSAGES/messages.po',
        'translations/id/LC_MESSAGES/messages.po'
    ]
    
    print("🔍 Checking project structure...")
    missing = []
    for file_path in required_files:
        full_path = os.path.join(base_path, file_path)
        if not os.path.exists(full_path):
            missing.append(file_path)
    
    if missing:
        print(f"❌ Missing {len(missing)} files:")
        for m in missing:
            print(f"   - {m}")
        return False
    else:
        print("✅ All required files exist")
        return True

def check_requirements():
    """Check if requirements.txt has all necessary packages."""
    print("\n📦 Checking requirements.txt...")
    base_path = os.path.dirname(os.path.abspath(__file__))
    req_path = os.path.join(base_path, 'requirements.txt')
    with open(req_path, 'r') as f:
        content = f.read()
    
    required_pkgs = [
        'Flask==3.0.0',
        'Flask-SQLAlchemy==3.1.1',
        'Flask-Login==0.6.3',
        'Flask-Mail==0.9.1',
        'Flask-Babel==4.0.0',
        'Flask-WTF==1.2.1',
        'WTForms==3.1.1',
        'email-validator==2.1.0',
        'Pillow==10.1.0',
        'python-dotenv==1.0.0',
        'Werkzeug==3.0.1'
    ]
    
    missing_pkgs = []
    for pkg in required_pkgs:
        if pkg not in content:
            missing_pkgs.append(pkg)
    
    if missing_pkgs:
        print(f"❌ Missing {len(missing_pkgs)} packages in requirements.txt:")
        for pkg in missing_pkgs:
            print(f"   - {pkg}")
        return False
    else:
        print("✅ All required packages listed in requirements.txt")
        return True

def check_database_models():
    """Check if database models are properly defined."""
    print("\n🗄️  Checking database models...")
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base_path, 'models.py'), 'r') as f:
            content = f.read()
        
        required_classes = [
            'class User(',
            'class ServiceCategory(',
            'class Product(',
            'class CaseStudy(',
            'class NewsArticle(',
            'class QuoteRequest(',
            'class SiteSetting(',
            'class Document('
        ]
        
        missing_classes = []
        for cls in required_classes:
            if cls not in content:
                missing_classes.append(cls)
        
        if missing_classes:
            print(f"❌ Missing {len(missing_classes)} model classes:")
            for cls in missing_classes:
                print(f"   - {cls}")
            return False
        else:
            print("✅ All database model classes defined")
            return True
    except Exception as e:
        print(f"❌ Error reading models.py: {e}")
        return False

def check_routes():
    """Check if all route blueprints are defined."""
    print("\n🛣️  Checking route blueprints...")
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base_path, 'app.py'), 'r') as f:
            content = f.read()
        
        required_blueprints = [
            'main_bp',
            'services_bp',
            'cases_bp',
            'quote_bp',
            'news_bp',
            'auth_bp',
            'admin_bp'
        ]
        
        missing_bps = []
        for bp in required_blueprints:
            if bp not in content:
                missing_bps.append(bp)
        
        if missing_bps:
            print(f"❌ Missing {len(missing_bps)} blueprints in app.py:")
            for bp in missing_bps:
                print(f"   - {bp}")
            return False
        else:
            print("✅ All route blueprints registered in app.py")
            return True
    except Exception as e:
        print(f"❌ Error reading app.py: {e}")
        return False

def check_templates():
    """Check if all templates exist and have basic content."""
    print("\n📄 Checking HTML templates...")
    base_path = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(base_path, 'templates')
    required_templates = [
        'base.html',
        'index.html',
        'about.html',
        'quote.html',
        'contact.html',
        'services/supply.html',
        'services/technical.html',
        'cases/list.html',
        'cases/detail.html',
        'news/list.html',
        'news/detail.html',
        'auth/login.html',
        'auth/register.html',
        'admin/dashboard.html',
        'admin/cases.html',
        'admin/news.html',
        'admin/products.html',
        'admin/quotes.html',
        'admin/settings.html',
        'admin/users.html'
    ]
    
    missing_templates = []
    for template in required_templates:
        path = os.path.join(templates_dir, template)
        if not os.path.exists(path):
            missing_templates.append(template)
        elif os.path.getsize(path) < 100:
            print(f"⚠️  Template {template} is very small ({os.path.getsize(path)} bytes)")
    
    if missing_templates:
        print(f"❌ Missing {len(missing_templates)} templates:")
        for tpl in missing_templates:
            print(f"   - {tpl}")
        return False
    else:
        print(f"✅ All {len(required_templates)} templates exist")
        return True

def main():
    print("=" * 60)
    print("LanJing Ship Service - Dynamic Website Installation Test")
    print("=" * 60)
    
    tests = [
        check_project_structure,
        check_requirements,
        check_database_models,
        check_routes,
        check_templates
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ ALL {total} TESTS PASSED!")
        print("\n🎉 The project is ready for installation.")
        print("\nNext steps:")
        print("1. Create virtual environment: python3 -m venv venv")
        print("2. Activate it: source venv/bin/activate (or venv\\Scripts\\activate on Windows)")
        print("3. Install dependencies: pip install -r requirements.txt")
        print("4. Copy .env.example to .env and configure your settings")
        print("5. Run admin_setup.py to create database and admin user")
        print("6. Start the server: python app.py")
        print("\nAdmin credentials will be: admin@lanjing.com / admin123")
        return 0
    else:
        print(f"❌ {passed}/{total} tests passed")
        print("\nPlease fix the issues above before proceeding.")
        return 1

if __name__ == '__main__':
    sys.exit(main())