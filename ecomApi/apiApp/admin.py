from django.contrib import admin
from .models import (
    Brand, Category, Subcategory, ProductImage, Product, ProductVariant,
    ProductReview, Cart, CartProduct, Wishlist, Order, OrderProduct,
    Wallet, WalletTransaction, ProductOffer, FlashSale
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
    list_display = ('product_variant', 'image')
    search_fields = ('product_variant__product__title',)

admin.site.register(ProductImage, ProductImageAdmin)

# Product Variant Model Admin
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size', 'stock', 'additional_price')  # Correct fields
    search_fields = ('product__title', 'color', 'size')
    list_filter = ('color', 'size')

admin.site.register(ProductVariant, ProductVariantAdmin)

# Product Model Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'subcategory', 'brand', 'mrp', 'price', 'active', 'sku')
    search_fields = ('title', 'category__title', 'subcategory__title', 'brand__title')
    list_filter = ('active', 'category', 'subcategory', 'brand')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Product, ProductAdmin)

# Product Review Model Admin
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'approved')
    list_filter = ('approved', 'rating')
    search_fields = ('product__title', 'user__username', 'review')

admin.site.register(ProductReview, ProductReviewAdmin)

# Cart Product Model Admin
class CartProductAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__user__username', 'product__title')

admin.site.register(CartProduct, CartProductAdmin)

# Cart Model Admin
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

admin.site.register(Cart, CartAdmin)

# Wishlist Model Admin
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ('user__username', 'product__title')

admin.site.register(Wishlist, WishlistAdmin)

# Order Product Model Admin
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order__user__username', 'product__title')

admin.site.register(OrderProduct, OrderProductAdmin)

# Order Model Admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'status')

admin.site.register(Order, OrderAdmin)

# Wallet Model Admin
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username',)

admin.site.register(Wallet, WalletAdmin)

# Wallet Transaction Model Admin
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'amount', 'transaction_type', 'created_at')  # Removed 'order'
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('wallet__user__username',)

admin.site.register(WalletTransaction, WalletTransactionAdmin)

# Product Offer Model Admin
class ProductOfferAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percentage', 'start_date', 'end_date')
    search_fields = ('product__title',)

admin.site.register(ProductOffer, ProductOfferAdmin)

# Flash Sale Model Admin
class FlashSaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percentage', 'start_date', 'end_date')
    search_fields = ('product__title',)

admin.site.register(FlashSale, FlashSaleAdmin)
