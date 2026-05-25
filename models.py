from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(64), unique=True, index=True)
    token_created_at = db.Column(db.DateTime)
    verified_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_verification_token(self):
        import secrets
        self.verification_token = secrets.token_urlsafe(48)
        self.token_created_at = datetime.utcnow()
        return self.verification_token

    def token_expired(self):
        if not self.token_created_at:
            return True
        from datetime import timedelta
        return datetime.utcnow() > self.token_created_at + timedelta(hours=24)

    def __repr__(self):
        return f'<User {self.username}>'


class ServiceCategory(db.Model):
    __tablename__ = 'service_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_id = db.Column(db.String(100))  # Indonesian name
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    icon = db.Column(db.String(200))
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    products = db.relationship('Product', backref='category', lazy='dynamic',
                               cascade='all, delete-orphan')

    def __repr__(self):
        return f'<ServiceCategory {self.name}>'


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    name_id = db.Column(db.String(200))  # Indonesian name
    description = db.Column(db.Text)
    description_id = db.Column(db.Text)
    features = db.Column(db.Text)
    features_id = db.Column(db.Text)
    image_path = db.Column(db.String(500))
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.name}>'


class CaseStudy(db.Model):
    __tablename__ = 'case_studies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    client_name = db.Column(db.String(200))
    service_type = db.Column(db.String(100))
    scope = db.Column(db.Text)
    challenge = db.Column(db.Text)
    solution = db.Column(db.Text)
    results = db.Column(db.Text)
    image_path = db.Column(db.String(500))
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CaseStudy {self.title}>'


class NewsArticle(db.Model):
    __tablename__ = 'news_articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    slug = db.Column(db.String(300), unique=True, nullable=False, index=True)
    summary = db.Column(db.Text)
    content = db.Column(db.Text)
    image_path = db.Column(db.String(500))
    is_published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<NewsArticle {self.title}>'


class QuoteRequest(db.Model):
    __tablename__ = 'quote_requests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50))
    country = db.Column(db.String(50))
    service_type = db.Column(db.String(100))
    vessel_type = db.Column(db.String(100))
    location = db.Column(db.String(200))
    requirements = db.Column(db.Text)
    file_path = db.Column(db.String(500))
    timeline = db.Column(db.String(50))
    budget = db.Column(db.String(50))
    status = db.Column(db.String(30), default='new')  # new, following, quoted, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<QuoteRequest {self.name} - {self.company}>'


class SiteSetting(db.Model):
    __tablename__ = 'site_settings'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<SiteSetting {self.key}>'


class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    title_id = db.Column(db.String(300))
    description = db.Column(db.Text)
    file_path = db.Column(db.String(500))
    category = db.Column(db.String(100))
    download_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Document {self.title}>'