# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Xnews** is a Django 6.0 live news aggregator that fetches real news from NewsAPI (newsapi.org). Users can view fetched news articles and add comments (140 character limit). Articles are automatically fetched from external APIs rather than created by users.

## Development Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Configuration
Create `.env` file (see `.env.example`):
```bash
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
NEWS_API_KEY=your-newsapi-key-here  # Get from newsapi.org
```

### Running the Server
```bash
# Development server
python manage.py runserver

# Or use the virtual environment
source .venv/bin/activate && python manage.py runserver
```

### Fetching News
```bash
# Fetch latest news (requires NEWS_API_KEY in .env)
python manage.py fetch_news

# Fetch specific category (business, entertainment, general, health, science, sports, technology)
python manage.py fetch_news --category technology --count 10

# Fetch from specific country (us, gb, ca, etc.)
python manage.py fetch_news --country gb --count 20
```

### Code Quality
```bash
# Format with Black
black .

# Check formatting without changes
black --check .
```

### Testing
```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test articles
python manage.py test accounts

# Run a specific test class
python manage.py test articles.tests.ArticleTests

# Run with verbosity
python manage.py test -v 2
```

### Database
```bash
# Create migrations
python manage.py makemigrations

# Shell with Django extensions
python manage.py shell_plus

# Database URL from environment (production uses PostgreSQL via DATABASE_URL)
```

## Architecture

### App Structure

| App | Purpose | Key Files |
|-----|---------|-----------|
| `accounts/` | Custom user authentication with age field | `models.py` (CustomUser), `forms.py` (CustomUserCreationForm), `views.py` (SignUpView) |
| `articles/` | News fetching and commenting | `models.py` (Article, Comment), `services/news_api.py` (fetch/parse logic), `management/commands/fetch_news.py` (CLI), `views.py` (List/Detail only) |
| `pages/` | Static pages (home) | `views.py` (HomePageView) |
| `django_project/` | Project configuration | `settings.py`, `urls.py` (root URLconf) |

### URL Routing Structure

```
/                    -> HomePageView (pages)
/accounts/signup/    -> SignUpView (accounts)
/accounts/login/     -> Django auth (built-in)
/accounts/logout/    -> Django auth (built-in)
/articles/           -> ArticleListView (paginated news list)
/articles/<pk>/       -> ArticleDetailView (article with comments)
/admin/             -> Django admin
```

### Key Patterns

**External News Integration**: Articles are fetched from NewsAPI via `articles/services/news_api.py`:
- `fetch_top_headlines()` - API call with category/country/page_size params
- `save_articles()` - Parses response, prevents duplicates via `external_id` (article URL)

**Article Model** (external news storage):
- `title`, `body` - Article content
- `source_name` - News source (e.g., "BBC News", "CNN")
- `url` - Original article link (also used as `external_id` for deduplication)
- `image_url` - Optional article image
- `published_at` - Original publish date from source

**Comment System**:
- Comments remain user-generated via `Comment` model
- `CommentForm` is a ModelForm with 140 char limit
- Only authenticated users can comment on fetched articles

**Removed Features** (from original article platform):
- No user article creation - articles come from NewsAPI only
- No edit/delete views - fetched articles are read-only
- Author field changed from ForeignKey to source_name CharField

**Class-Based Views (CBVs)**:
- `ArticleListView` - Paginated list of fetched articles
- `ArticleDetailView` - Combines `CommentGet` (GET) and `CommentPost` (POST) for article display + commenting
- `SignUpView` - User registration

**Forms**:
- Uses `django-crispy-forms` with `crispy-bootstrap5` for all form rendering
- `CommentForm` is the only user-facing form

**Custom User Model**:
- `AUTH_USER_MODEL = "accounts.CustomUser"` configured in settings
- Extends `AbstractUser` with optional `age` field

**Static Files**:
- WhiteNoise configured for production (`whitenoise.storage.CompressedManifestStaticFilesStorage`)
- Bootstrap 5 loaded via CDN in `base.html`

### Environment Configuration

Uses `environs` library with `.env` file support:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Boolean debug flag
- `DATABASE_URL` - PostgreSQL in production, defaults to SQLite locally
- `NEWS_API_KEY` - API key from newsapi.org (required for fetching)

### Deployment

Configured for Render deployment:
- `build.sh` - Install deps, collectstatic, migrate, create superuser
- `Procfile` - `web: gunicorn django_project.wsgi`
- `CSRF_TRUSTED_ORIGINS` includes `https://*.onrender.com`
- News fetching must be done manually or via scheduled job (not automated in deployment)

### Template Structure

All templates extend `templates/base.html`:
- Bootstrap 5 styling
- Navigation with auth-aware links
- Blocks: `title`, `content`
- Article images displayed when available (`image_url`)
- External article links open in new tab

## Testing Approach

Test files exist in each app (`tests.py`) but are minimal. Tests should:
- Use Django's `TestCase`
- Test model `get_absolute_url()` methods
- Test news API service with mocked responses
- Test comment form validation
- Test view permissions (login required for commenting)

## Common Operations

```bash
# Collect static files for production
python manage.py collectstatic --noinput

# Check deployment settings
python manage.py check --deploy

# Load shell with pre-imported models
python manage.py shell_plus

# Fetch latest news
python manage.py fetch_news --category general --count 20
```
