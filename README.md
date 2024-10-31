
# Django E-commerce Scraper Application

This project is a Django application designed for scraping product data from e-commerce websites and saving it to a  database. It utilizes Celery for task scheduling and Redis as a message broker.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Using Celery](#using-celery)
- [Testing](#testing)
- [Notes](#notes)

## Requirements

- Python 3.8+
- Django 3.2+
- Redis (for Celery message broker)
- Celery 5.2+
- `pip` (Python package installer)
- `virtualenv` (optional but recommended for managing virtual environments)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/muhammadtahir-atta/amazon-products-scrapper
  
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Install the required packages:**

  - Also add the correct chromedriver path in scrapping.py file(Download Chromedriver and get the path of chromedriver.exe)

6. **Run the Redis server:**
   - Download and run `redis.exe` if you are on Windows, or start the Redis server using your preferred method on macOS/Linux.

7. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

8. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```
   - Follow the prompts to set the credentials of your choice.

9. **Run the Django development server:**
   ```bash
   python manage.py runserver
   ```

10. **Access the admin dashboard:**
   - Open your web browser and go to `http://127.0.0.1:8000/admin`.

11. **Add brands to scrape:**
    - In the admin dashboard, navigate to the "Brands" table and add the brands you want to scrape. Ensure to provide both the name and the URL.
    - Example URLs:
      - `https://www.amazon.com/s?i=kitchen&rh=n%3A289913%2Cp_123%3A1091235`
      - `https://www.amazon.com/s?i=kitchen&rh=n%3A289913%2Cp_123%3A391646`

## Using Celery

1. **Start the Celery worker in a new terminal:**
   ```bash
   celery -A Demo worker --loglevel=info --pool=solo
   ```

2. **Start the Celery beat scheduler in another new terminal:**
   ```bash
   celery -A Demo beat --loglevel=info
   ```

3. **Scheduled Task:**
   - The scraping task will be scheduled to run automatically every 6 hours. You can change this interval for testing purposes in the settings file.Also add a comment to change time for testing in Celery Configuration in settings.py.

4. **Check the database:**
   - When the task runs, the scraped product data will be saved in the database.

5. **Access the frontend:**
   - Visit the API endpoint to view the frontend page: `http://127.0.0.1:8000`.
   - Here, you can select a brand from the dropdown to view all products scraped from Amazon.

## Notes

- **SKU Information:**
  - Please note that SKU information is not included in the scraped products, as it is often not available on Amazon products, primarily showing details related to sellers.

- **Error Handling:**
  - Ensure Redis  is running before starting the server and Celery tasks to avoid connection errors.


