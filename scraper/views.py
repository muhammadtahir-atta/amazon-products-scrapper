from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Brand, Product
from django.shortcuts import render

class BrandProductsAPIView(APIView):
    def get(self, request, brand_id):
        try:
            brand = Brand.objects.get(id=brand_id)
            products = Product.objects.filter(brand=brand)
            product_data = [
                {
                    "name": product.name,
                    "asin": product.asin,
                    "image_url": product.image_url,
                    "sku": product.sku
                } for product in products
            ]
            return Response({"products": product_data}, status=status.HTTP_200_OK)
        except Brand.DoesNotExist:
            return Response({"error": "Brand not found"}, status=status.HTTP_404_NOT_FOUND)
        
class BrandSelectionView(APIView):
    def get(self, request):
        brands = Brand.objects.all()
        return render(request, 'brand_product.html', {'brands': brands})  # Update the template name here

