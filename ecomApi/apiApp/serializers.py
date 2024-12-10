from rest_framework import serializers
from .models import SubCategory, Category, Product, ProductImage

# SubCategory Serializer
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory_name']


# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_icon', 'category_image', 'subcategories']


# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubCategorySerializer()
    images = serializers.PrimaryKeyRelatedField(queryset=ProductImage.objects.all(), many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'subcategory', 'description', 'price', 'discount', 'stock_quantity', 'specifications', 'slug', 'images']


# ProductImage Serializer
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image']
