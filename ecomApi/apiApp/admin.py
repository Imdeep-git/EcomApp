from django.contrib import admin
from .models import (
    Brand, Category, Subcategory, ProductImage, Product, ProductStock,
    ProductReview, Cart, CartProduct, Wishlist, Order, OrderProduct,
    Wallet, WalletTransaction, OrderTracking, UserProfile, UserVerification,
    ProductOffer, FlashSale
)

# Brand Model Admin
class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'meta_title', 'meta_keywords', 'meta_description')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Brand, BrandAdmin)

# Category Model Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'meta_title', 'meta_keywords', 'meta_description', 'active')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)

# Subcategory Model Admin
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'slug', 'meta_title', 'meta_keywords', 'meta_description', 'active')
    search_fields = ('title', 'category__title')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Subcategory, SubcategoryAdmin)

# Product Image Model Admin
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product_variant', 'color', 'size')
    search_fields = ('product_variant__title',)

admin.site.register(ProductImage, ProductImageAdmin)

# Product Model Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'mrp', 'price', 'cost_price', 'active', 'category', 'subcategory', 'brand', 'sku')
    search_fields = ('title', 'category__title', 'subcategory__title', 'brand__title')
    list_filter = ('active', 'category', 'subcategory', 'brand')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Product, ProductAdmin)

# Product Stock Model Admin
class ProductStockAdmin(admin.ModelAdmin):
    list_display = ('product', 'stock_type', 'quantity', 'created_at', 'technician', 'service_provider')
    list_filter = ('stock_type', 'created_at')
    search_fields = ('product__title', 'technician__username', 'service_provider__username')

admin.site.register(ProductStock, ProductStockAdmin)

# Product Review Model Admin
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'approved')  # Removed created_at
    list_filter = ('approved', 'rating')
    search_fields = ('product__title', 'user__username', 'review')

admin.site.register(ProductReview, ProductReviewAdmin)

# Cart Model Admin
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

admin.site.register(Cart, CartAdmin)

# CartProduct Model Admin
class CartProductAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__user__username', 'product__title')

admin.site.register(CartProduct, CartProductAdmin)

# Wishlist Model Admin
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ('user__username', 'product__title')

admin.site.register(Wishlist, WishlistAdmin)

# Order Model Admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'status')

admin.site.register(Order, OrderAdmin)

# OrderProduct Model Admin
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order__user__username', 'product__title')

admin.site.register(OrderProduct, OrderProductAdmin)

# Wallet Model Admin
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username',)

admin.site.register(Wallet, WalletAdmin)

# WalletTransaction Model Admin
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'amount', 'transaction_type', 'created_at', 'order')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('wallet__user__username', 'order__id')

admin.site.register(WalletTransaction, WalletTransactionAdmin)

# OrderTracking Model Admin
class OrderTrackingAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'updated_at')
    list_filter = ('status', 'updated_at')
    search_fields = ('order__user__username',)

admin.site.register(OrderTracking, OrderTrackingAdmin)

# UserProfile Model Admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username',)

admin.site.register(UserProfile, UserProfileAdmin)

# UserVerification Model Admin
class UserVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_verified', 'mobile_verified', 'verification_code')
    list_filter = ('email_verified', 'mobile_verified')
    search_fields = ('user__username',)

admin.site.register(UserVerification, UserVerificationAdmin)

# ProductOffer Model Admin
class ProductOfferAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percentage', 'start_date', 'end_date')
    search_fields = ('product__title',)

admin.site.register(ProductOffer, ProductOfferAdmin)

# FlashSale Model Admin
class FlashSaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percentage', 'start_date', 'end_date')
    search_fields = ('product__title',)

admin.site.register(FlashSale, FlashSaleAdmin)
