import os
from flask import Flask
from config import config
from extensions import db, login_manager, mail, babel


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')

    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    babel.init_app(app)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # User loader for Flask-Login
    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Babel locale config
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'

    # Register blueprints
    from routes.main import main_bp
    from routes.services import services_bp
    from routes.cases import cases_bp
    from routes.quote import quote_bp
    from routes.news import news_bp
    from routes.auth import auth_bp
    from routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(services_bp, url_prefix='/services')
    app.register_blueprint(cases_bp, url_prefix='/case-studies')
    app.register_blueprint(quote_bp, url_prefix='/request-quote')
    app.register_blueprint(news_bp, url_prefix='/news')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Context processors
    from models import SiteSetting

    @app.context_processor
    def inject_settings():
        settings = {}
        try:
            all_settings = SiteSetting.query.all()
            for s in all_settings:
                settings[s.key] = s.value
        except Exception:
            pass
        return {
            'site_settings': settings,
            'current_year': 2026,
        }

    # Create tables and seed data
    with app.app_context():
        db.create_all()
        _seed_default_data(app)

    return app


def _seed_default_data(app):
    from models import SiteSetting, User

    defaults = {
        'site_name': 'LanJing Ship Service',
        'site_description': 'Your trusted partner for comprehensive marine equipment supply, technical solutions and ship services in Indonesia.',
        'company_name': 'AnHui LanJing Ship Service Co., Ltd.',
        'company_address': 'Room A02, No. 18 East Shipai Avenue, Industrial Park, Huaining County, Anqing City, Anhui Province, China',
        'company_phone': '008618956963823',
        'company_email': 'AhLanJing@outlook.com',
        'company_whatsapp': '008618956963823',
        'indonesia_office': 'Jakarta',
        'company_slogan': 'Sincere service, innovative communication, mutual success.',
        'meta_description': 'LanJing Ship Service - Your trusted partner for comprehensive marine equipment supply, technical solutions and ship services in Indonesia.',
    }

    for key, value in defaults.items():
        existing = SiteSetting.query.filter_by(key=key).first()
        if not existing:
            db.session.add(SiteSetting(key=key, value=value))

    # Seed default admin user
    if not User.query.filter_by(email='admin@lanjing.com').first():
        admin = User(
            username='admin',
            email='admin@lanjing.com',
            is_admin=True,
            is_verified=True,
        )
        admin.set_password('admin123')
        db.session.add(admin)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()


if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, port=5000)