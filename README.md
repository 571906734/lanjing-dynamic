# LanJing Ship Service - Dynamic Website

A full-featured Flask dynamic website for LanJing Ship Service, a marine equipment supply and technical solutions company based in China, serving the Indonesian maritime industry.

## Features

- **Public Website**: Home, About, Services (Marine Supply + Technical Solutions), Case Studies, News, Contact
- **Quote Request System**: Multi-field quote form with file upload, email notifications (customer confirmation + admin alert)
- **CMS Admin Panel**: Full content management for cases, news, products, categories, quotes, settings, and users
- **User Authentication**: Registration, login, logout via Flask-Login
- **Multi-language Ready**: English (active) + Indonesian (Bahasa Indonesia) framework via Flask-Babel
- **SEO Friendly**: Slug-based URLs, meta descriptions, semantic HTML
- **Responsive Design**: Mobile-friendly frontend and admin panel

## Tech Stack

- **Flask 3.0** - Web framework
- **SQLAlchemy + SQLite** - Database ORM
- **Flask-Login** - User authentication
- **Flask-Mail** - Email notifications
- **Flask-Babel** - Internationalization
- **Jinja2** - Template engine
- **Werkzeug** - Password hashing, file handling

## Quick Start

### Prerequisites

- Python 3.10+
- pip

### Installation

1. **Clone or extract the project**

```bash
cd lanjing-dynamic
```

2. **Create a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

```bash
cp .env.example .env
# Edit .env with your settings (especially SECRET_KEY and email config)
```

5. **Initialize the database and create admin user**

```bash
python admin_setup.py
```

This will:
- Create the SQLite database (lanjing.db)
- Create all tables
- Insert seed data (product categories, sample cases)
- Create an admin user: **admin@lanjing.com / admin123**

6. **Run the application**

```bash
flask run
```

Or directly:

```bash
python app.py
```

The site will be available at `http://localhost:5000`.

7. **Access the admin panel**

Navigate to `http://localhost:5000/admin` and log in with:
- Email: `admin@lanjing.com`
- Password: `admin123`

## Project Structure

```
lanjing-dynamic/
├── app.py              # Flask application factory
├── config.py           # Configuration classes (Dev/Prod)
├── models.py           # SQLAlchemy database models (8 tables)
├── extensions.py       # Flask extension instances
├── admin_setup.py      # Admin user creation script
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── routes/             # Blueprint route handlers
│   ├── main.py         # Home, About, Contact
│   ├── services.py     # Marine Supply, Technical Solutions
│   ├── cases.py        # Case Studies (list + detail)
│   ├── quote.py        # Quote form submission + email
│   ├── news.py         # News & Resources
│   ├── auth.py         # Login, Register, Logout
│   └── admin.py        # CMS admin panel
├── templates/          # Jinja2 templates
│   ├── base.html       # Base layout (header, nav, footer)
│   ├── index.html      # Homepage (dynamic)
│   ├── about.html      # About page
│   ├── quote.html      # Quote request form
│   ├── contact.html    # Contact page
│   ├── services/       # Service pages
│   ├── cases/          # Case study pages
│   ├── news/           # News pages
│   ├── auth/           # Login/Register pages
│   └── admin/          # CMS admin pages
├── static/             # Static assets
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript
│   └── uploads/        # File uploads
└── translations/       # i18n translation files
```

## Email Configuration

To enable email notifications for quote submissions, configure the email settings in `.env`:

**Gmail example:**
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
ADMIN_EMAIL=admin@lanjing.com
```

> For Gmail, you need to enable 2FA and generate an App Password.

**Test email without actual SMTP:**
If SMTP is not configured, the system will still save quote requests to the database and show a warning in the console. Email sending failures do not block quote submissions.

## Admin Panel

The admin panel at `/admin` provides:

| Section | Features |
|---------|----------|
| Dashboard | Stats overview (total/today quotes, cases, news) |
| Case Studies | CRUD with title, slug, client, scope, challenge, solution, results |
| News | Publish/draft toggle, full content editing |
| Products | Category + product management |
| Quotes | Status tracking (New/Pending/Quoted/Completed), notes |
| Settings | Company info, contact details, SEO meta |
| Users | Admin user management |

## Multi-language

Currently English is the active language. Indonesian (Bahasa Indonesia) translations are scaffolded in `translations/id/LC_MESSAGES/messages.po`. To activate:

1. Translate the strings in `messages.po`
2. Compile: `pybabel compile -d translations`
3. Add `/id/` URL prefix routing

## Production Deployment

For production:

1. Set `FLASK_ENV=production` in `.env`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Set up a reverse proxy (Nginx)
4. Use environment variables for sensitive config (never commit `.env`)
5. Configure proper email SMTP credentials
6. Set `SESSION_COOKIE_SECURE=True` if using HTTPS

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## Security Notes

- Change the default admin password immediately after first login
- Generate a strong `SECRET_KEY` (use `python -c "import secrets; print(secrets.token_hex(32))"`)
- Never commit `.env` to version control
- Ensure `static/uploads/` has proper permissions
- Consider rate limiting for the quote form in production

## License

Proprietary - AnHui LanJing Ship Service Co., Ltd.