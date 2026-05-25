from flask import Blueprint, render_template, abort
from models import NewsArticle

news_bp = Blueprint('news', __name__)


@news_bp.route('/')
def list_news():
    articles = NewsArticle.query.filter_by(is_published=True)\
        .order_by(NewsArticle.published_at.desc()).all()
    return render_template('news/list.html', articles=articles)


@news_bp.route('/<slug>')
def news_detail(slug):
    article = NewsArticle.query.filter_by(slug=slug, is_published=True).first_or_404()
    return render_template('news/detail.html', article=article)
