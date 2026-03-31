import requests
from django.conf import settings


def fetch_top_headlines(category="general", country="us", page_size=20):
    """Fetch top headlines from NewsAPI."""
    api_key = settings.NEWS_API_KEY
    if not api_key:
        raise ValueError("NEWS_API_KEY not configured in settings")

    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "category": category,
        "country": country,
        "pageSize": page_size,
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def save_articles(articles_data):
    """Save fetched articles to database, skipping duplicates."""
    from articles.models import Article

    saved_count = 0
    for article_data in articles_data.get("articles", []):
        # Skip if missing required fields
        if not article_data.get("title") or not article_data.get("url"):
            continue

        # Use url as unique identifier to prevent duplicates
        external_id = article_data["url"]
        if Article.objects.filter(external_id=external_id).exists():
            continue

        # Parse published_at date
        published_at = article_data.get("publishedAt")
        if not published_at:
            from django.utils import timezone
            published_at = timezone.now()

        Article.objects.create(
            title=article_data["title"][:255],
            body=article_data.get("description") or article_data.get("content", ""),
            source_name=article_data.get("source", {}).get("name", "Unknown"),
            url=article_data["url"],
            image_url=article_data.get("urlToImage", ""),
            published_at=published_at,
            external_id=external_id,
        )
        saved_count += 1

    return saved_count
