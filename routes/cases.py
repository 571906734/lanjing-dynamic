from flask import Blueprint, render_template, abort
from models import CaseStudy

cases_bp = Blueprint('cases', __name__)


@cases_bp.route('/')
def list_cases():
    all_cases = CaseStudy.query.order_by(CaseStudy.created_at.desc()).all()
    return render_template('cases/list.html', cases=all_cases)


@cases_bp.route('/<slug>')
def case_detail(slug):
    case = CaseStudy.query.filter_by(slug=slug).first_or_404()
    return render_template('cases/detail.html', case=case)
