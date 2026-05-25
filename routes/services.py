from flask import Blueprint, render_template
from models import ServiceCategory, Product

services_bp = Blueprint('services', __name__)


@services_bp.route('/supply')
def supply():
    categories = ServiceCategory.query.filter_by(is_active=True)\
        .order_by(ServiceCategory.order).all()
    products = Product.query.filter_by(is_active=True)\
        .order_by(Product.order).all()
    return render_template('services/supply.html',
                           categories=categories,
                           products=products)


@services_bp.route('/technical')
def technical():
    return render_template('services/technical.html')
