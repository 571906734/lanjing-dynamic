import os
from datetime import datetime
from functools import wraps
from flask import (Blueprint, render_template, request, redirect,
                   url_for, flash, current_app)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from extensions import db
from models import (User, ServiceCategory, Product, CaseStudy,
                    NewsArticle, QuoteRequest, SiteSetting, Document)

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    total_quotes = QuoteRequest.query.count()
    today = datetime.utcnow().date()
    today_quotes = QuoteRequest.query.filter(
        db.func.date(QuoteRequest.created_at) == today
    ).count()
    total_cases = CaseStudy.query.count()
    total_news = NewsArticle.query.count()
    recent_quotes = QuoteRequest.query.order_by(
        QuoteRequest.created_at.desc()
    ).limit(5).all()
    return render_template('admin/dashboard.html',
                           total_quotes=total_quotes,
                           today_quotes=today_quotes,
                           total_cases=total_cases,
                           total_news=total_news,
                           recent_quotes=recent_quotes)


@admin_bp.route('/cases', methods=['GET', 'POST'])
@admin_bp.route('/cases/<int:case_id>', methods=['GET', 'POST'])
@admin_required
def manage_cases(case_id=None):
    case = None
    if case_id:
        case = CaseStudy.query.get_or_404(case_id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        slug = request.form.get('slug', '').strip() or title.lower().replace(' ', '-').replace('/', '-')
        client_name = request.form.get('client_name', '').strip()
        service_type = request.form.get('service_type', '').strip()
        scope = request.form.get('scope', '').strip()
        challenge = request.form.get('challenge', '').strip()
        solution = request.form.get('solution', '').strip()
        results = request.form.get('results', '').strip()
        is_featured = request.form.get('is_featured') == 'on'

        if not title:
            flash('Title is required.', 'danger')
            all_cases = CaseStudy.query.order_by(CaseStudy.created_at.desc()).all()
            return render_template('admin/cases.html', cases=all_cases, edit_case=case)

        if case:
            case.title = title
            case.slug = slug
            case.client_name = client_name
            case.service_type = service_type
            case.scope = scope
            case.challenge = challenge
            case.solution = solution
            case.results = results
            case.is_featured = is_featured
            flash('Case study updated.', 'success')
        else:
            case = CaseStudy(
                title=title, slug=slug, client_name=client_name,
                service_type=service_type, scope=scope,
                challenge=challenge, solution=solution, results=results,
                is_featured=is_featured
            )
            db.session.add(case)
            flash('Case study created.', 'success')

        db.session.commit()
        return redirect(url_for('admin.manage_cases'))

    all_cases = CaseStudy.query.order_by(CaseStudy.created_at.desc()).all()
    return render_template('admin/cases.html', cases=all_cases, edit_case=case)


@admin_bp.route('/cases/<int:case_id>/delete', methods=['POST'])
@admin_required
def delete_case(case_id):
    case = CaseStudy.query.get_or_404(case_id)
    db.session.delete(case)
    db.session.commit()
    flash('Case study deleted.', 'success')
    return redirect(url_for('admin.manage_cases'))


@admin_bp.route('/news', methods=['GET', 'POST'])
@admin_bp.route('/news/<int:article_id>', methods=['GET', 'POST'])
@admin_required
def manage_news(article_id=None):
    article = None
    if article_id:
        article = NewsArticle.query.get_or_404(article_id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        slug = request.form.get('slug', '').strip() or title.lower().replace(' ', '-')
        summary = request.form.get('summary', '').strip()
        content = request.form.get('content', '').strip()
        is_published = request.form.get('is_published') == 'on'

        if not title:
            flash('Title is required.', 'danger')
            all_articles = NewsArticle.query.order_by(NewsArticle.created_at.desc()).all()
            return render_template('admin/news.html', articles=all_articles, edit_article=article)

        if article:
            article.title = title
            article.slug = slug
            article.summary = summary
            article.content = content
            article.is_published = is_published
            if is_published and not article.published_at:
                article.published_at = datetime.utcnow()
            flash('Article updated.', 'success')
        else:
            article = NewsArticle(
                title=title, slug=slug, summary=summary, content=content,
                is_published=is_published,
                published_at=datetime.utcnow() if is_published else None
            )
            db.session.add(article)
            flash('Article created.', 'success')

        db.session.commit()
        return redirect(url_for('admin.manage_news'))

    all_articles = NewsArticle.query.order_by(NewsArticle.created_at.desc()).all()
    return render_template('admin/news.html', articles=all_articles, edit_article=article)


@admin_bp.route('/news/<int:article_id>/delete', methods=['POST'])
@admin_required
def delete_news(article_id):
    article = NewsArticle.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    flash('Article deleted.', 'success')
    return redirect(url_for('admin.manage_news'))


@admin_bp.route('/products', methods=['GET', 'POST'])
@admin_bp.route('/products/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def manage_products(product_id=None):
    product = None
    if product_id:
        product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category_id = request.form.get('category_id', type=int)
        description = request.form.get('description', '').strip()
        features = request.form.get('features', '').strip()
        order = request.form.get('order', type=int, default=0)
        is_active = request.form.get('is_active') == 'on'

        if not name:
            flash('Name is required.', 'danger')
            categories = ServiceCategory.query.order_by(ServiceCategory.order).all()
            all_products = Product.query.order_by(Product.order).all()
            return render_template('admin/products.html',
                                   products=all_products,
                                   categories=categories,
                                   edit_product=product)

        if product:
            product.name = name
            product.category_id = category_id
            product.description = description
            product.features = features
            product.order = order
            product.is_active = is_active
            flash('Product updated.', 'success')
        else:
            product = Product(
                name=name, category_id=category_id,
                description=description, features=features,
                order=order, is_active=is_active
            )
            db.session.add(product)
            flash('Product created.', 'success')

        db.session.commit()
        return redirect(url_for('admin.manage_products'))

    categories = ServiceCategory.query.order_by(ServiceCategory.order).all()
    all_products = Product.query.order_by(Product.order).all()
    return render_template('admin/products.html',
                           products=all_products,
                           categories=categories,
                           edit_product=product)


@admin_bp.route('/products/<int:product_id>/delete', methods=['POST'])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted.', 'success')
    return redirect(url_for('admin.manage_products'))


# Category management
@admin_bp.route('/categories', methods=['GET', 'POST'])
@admin_required
def manage_categories():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        slug = request.form.get('slug', '').strip() or name.lower().replace(' ', '-')
        description = request.form.get('description', '').strip()
        icon = request.form.get('icon', '').strip()
        order = request.form.get('order', type=int, default=0)

        if name:
            cat = ServiceCategory(
                name=name, slug=slug, description=description,
                icon=icon, order=order
            )
            db.session.add(cat)
            db.session.commit()
            flash('Category created.', 'success')
        return redirect(url_for('admin.manage_categories'))

    categories = ServiceCategory.query.order_by(ServiceCategory.order).all()
    return render_template('admin/products.html', categories=categories,
                           products=[], edit_product=None, manage_categories=True)


@admin_bp.route('/categories/<int:cat_id>/edit', methods=['POST'])
@admin_required
def edit_category(cat_id):
    cat = ServiceCategory.query.get_or_404(cat_id)
    cat.name = request.form.get('name', '').strip()
    cat.slug = request.form.get('slug', '').strip() or cat.name.lower().replace(' ', '-')
    cat.description = request.form.get('description', '').strip()
    cat.order = request.form.get('order', type=int, default=0)
    cat.is_active = request.form.get('is_active') == 'on'
    db.session.commit()
    flash('Category updated.', 'success')
    return redirect(url_for('admin.manage_categories'))


@admin_bp.route('/categories/<int:cat_id>/delete', methods=['POST'])
@admin_required
def delete_category(cat_id):
    cat = ServiceCategory.query.get_or_404(cat_id)
    db.session.delete(cat)
    db.session.commit()
    flash('Category deleted.', 'success')
    return redirect(url_for('admin.manage_categories'))


@admin_bp.route('/quotes')
@admin_required
def view_quotes():
    status_filter = request.args.get('status', '')
    if status_filter:
        quotes = QuoteRequest.query.filter_by(status=status_filter)\
            .order_by(QuoteRequest.created_at.desc()).all()
    else:
        quotes = QuoteRequest.query.order_by(QuoteRequest.created_at.desc()).all()
    return render_template('admin/quotes.html', quotes=quotes, status_filter=status_filter)


@admin_bp.route('/quotes/<int:quote_id>/update', methods=['POST'])
@admin_required
def update_quote(quote_id):
    quote = QuoteRequest.query.get_or_404(quote_id)
    new_status = request.form.get('status', '').strip()
    notes = request.form.get('notes', '').strip()

    if new_status in ('new', 'following', 'quoted', 'completed'):
        quote.status = new_status
    if notes:
        quote.notes = notes
    db.session.commit()
    flash('Quote updated.', 'success')
    return redirect(url_for('admin.view_quotes'))


@admin_bp.route('/quotes/<int:quote_id>/delete', methods=['POST'])
@admin_required
def delete_quote(quote_id):
    quote = QuoteRequest.query.get_or_404(quote_id)
    db.session.delete(quote)
    db.session.commit()
    flash('Quote deleted.', 'success')
    return redirect(url_for('admin.view_quotes'))


@admin_bp.route('/settings', methods=['GET', 'POST'])
@admin_required
def manage_settings():
    if request.method == 'POST':
        for key in request.form:
            if key.startswith('setting_'):
                setting_key = key[8:]
                setting = SiteSetting.query.filter_by(key=setting_key).first()
                if setting:
                    setting.value = request.form[key]
                else:
                    db.session.add(SiteSetting(key=setting_key, value=request.form[key]))
        db.session.commit()
        flash('Settings saved.', 'success')
        return redirect(url_for('admin.manage_settings'))

    settings = SiteSetting.query.all()
    return render_template('admin/settings.html', settings=settings)


@admin_bp.route('/users')
@admin_required
def manage_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)


@admin_bp.route('/users/add', methods=['POST'])
@admin_required
def add_user():
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    is_admin = request.form.get('is_admin') == 'on'

    if not username or not email or not password:
        flash('All fields are required.', 'danger')
        return redirect(url_for('admin.manage_users'))

    if User.query.filter_by(username=username).first():
        flash('Username already exists.', 'danger')
        return redirect(url_for('admin.manage_users'))

    user = User(username=username, email=email, is_admin=is_admin)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    flash('User created.', 'success')
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    if user_id == current_user.id:
        flash('You cannot delete yourself.', 'danger')
        return redirect(url_for('admin.manage_users'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted.', 'success')
    return redirect(url_for('admin.manage_users'))
