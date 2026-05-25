from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import NewsArticle, CaseStudy, ServiceCategory

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    latest_news = NewsArticle.query.filter_by(is_published=True)\
        .order_by(NewsArticle.published_at.desc()).limit(3).all()
    featured_cases = CaseStudy.query.filter_by(is_featured=True)\
        .order_by(CaseStudy.created_at.desc()).limit(3).all()
    if len(featured_cases) < 3:
        featured_cases = CaseStudy.query.order_by(CaseStudy.created_at.desc()).limit(3).all()
    categories = ServiceCategory.query.filter_by(is_active=True)\
        .order_by(ServiceCategory.order).all()
    return render_template('index.html',
                           latest_news=latest_news,
                           featured_cases=featured_cases,
                           categories=categories)


@main_bp.route('/about')
def about():
    return render_template('about.html')


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # 处理联系表单提交
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        # 这里可以添加邮件发送逻辑或数据库存储
        flash('Thank you for your message! We will contact you soon.', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('contact.html')
