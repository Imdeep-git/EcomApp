from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

# ===========================
# Core Models
# ===========================

class Brand(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    thumb = models.ImageField(upload_to='brand_thumbnails/', null=True, blank=True)
    banner = models.ImageField(upload_to='brand_banners/', null=True, blank=True)

    # SEO fields
    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_keywords = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    thumb = models.ImageField(upload_to='category_thumbnails/', null=True, blank=True)
    banner = models.ImageField(upload_to='category_banners/', null=True, blank=True)
    active = models.BooleanField(default=True)

    # SEO fields
    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_keywords = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Subcategory(models.Model):
    title = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    thumb = models.ImageField(upload_to='subcategory_thumbnails/', null=True, blank=True)
    banner = models.ImageField(upload_to='subcategory_banners/', null=True, blank=True)
    active = models.BooleanField(default=True)

    # SEO fields
    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_keywords = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ===========================
# Product and Inventory
# ===========================

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    thumb = models.ImageField(upload_to='product_thumbnails/', null=True, blank=True)
    banner = models.ImageField(upload_to='product_banners/', null=True, blank=True)

    # Pricing fields
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Stock and Variant options
    color = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    total_stock = models.PositiveIntegerField(default=0)

    # Relationships
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    # SKU Generation
    sku = models.CharField(max_length=100, unique=True, blank=True)

    # SEO fields
    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_keywords = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    active = models.BooleanField(default=True)

    def generate_sku(self):
        if not self.sku:
            self.sku = f"{self.brand.id}-{uuid.uuid4().hex[:8]}"  # SKU format: brand-id + unique identifier

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.generate_sku()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    additional_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.title} - {self.color}/{self.size}"


class ProductImage(models.Model):
    product_variant = models.ForeignKey(ProductVariant, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_variant_images/')

    def __str__(self):
        return f"{self.product_variant.product.title} - {self.product_variant.color}/{self.product_variant.size}"


# ===========================
# Promotions
# ===========================

class ProductOffer(models.Model):
    product = models.ForeignKey(Product, related_name='offers', on_delete=models.CASCADE)
    discount_percentage = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Offer for {self.product.title} - {self.discount_percentage}% off"


class FlashSale(models.Model):
    product = models.ForeignKey(Product, related_name='flash_sales', on_delete=models.CASCADE)
    discount_percentage = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Flash Sale for {self.product.title} - {self.discount_percentage}% off"


# ===========================
# Reviews and Feedback
# ===========================

class ProductReview(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5)  # Star rating (1 to 5)
    review = models.TextField(null=True, blank=True)
    approved = models.BooleanField(default=False)  # Moderation flag

    def __str__(self):
        return f"Review for {self.product.title} by {self.user.username}"


# ===========================
# Orders, Cart, Wishlist, Wallet
# ===========================

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartProduct')

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.title} in {self.cart.user.username}'s cart"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Wishlist for {self.user.username}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProduct')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.title} in Order {self.order.id}"


# ===========================
# Wallet System
# ===========================

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Wallet for {self.user.username}"


class WalletTransaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50)  # Deposit, Withdrawal, etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} for {self.wallet.user.username}"
