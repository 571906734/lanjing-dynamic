#!/usr/bin/env python3
"""
Seed test data for LanJing Ship Service website
"""
import os
import sys
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, ServiceCategory, Product, CaseStudy, NewsArticle, QuoteRequest

app = create_app()

with app.app_context():
    print("Seeding test data...")
    
    # 1. Service Categories
    categories = [
        ServiceCategory(
            name="Marine Equipment",
            name_id="Peralatan Kelautan",
            slug="marine-equipment",
            description="High-quality marine equipment and spare parts",
            icon="fa-anchor",
            order=1
        ),
        ServiceCategory(
            name="Technical Services",
            name_id="Layanan Teknis",
            slug="technical-services",
            description="Professional technical support and maintenance",
            icon="fa-tools",
            order=2
        ),
        ServiceCategory(
            name="Repair & Maintenance",
            name_id="Perbaikan & Pemeliharaan",
            slug="repair-maintenance",
            description="Comprehensive repair and maintenance services",
            icon="fa-wrench",
            order=3
        )
    ]
    
    for cat in categories:
        existing = ServiceCategory.query.filter_by(slug=cat.slug).first()
        if not existing:
            db.session.add(cat)
            print(f"Added category: {cat.name}")
    
    # 2. Products
    products = [
        Product(
            category_id=1,
            name="Marine Diesel Engine Parts",
            name_id="Suku Cadang Mesin Diesel Kelautan",
            description="High-quality spare parts for marine diesel engines",
            features="Durable materials, corrosion-resistant, OEM standards",
            image_path="/static/images/products/engine-parts.jpg",
            order=1
        ),
        Product(
            category_id=1,
            name="Navigation Equipment",
            name_id="Peralatan Navigasi",
            description="Advanced navigation systems and equipment",
            features="GPS, radar, AIS, ECDIS compatible",
            image_path="/static/images/products/navigation.jpg",
            order=2
        ),
        Product(
            category_id=2,
            name="Technical Consultation",
            name_id="Konsultasi Teknis",
            description="Expert technical consultation services",
            features="24/7 support, on-site assistance, troubleshooting",
            order=1
        )
    ]
    
    for prod in products:
        existing = Product.query.filter_by(name=prod.name).first()
        if not existing:
            db.session.add(prod)
            print(f"Added product: {prod.name}")
    
    # 3. Case Studies
    cases = [
        CaseStudy(
            title="Major Engine Overhaul for Bulk Carrier",
            slug="major-engine-overhaul-bulk-carrier",
            client_name="PT. Indonesia Shipping",
            service_type="Repair & Maintenance",
            scope="Complete overhaul of main engine and auxiliary systems",
            challenge="Engine performance degradation and frequent breakdowns",
            solution="Comprehensive inspection, replacement of worn parts, and system optimization",
            results="Engine performance restored to 95% of original capacity, fuel efficiency improved by 15%",
            is_featured=True
        ),
        CaseStudy(
            title="Navigation System Upgrade for Tanker",
            slug="navigation-system-upgrade-tanker",
            client_name="Oceanic Tankers Ltd.",
            service_type="Technical Services",
            scope="Upgrade of navigation and communication systems",
            challenge="Obsolete equipment and compliance issues",
            solution="Installation of modern ECDIS, AIS, and satellite communication systems",
            results="Full compliance with international regulations, improved safety and efficiency",
            is_featured=True
        )
    ]
    
    for case in cases:
        existing = CaseStudy.query.filter_by(slug=case.slug).first()
        if not existing:
            db.session.add(case)
            print(f"Added case study: {case.title}")
    
    # 4. News Articles (add one more)
    news = NewsArticle(
        title="LanJing Expands Services to Eastern Indonesia",
        slug="lanjing-expands-services-eastern-indonesia",
        summary="LanJing Ship Service announces expansion of operations to Eastern Indonesia",
        content="We are pleased to announce the expansion of our services to Eastern Indonesia...",
        is_published=True,
        published_at=datetime.utcnow()
    )
    
    existing_news = NewsArticle.query.filter_by(slug=news.slug).first()
    if not existing_news:
        db.session.add(news)
        print(f"Added news article: {news.title}")
    
    # 5. Test Quote Request
    quote = QuoteRequest(
        name="Test Customer",
        company="Test Shipping Co.",
        email="test@example.com",
        phone="+62 812 3456 7890",
        service_type="Technical Services",
        vessel_type="Container Ship",
        requirements="Need consultation for engine maintenance",
        status="new"
    )
    
    existing_quote = QuoteRequest.query.filter_by(email=quote.email).first()
    if not existing_quote:
        db.session.add(quote)
        print(f"Added test quote request: {quote.name}")
    
    try:
        db.session.commit()
        print("Test data seeded successfully!")
        
        # Show summary
        print("\nDatabase Summary:")
        print(f"Service Categories: {ServiceCategory.query.count()}")
        print(f"Products: {Product.query.count()}")
        print(f"Case Studies: {CaseStudy.query.count()}")
        print(f"News Articles: {NewsArticle.query.count()}")
        print(f"Quote Requests: {QuoteRequest.query.count()}")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding data: {e}")
        sys.exit(1)