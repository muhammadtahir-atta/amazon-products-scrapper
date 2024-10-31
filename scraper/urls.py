from django.urls import path, include
from rest_framework.routers import DefaultRouter
from scraper.views import BrandProductsAPIView,BrandSelectionView
from .scrapping import *



urlpatterns = [
    path('api/scrape-amazon/', AmazonScraperAPIView.as_view(), name='scrape_amazon'),
    path('api/brands/<int:brand_id>/', BrandProductsAPIView.as_view(), name='brand-products'),
    path('', BrandSelectionView.as_view(), name='brand-selection'),



]
