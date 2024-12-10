from django.contrib import admin
from apiApp.models import *

# Register your models here.
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('subcategory_name',)
    
    search_fields = ('subcategory_name',)
    
    list_filter = ('subcategory_name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    
    #search box for 'category_name'
    search_fields = ('category_name',)

    list_filter = ('category_name',)  # Can filter categories by category_name
    
    filter_horizontal = ('subcategories',)

admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)



# registering products

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of empty forms to display

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory', 'price', 'stock_quantity')
    search_fields = ('name', 'description')
    list_filter = ('category', 'subcategory')
    inlines = [ProductImageInline]  

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('categories',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Product, ProductAdmin)