from django.db import models
from django.utils.text import slugify
import uuid
from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model()


# Brand Model
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


# Category Model
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


# Subcategory Model
class Subcategory(models.Model):
    title = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    thumb = models.ImageField(upload_to='subcategory_thumbnails/', null=True, blank=True)
    banner = models.ImageField(upload_to='subcategory_banners/', null=True, blank=True)
    active = models.BooleanField(default=True)

    # SEO fields for subcategory
    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_keywords = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# Product Image Model (for variant images)
class ProductImage(models.Model):
    product_variant = models.ForeignKey('Product', related_name='variant_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_variant_images/')
    color = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.product_variant.title} - {self.color} - {self.size}"


# Product Model
class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    thumb = models.ImageField(upload_to='product_thumbnails/', null=True, blank=True)
    banner = models.ImageField(upload_to='product_banners/', null=True, blank=True)

    # Pricing fields
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)  # e.g., "kg", "piece"
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)

    # SEO fields
    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_keywords = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    active = models.BooleanField(default=True)

    # Variant options (color, size)
    color = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)

    # Foreign key to category and subcategory
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    # Foreign key to brand
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    # SKU Generation
    sku = models.CharField(max_length=100, unique=True, blank=True)

    # Product images for variant
    image_gallery = models.ManyToManyField(ProductImage, blank=True)

    # Stock Tracking
    total_stock = models.PositiveIntegerField(default=0)  # Tracks available stock

    def generate_sku(self):
        if not self.sku:
            self.sku = f"{self.brand.id}-{uuid.uuid4().hex[:8]}"  # SKU format: brand-id + unique identifier
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.generate_sku()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def update_stock(self, stock_type, quantity):
        """Update stock based on the stock type."""
        if stock_type == 'sale':
            self.total_stock -= quantity
        elif stock_type in ['purchase', 'restock']:
            self.total_stock += quantity
        self.save()


# Product Stock Management
class ProductStock(models.Model):
    STOCK_TYPE_CHOICES = [
        ('purchase', 'Purchase'),
        ('sale', 'Sale'),
        ('restock', 'Restock'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    stock_type = models.CharField(max_length=20, choices=STOCK_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=now)
    technician = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='technician_sales'
    )  # For technician service provider reports
    service_provider = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='service_provider_commissions'
    )  # For service provider commissions
    remarks = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.title} - {self.stock_type} - {self.quantity}"

    @property
    def product_sku(self):
        return self.product.sku


# Product Review Model
class ProductReview(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5)  # Star rating (1 to 5)
    review = models.TextField(null=True, blank=True)
    approved = models.BooleanField(default=False)  # Moderation flag

    def __str__(self):
        return f"Review for {self.product.title} by {self.user.username}"


# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartProduct')

    def __str__(self):
        return f"Cart for {self.user.username}"


# CartProduct Model (through table for Cart and Product)
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.title} in {self.cart.user.username}'s cart"


# Wishlist Model
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Wishlist for {self.user.username}"


# Order Model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProduct')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


# OrderProduct Model (through table for Order and Product)
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.title} in Order {self.order.id}"


# Wallet Model
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Wallet for {self.user.username}"


# Wallet Transaction Model
class WalletTransaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50)  # Deposit, Withdrawal, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} for {self.wallet.user.username}"


# Order Tracking Model
class OrderTracking(models.Model):
    order = models.ForeignKey(Order, related_name='tracking', on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order.id} - {self.status} at {self.updated_at}"


# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='user_profiles/', null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


# User Authentication (Email and Mobile Verification)
class UserVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
    mobile_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return f"Verification status for {self.user.username}"


# Product Offer Model
class ProductOffer(models.Model):
    product = models.ForeignKey(Product, related_name='offers', on_delete=models.CASCADE)
    discount_percentage = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Offer for {self.product.title} - {self.discount_percentage}% off"


# Flash Sales Model
class FlashSale(models.Model):
    product = models.ForeignKey(Product, related_name='flash_sales', on_delete=models.CASCADE)
    discount_percentage = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Flash Sale for {self.product.title} - {self.discount_percentage}% off"
