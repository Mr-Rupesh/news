# Xnews — Live News Aggregator

A Django web application that fetches and displays real-time news from NewsAPI. Authenticated users can browse the latest headlines and leave short comments on articles.

---

## Overview

Xnews is a full-stack Django project built to demonstrate proficiency in backend web development, third-party API integration, and user authentication. Rather than letting users create articles manually, the app pulls live news from [NewsAPI.org](https://newsapi.org) and stores them in a database — keeping the feed fresh and real.

**Key highlights:**

- Live news fetched from NewsAPI across categories like technology, sports, business, and more
- User registration and authentication with a custom user model
- Comment system (140-character limit) on any article, for authenticated users only
- Duplicate prevention using article URL as a unique external identifier
- Articles filtered to the last 24 hours by default, with an option to view all
- Deployed on Render with PostgreSQL in production and WhiteNoise for static files

---

## Tech Stack

- **Backend:** Django 6.0, Python
- **Database:** SQLite (development) / PostgreSQL (production)
- **External API:** NewsAPI.org
- **Frontend:** Bootstrap 5, django-crispy-forms
- **Deployment:** Render, Gunicorn, WhiteNoise

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Mr-Rupesh/news.git
cd news
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
NEWS_API_KEY=your-newsapi-key
```

> Get a free API key at [newsapi.org](https://newsapi.org)

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

### 7. Fetch news articles

```bash
# Fetch general news (default)
python manage.py fetch_news

# Fetch by category and count
python manage.py fetch_news --category technology --count 10

# Fetch by country
python manage.py fetch_news --country gb --count 20
```

Available categories: `business`, `entertainment`, `general`, `health`, `science`, `sports`, `technology`

---

## Contact

**Rupesh Malhipparge** — [rupeshmalhipparge@gmail.com](mailto:rupeshmalhipparge@gmail.com)
