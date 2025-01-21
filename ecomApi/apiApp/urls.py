from django.urls import path, include
from django.conf import settings  # Add this import
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import (
    BrandViewSet, CategoryViewSet, SubcategoryViewSet, ProductViewSet, 
    ProductImageViewSet, ProductVariantViewSet, ProductReviewViewSet, 
    CartViewSet, CartProductViewSet, WishlistViewSet, OrderViewSet, 
    OrderProductViewSet, WalletViewSet, WalletTransactionViewSet, 
    ProductOfferViewSet, FlashSaleViewSet
)

# Initialize router
router = DefaultRouter()

# Register routes
router.register(r'brands', BrandViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-images', ProductImageViewSet)
router.register(r'product-variants', ProductVariantViewSet)  # Updated for ProductVariant
router.register(r'product-reviews', ProductReviewViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-products', CartProductViewSet)
router.register(r'wishlists', WishlistViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-products', OrderProductViewSet)
router.register(r'wallets', WalletViewSet)
router.register(r'wallet-transactions', WalletTransactionViewSet)
router.register(r'product-offers', ProductOfferViewSet)
router.register(r'flash-sales', FlashSaleViewSet)

# Define urlpatterns
urlpatterns = [
    path('api/', include(router.urls)),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
