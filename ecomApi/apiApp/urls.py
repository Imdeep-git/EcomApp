from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import SubCategoryViewSet, CategoryViewSet, ProductViewSet, ProductImageViewSet

# Setting up the router to automatically generate the URL routes for the viewsets
router = DefaultRouter()
router.register(r'subcategories', SubCategoryViewSet, basename='subcategories')  # For SubCategory model
router.register(r'categories', CategoryViewSet, basename='categories')  # For Category model
router.register(r'products', ProductViewSet, basename='products')  # For Product model
router.register(r'product-images', ProductImageViewSet, basename='product-images')  # For ProductImage model

urlpatterns = [
    path('api/', include(router.urls)),  # API base path including all the viewsets
]

# Serving media files (images) during development (only necessary if DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
