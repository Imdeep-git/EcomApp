from rest_framework import serializers
from .models import (
    Brand, Category, Subcategory, Product, ProductVariant, ProductImage, ProductReview, 
    Cart, CartProduct, Wishlist, Order, OrderProduct, Wallet, WalletTransaction, 
    ProductOffer, FlashSale
)

# ===========================
# Core Serializers
# ===========================

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'


# ===========================
# Product and Inventory Serializers
# ===========================

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Returns user's username
    product = serializers.StringRelatedField(read_only=True)  # Returns product's title

    class Meta:
        model = ProductReview
        fields = '__all__'


# ===========================
# Cart and Wishlist Serializers
# ===========================

class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Embed product details

    class Meta:
        model = CartProduct
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(source='cartproduct_set', many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Embed product details

    class Meta:
        model = Wishlist
        fields = '__all__'


# ===========================
# Order Serializers
# ===========================

class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Embed product details

    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(source='orderproduct_set', many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


# ===========================
# Wallet Serializers
# ===========================

class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = '__all__'


class WalletSerializer(serializers.ModelSerializer):
    transactions = WalletTransactionSerializer(source='wallettransaction_set', many=True, read_only=True)

    class Meta:
        model = Wallet
        fields = '__all__'


# ===========================
# Promotion Serializers
# ===========================

class ProductOfferSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Embed product details

    class Meta:
        model = ProductOffer
        fields = '__all__'


class FlashSaleSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Embed product details

    class Meta:
        model = FlashSale
        fields = '__all__'
