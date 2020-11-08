from django.apps import AppConfig

class NewsScraperConfig(AppConfig):
    name = 'news_scraper'

    def ready(self) -> None:
        from .scrapers import initialize_newspapers,scrape_everything
        initialize_newspapers()
        scrape_everything()
