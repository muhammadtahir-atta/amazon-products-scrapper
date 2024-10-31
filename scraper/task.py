from celery import shared_task
from .scrapping import AmazonScraperAPIView
import logging


logger = logging.getLogger(__name__)

@shared_task(name='scraper.task.scrape_amazon_products', bind=True, max_retries=3)
def scrape_amazon_products(self):
    logger.info("Starting scraping task...")
    scraper_view = AmazonScraperAPIView()
    request = type('Request', (object,), {})()  # Mock request object
    try:
        response = scraper_view.post(request)
        logger.info("Scraping completed successfully.")
        if response.status_code != 200:
            logger.error(f"Failed to scrape: {response.data}")
            raise Exception(f"Failed to scrape: {response.data}")
    except Exception as exc:
        logger.error(f"Error occurred: {exc}")
        raise self.retry(exc=exc, countdown=60)  # Retry after 60 seconds