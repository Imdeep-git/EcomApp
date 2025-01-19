from django.contrib import admin
from apiApp.models import (
    SubCategory, Category, Product, ProductImage, ProductVariant, ProductReview, InventoryLog, Wishlist
)

# SubCategory Admin
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('subcategory_name', 'slug')
    search_fields = ('subcategory_name',)
    list_filter = ('subcategory_name',)
    prepopulated_fields = {'slug': ('subcategory_name',)}  # Auto-generates the slug


# Category Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'is_active', 'slug')
    search_fields = ('category_name',)
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('category_name',)}
    filter_horizontal = ('subcategories',)  # Many-to-Many field


# Inline for Product Images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of empty forms to display


# Inline for Product Variants
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


# Inline for Product Reviews
class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 1
    readonly_fields = ('user', 'rating', 'comment', 'created_at')


# Product Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'subcategory', 'price', 'discounted_price',
        'stock_quantity', 'status', 'views_count', 'is_featured'
    )
    search_fields = ('name', 'description', 'tags')
    list_filter = ('category', 'subcategory', 'status', 'is_featured')
    readonly_fields = ('created_at', 'updated_at', 'discounted_price')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariantInline, ProductReviewInline]

    fieldsets = (
        ('General Information', {
            'fields': ('name', 'category', 'subcategory', 'description', 'specifications', 'tags', 'slug')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'discount_type', 'discount_value', 'discounted_price', 'stock_quantity', 'status')
        }),
        ('Additional Information', {
            'fields': ('is_featured', 'views_count', 'average_rating', 'review_count', 'available_date', 'currency')
        }),
        ('Meta Information', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at')
        }),
    )


# Wishlist Admin
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('added_at',)


# Inventory Log Admin
class InventoryLogAdmin(admin.ModelAdmin):
    list_display = ('product', 'change_quantity', 'created_at', 'note')
    search_fields = ('product__name', 'note')
    list_filter = ('created_at',)


# Registering all Admin Classes
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(InventoryLog, InventoryLogAdmin)
