from rest_framework import serializers
from .models import SubCategory, Category, Product, ProductImage, ProductVariant, ProductReview

# SubCategory Serializer
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory_name', 'description', 'slug']

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_icon', 'category_image', 'description', 'subcategories', 'slug', 'is_active']

# ProductImage Serializer
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'order']

# ProductReview Serializer
class ProductReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'rating', 'comment', 'created_at', 'helpful_count']

# ProductVariant Serializer
class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'variant_name', 'variant_value', 'price', 'stock_quantity']

# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    # Optional related data, nullable if not found
    category = CategorySerializer(allow_null=True)
    subcategory = SubCategorySerializer(allow_null=True)
    
    # For read-only fields (images, reviews, variants)
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'subcategory', 'description', 'price', 'discount_type', 
            'discount_value', 'discounted_price', 'stock_quantity', 'status', 'sku', 
            'specifications', 'slug', 'tags', 'is_featured', 'views_count', 'average_rating', 
            'review_count', 'available_date', 'currency', 'is_active', 'created_at', 
            'updated_at', 'created_by', 'updated_by', 'images', 'reviews', 'variants'
        ]
