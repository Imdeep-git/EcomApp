from rest_framework import viewsets
from .models import Brand, Category, Subcategory, Product, ProductImage, ProductStock, ProductReview, Cart, CartProduct, Wishlist, Order, OrderProduct, Wallet, WalletTransaction, OrderTracking, UserProfile, UserVerification, ProductOffer, FlashSale
from .serializers import BrandSerializer, CategorySerializer, SubcategorySerializer, ProductSerializer, ProductImageSerializer, ProductStockSerializer, ProductReviewSerializer, CartSerializer, CartProductSerializer, WishlistSerializer, OrderSerializer, OrderProductSerializer, WalletSerializer, WalletTransactionSerializer, OrderTrackingSerializer, UserProfileSerializer, UserVerificationSerializer, ProductOfferSerializer, FlashSaleSerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductStockViewSet(viewsets.ModelViewSet):
    queryset = ProductStock.objects.all()
    serializer_class = ProductStockSerializer


class ProductReviewViewSet(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer


class CartProductViewSet(viewsets.ModelViewSet):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer


class OrderProductViewSet(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class WalletTransactionViewSet(viewsets.ModelViewSet):
    queryset = WalletTransaction.objects.all()
    serializer_class = WalletTransactionSerializer


class OrderTrackingViewSet(viewsets.ModelViewSet):
    queryset = OrderTracking.objects.all()
    serializer_class = OrderTrackingSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserVerificationViewSet(viewsets.ModelViewSet):
    queryset = UserVerification.objects.all()
    serializer_class = UserVerificationSerializer


class ProductOfferViewSet(viewsets.ModelViewSet):
    queryset = ProductOffer.objects.all()
    serializer_class = ProductOfferSerializer


class FlashSaleViewSet(viewsets.ModelViewSet):
    queryset = FlashSale.objects.all()
    serializer_class = FlashSaleSerializer


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
