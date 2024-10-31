import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.db import IntegrityError
from .models import Brand, Product
from selenium.common.exceptions import NoSuchElementException

class AmazonScraperAPIView(APIView):
    def post(self, request):
        options = Options()
        options.headless = False
        service = Service('C:\\Demo\\chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=options)

        try:
            brands = Brand.objects.all()
            scraped_data = []

            for brand in brands:
                print(f"Scraping Amazon page for brand: {brand.name}")
                products_data = self.scrape_amazon_product(driver, brand.amazon_url)
                self.save_products_to_db(brand, products_data, scraped_data)

            return Response({"message": "Scraping completed successfully.", "data": scraped_data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            driver.quit()

    def scrape_amazon_product(self, driver, amazon_url):
        driver.get(amazon_url)
        time.sleep(3)
        driver.refresh()

        all_products_data = []

        while True:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".s-main-slot .s-result-item"))
                )

                product_elements = driver.find_elements(By.CSS_SELECTOR, ".s-main-slot .s-result-item")
                for product in product_elements:
                    try:
                        name = product.find_element(By.CSS_SELECTOR, "span.a-text-normal").text
                        asin = product.get_attribute("data-asin")
                        image_url = product.find_element(By.CSS_SELECTOR, "img.s-image").get_attribute("src")
                        sku = None  

                        all_products_data.append({
                            "name": name,
                            "asin": asin,
                            "image_url": image_url,
                            "sku": sku
                        })
                    except Exception as e:
                        print(f"Error extracting product data: {e}")

                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, ".s-pagination-next.s-pagination-button")
                    if "s-pagination-disabled" in next_button.get_attribute("class"):
                        print("Reached last page of pagination.")
                        break  
                    else:
                        next_button.click()  
                        time.sleep(5)  

                except NoSuchElementException:
                    print("Next button not found. Reached the last page.")
                    break  

            except Exception as e:
                print(f"Error navigating Amazon page: {e}")
                break  

        return all_products_data

    def save_products_to_db(self, brand, products_data, scraped_data):
        for product_data in products_data:
            try:
                product, created = Product.objects.update_or_create(
                    asin=product_data["asin"],
                    defaults={
                        "name": product_data["name"],
                        "sku": product_data["sku"],
                        "image_url": product_data["image_url"],
                        "brand": brand
                    }
                )
                if created:
                    print(f"Saved new product: {product_data['name']} ({product_data['asin']})")
                scraped_data.append(product_data)
            except IntegrityError:
                print(f"Product with ASIN {product_data['asin']} already exists.")
