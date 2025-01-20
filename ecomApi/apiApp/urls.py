from django.urls import path, include
from django.conf import settings  # Add this import
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import BrandViewSet, CategoryViewSet, SubcategoryViewSet, ProductViewSet, ProductImageViewSet, ProductStockViewSet, ProductReviewViewSet, CartViewSet, CartProductViewSet, WishlistViewSet, OrderViewSet, OrderProductViewSet, WalletViewSet, WalletTransactionViewSet, OrderTrackingViewSet, UserProfileViewSet, UserVerificationViewSet, ProductOfferViewSet, FlashSaleViewSet

router = DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-images', ProductImageViewSet)
router.register(r'product-stocks', ProductStockViewSet)
router.register(r'product-reviews', ProductReviewViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-products', CartProductViewSet)
router.register(r'wishlists', WishlistViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-products', OrderProductViewSet)
router.register(r'wallets', WalletViewSet)
router.register(r'wallet-transactions', WalletTransactionViewSet)
router.register(r'order-trackings', OrderTrackingViewSet)
router.register(r'user-profiles', UserProfileViewSet)
router.register(r'user-verifications', UserVerificationViewSet)
router.register(r'product-offers', ProductOfferViewSet)
router.register(r'flash-sales', FlashSaleViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
