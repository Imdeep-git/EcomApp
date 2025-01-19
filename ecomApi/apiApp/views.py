from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from .models import SubCategory, Category, Product, ProductImage, ProductReview, ProductVariant
from .serializers import SubCategorySerializer, CategorySerializer, ProductSerializer, ProductImageSerializer

# SubCategory ViewSet
class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    search_fields = ['subcategory_name']  # Allow searching subcategory name
    ordering_fields = ['subcategory_name', 'id']  # Allow ordering by these fields
    ordering = ['subcategory_name']  # Default ordering

# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    search_fields = ['category_name']  # Allow searching category name
    ordering_fields = ['category_name', 'id']  # Allow ordering
    ordering = ['category_name']  # Default ordering

    # Optimize queryset with prefetch_related
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related(
            Prefetch('subcategories', queryset=SubCategory.objects.all())
        )

# Product ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    search_fields = ['name', 'description', 'tags']  # Allow searching products
    ordering_fields = ['name', 'created_at', 'price']  # Allow ordering
    ordering = ['name']  # Default ordering

    # Optimize queryset with select_related and prefetch_related
    def get_queryset(self):
        queryset = super().get_queryset()

        # Using select_related for single-valued relationships (ForeignKeys)
        queryset = queryset.select_related('category', 'subcategory')

        # Prefetch related data correctly for multi-valued relationships
        queryset = queryset.prefetch_related(
            Prefetch('images', queryset=ProductImage.objects.all()),  # Prefetch product images
            Prefetch('reviews', queryset=ProductReview.objects.all()),  # Prefetch product reviews
            Prefetch('variants', queryset=ProductVariant.objects.all())  # Prefetch product variants
        )

        return queryset

# ProductImage ViewSet
class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Filter by product ID from query parameters
    def get_queryset(self):
        queryset = super().get_queryset()
        product = self.request.query_params.get('product')

        # Validate product query parameter
        if product:
            try:
                product_id = int(product)
                queryset = queryset.filter(product__id=product_id)
            except ValueError:
                raise ValidationError({"product": "Product ID must be an integer."})

        return queryset
