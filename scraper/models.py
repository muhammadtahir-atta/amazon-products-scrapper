from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=255)
    amazon_url = models.URLField()  # URL for the brand's page on Amazon

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    asin = models.CharField(max_length=20, unique=True)
    sku = models.CharField(max_length=20, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return f"{self.name} ({self.asin})"
