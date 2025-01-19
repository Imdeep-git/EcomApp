from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db.models import F

# SubCategory Model
class SubCategory(models.Model):
    subcategory_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.subcategory_name


# Category Model
class Category(models.Model):
    category_name = models.CharField(max_length=255)
    category_icon = models.ImageField(upload_to='categories/icons/')
    category_image = models.ImageField(upload_to='categories/images/')
    description = models.TextField(null=True, blank=True)
    subcategories = models.ManyToManyField(SubCategory, related_name='categories')
    slug = models.SlugField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name


# Product Model
PRODUCT_STATUS = (
    ('in_stock', 'In Stock'),
    ('out_of_stock', 'Out of Stock'),
    ('discontinued', 'Discontinued'),
)

DISCOUNT_TYPES = (
    ('percentage', 'Percentage'),
    ('fixed', 'Fixed'),
)

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES, default='percentage')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=PRODUCT_STATUS, default='in_stock')
    sku = models.CharField(max_length=100, unique=True)
    specifications = models.JSONField(default=dict, help_text="Store product specifications as a dictionary (e.g., {'processor': 'Intel i7', 'ram': '16GB'}).")
    slug = models.SlugField(max_length=500, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True, help_text="Comma-separated tags for the product.")
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    review_count = models.PositiveIntegerField(default=0)
    available_date = models.DateField(null=True, blank=True)
    currency = models.CharField(max_length=10, default="USD")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_products")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="updated_products")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.discount_type == 'percentage':
            self.discounted_price = self.price - (self.price * self.discount_value / 100)
        elif self.discount_type == 'fixed':
            self.discounted_price = self.price - self.discount_value
        super(Product, self).save(*args, **kwargs)


# ProductImage Model
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Image for {self.product.name}"


# ProductReview Model
class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  # e.g., 1-5 stars
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    helpful_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s review for {self.product.name}"


# ProductVariant Model
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    variant_name = models.CharField(max_length=255)  # e.g., "Color", "Size"
    variant_value = models.CharField(max_length=255)  # e.g., "Red", "XL"
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.variant_name}: {self.variant_value} for {self.product.name}"


# InventoryLog Model
class InventoryLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_logs')
    change_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Log for {self.product.name}: {self.change_quantity} items"


# Wishlist Model
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlisted_by")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


# Function to create a unique slug
def create_slug(instance):
    slug = slugify(instance.name)

    if instance.pk: 
        similar_slugs = Product.objects.filter(slug__startswith=slug).exclude(pk=instance.pk)
        if similar_slugs.exists():
            slug = f"{slug}-{similar_slugs.count() + 1}"
    else:
        similar_slugs = Product.objects.filter(slug=slug)
        if similar_slugs.exists():
            slug = f"{slug}-{similar_slugs.count() + 1}"

    return slug


# Signal to create a slug before saving the product
def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
        print(f"Generated slug for {instance.name}: {instance.slug}")  # Debug log to check the slug

pre_save.connect(pre_save_product_receiver, sender=Product)


# Signal to create a slug for SubCategory
def pre_save_subcategory_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.subcategory_name)

pre_save.connect(pre_save_subcategory_receiver, sender=SubCategory)


# Signal to create a slug for Category
def pre_save_category_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.category_name)

pre_save.connect(pre_save_category_receiver, sender=Category)


# Product Manager with Search Functionality
from django.contrib.postgres.search import SearchVector

class ProductManager(models.Manager):
    def search(self, query):
        return self.annotate(search=SearchVector('name', 'description', 'tags')).filter(search=query)

Product.objects = ProductManager()
