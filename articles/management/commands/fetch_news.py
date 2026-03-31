from django.core.management.base import BaseCommand
from articles.services.news_api import fetch_top_headlines, save_articles


class Command(BaseCommand):
    help = "Fetch latest news from NewsAPI"

    def add_arguments(self, parser):
        parser.add_argument(
            "--category",
            default="general",
            help="News category (business, entertainment, general, health, science, sports, technology)",
        )
        parser.add_argument(
            "--country",
            default="us",
            help="Country code (e.g., us, gb, ca)",
        )
        parser.add_argument(
            "--count",
            type=int,
            default=20,
            help="Number of articles to fetch (max 100)",
        )

    def handle(self, *args, **options):
        self.stdout.write("Fetching news from NewsAPI...")
        try:
            data = fetch_top_headlines(
                category=options["category"],
                country=options["country"],
                page_size=options["count"],
            )
            saved = save_articles(data)
            self.stdout.write(
                self.style.SUCCESS(f"Successfully saved {saved} new articles")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error fetching news: {e}"))
